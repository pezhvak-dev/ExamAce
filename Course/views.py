import ast
from datetime import datetime

import pytz
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import uri_to_iri
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, View
from django_filters.views import FilterView

from Account.mixins import AuthenticatedUsersOnlyMixin
from Account.models import FavoriteExam
from Course.filters import ExamFilter
from Course.mixins import ParticipatedUsersOnlyMixin, CheckForExamTimeMixin, AllowedExamsOnlyMixin, \
    DownloadedQuestionsFileFirstMixin, AllowedFilesDownloadMixin, NonFinishedExamsOnlyMixin
from Course.models import BoughtExam, VideoCourse, Exam, ExamAnswer, DownloadedQuestionFile, EnteredExamUser, \
    UserFinalAnswer, \
    UserTempAnswer, ExamSection, ExamUnit
from Home.mixins import URLStorageMixin
from Home.models import Banner4, Banner5
from utils.useful_functions import get_time_difference


class AllVideoCourses(URLStorageMixin, ListView):
    model = VideoCourse
    context_object_name = 'video_courses'
    template_name = 'Course/all_video_courses.html'

    def get_queryset(self):
        video_courses = VideoCourse.objects.select_related('category', 'teacher').order_by('-created_at')

        return video_courses


class VideoCourseDetail(URLStorageMixin, DetailView):
    model = VideoCourse
    context_object_name = 'course'
    template_name = 'Course/video_course_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'teacher')

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})


class VideoCourseByCategory(URLStorageMixin, ListView):
    model = VideoCourse
    context_object_name = 'video_courses'
    template_name = 'Course/video_courses_by_category.html'

    def get_queryset(self):
        slug = uri_to_iri(self.kwargs.get('slug'))

        video_courses = get_list_or_404(VideoCourse, category__slug=slug)

        return video_courses


class AllBookCourses(URLStorageMixin, ListView):
    pass


class AllExams(URLStorageMixin, ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = 'Course/all_exams.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            favorite_exams = Exam.objects.filter(favoriteexam__user=user).values_list('id', flat=True)
        else:
            favorite_exams = []

        context['favorite_exams'] = favorite_exams

        return context

    def get_queryset(self):
        exams = Exam.objects.select_related('category', 'designer').order_by('-created_at')

        return exams


class ExamDetail(URLStorageMixin, DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'Course/exam_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('category', 'designer')

    def get_object(self, queryset=None):
        slug = uri_to_iri(self.kwargs.get(self.slug_url_kwarg))
        queryset = self.get_queryset()
        return get_object_or_404(queryset, **{self.slug_field: slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        sections = ExamSection.objects.filter(exam=self.object)

        section_names = list(set(sections.values_list('name', flat=True)))
        banner_4 = Banner4.objects.filter(can_be_shown=True).last()
        banner_5 = Banner5.objects.filter(can_be_shown=True).last()

        #  Checks if user can enter exam anymore or not. (Based on entrance time)
        is_time_up = False

        if self.request.user.is_authenticated:
            if EnteredExamUser.objects.filter(
                    user=user, exam=self.object
            ).exists():
                entered_exam_user = EnteredExamUser.objects.get(user=user, exam=self.object)

                date_1 = entered_exam_user.created_at
                date_2 = datetime.now(pytz.timezone('Iran'))

                total_duration = self.object.total_duration.total_seconds()

                difference = get_time_difference(date_1=date_1, date_2=date_2)

                time_left = int(total_duration - difference)

                if time_left < 0:
                    is_time_up = True

            can_be_continued = False
            if EnteredExamUser.objects.filter(user=user, exam=self.object).exists():
                can_be_continued = True

            has_finished_exam = False
            if UserFinalAnswer.objects.filter(user=user, exam=self.object).exists():
                has_finished_exam = True

            try:
                is_user_registered = Exam.objects.filter(participated_users=user, slug=self.object.slug).exists()

            except TypeError:
                is_user_registered = False

        else:
            is_user_registered = False
            can_be_continued = False
            has_finished_exam = False

        context['banner_4'] = banner_4  # Returns a single object
        context['banner_5'] = banner_5  # Returns a single object
        context['is_time_up'] = is_time_up  # Returns a boolean
        context['is_user_registered'] = is_user_registered  # Returns a boolean
        context['can_be_continued'] = can_be_continued  # Returns a boolean
        context['has_finished_exam'] = has_finished_exam  # Returns a boolean
        context['sections_names'] = section_names  # Returns a list

        return context


class ExamQuestionDownload(AuthenticatedUsersOnlyMixin, AllowedFilesDownloadMixin,
                           ParticipatedUsersOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get('slug')
        exam = Exam.objects.get(slug=slug)
        questions_file = exam.questions_file

        # Set headers for file download
        response = HttpResponse(questions_file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{exam.question_file_name}.pdf"'

        if not DownloadedQuestionFile.objects.filter(exam=exam, user=user).exists():
            DownloadedQuestionFile.objects.create(exam=exam, user=user)

        return response


class EnterExam(AuthenticatedUsersOnlyMixin, ParticipatedUsersOnlyMixin, AllowedExamsOnlyMixin,
                CheckForExamTimeMixin, NonFinishedExamsOnlyMixin, View):
    template_name = "Course/multiple_choice_exam.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get('slug')

        exam_section = ExamSection.objects.get(slug=slug)

        exam = Exam.objects.get(sections=exam_section)
        sections = ExamSection.objects.filter(exam=exam)
        flag = False
        next_section = None
        for section in sections:
            if flag:
                next_section = section.slug
            if section == exam_section:
                flag = True

        answer = UserTempAnswer.objects.filter(user=user, exam__sections=exam_section).last()

        if not EnteredExamUser.objects.filter(exam=exam, user=user).exists():
            EnteredExamUser.objects.create(exam=exam, user=user)

        entered_exam_user = EnteredExamUser.objects.get(exam=exam, user=user)

        date_1 = entered_exam_user.created_at
        date_2 = datetime.now(pytz.timezone('Iran'))

        total_duration = exam_section.total_duration.total_seconds()

        difference = get_time_difference(date_1=date_1, date_2=date_2)

        time_left = int(total_duration - difference)

        questions_and_answers = []
        exam_answers = ExamAnswer.objects.filter(unit__section=exam_section)

        for exam_answer in exam_answers:
            if UserTempAnswer.objects.filter(
                    user=user, question_number=exam_answer.question_number
            ).exists():
                exam_temp_answer = UserTempAnswer.objects.get(
                    user=user,
                    question_number=exam_answer.question_number
                )

                questions_and_answers.append(
                    {
                        "id": exam_answer.id,
                        "slug": exam_answer.unit.slug,
                        "question": exam_answer.question,
                        "question_number": exam_answer.question_number,
                        "answer_1": exam_answer.answer_1,
                        "answer_2": exam_answer.answer_2,
                        "answer_3": exam_answer.answer_3,
                        "answer_4": exam_answer.answer_4,
                        "selected_answer": exam_temp_answer.selected_answer
                    }
                )

            else:
                questions_and_answers.append(
                    {
                        "id": exam_answer.id,
                        "slug": exam_answer.unit.slug,
                        "question": exam_answer.question,
                        "question_number": exam_answer.question_number,
                        "answer_1": exam_answer.answer_1,
                        "answer_2": exam_answer.answer_2,
                        "answer_3": exam_answer.answer_3,
                        "answer_4": exam_answer.answer_4,
                        "selected_answer": None
                    }
                )

        context = {
            'time_left': time_left,
            'slug': exam.slug,
            'answer': answer,
            'next_section': next_section,
            'questions_and_answers': questions_and_answers
        }

        return render(request=request, template_name=self.template_name, context=context)


class CalculateExamResult(AuthenticatedUsersOnlyMixin, ParticipatedUsersOnlyMixin, AllowedExamsOnlyMixin, View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        user = request.user
        exam = get_object_or_404(Exam, slug=slug)

        user_final_answers = UserFinalAnswer.objects.filter(user=user, exam=exam).values("question_number",
                                                                                         "selected_answer")

        correct_answers = ExamAnswer.objects.filter(exam=exam).values("question_number", "true_answer",
                                                                      "true_answer_explanation", "section_id",
                                                                      "unit_id")

        section_mapping = {section.id: section for section in
                           ExamSection.objects.filter(examanswer__exam=exam).distinct()}

        unit_mapping = {unit.id: unit for unit in ExamUnit.objects.filter(examanswer__exam=exam).distinct()}

        # Create a dictionary to store the comparison results
        answer_comparison = {}

        # Convert querysets to dictionaries for easier lookup
        user_final_answers_dict = {answer['question_number']: answer['selected_answer'] for answer in
                                   user_final_answers}
        correct_answers_dict = {answer['question_number']: {'true_answer': answer['true_answer'],
                                                            'true_answer_explanation': answer[
                                                                'true_answer_explanation'],
                                                            'section_id': answer['section_id'],
                                                            'unit_id': answer['unit_id']}
                                for answer in correct_answers}

        # Iterate over each question number in correct_answers_dict to populate answer_comparison
        for question_number in correct_answers_dict:
            correct_answer_info = correct_answers_dict[question_number]
            correct_answer = correct_answer_info['true_answer']
            true_answer_explanation = correct_answer_info['true_answer_explanation']
            section_id = correct_answer_info['section_id']
            unit_id = correct_answer_info['unit_id']
            user_selected_answer = user_final_answers_dict.get(question_number)

            # Fetch ExamSection and ExamUnit details using section_id and unit_id from the mappings
            if section_id in section_mapping:
                section = section_mapping[section_id]
                section_name = section.name
            else:
                section_name = None

            if unit_id in unit_mapping:
                unit = unit_mapping[unit_id]
                unit_coefficient = unit.coefficient
            else:
                unit_coefficient = None

            # Check if user has not answered a question (selected_answer is None)
            if user_selected_answer is None:
                user_selected_answer = None
                answered_correctly = False
            else:
                answered_correctly = (user_selected_answer == correct_answer)

            answer_comparison[question_number] = {
                'correct_answer': correct_answer,
                'user_selected_answer': user_selected_answer,
                'true_answer_explanation': true_answer_explanation,
                'answered_correctly': answered_correctly,
                'section_name': section_name,
                'unit_coefficient': unit_coefficient
            }

        context = {
            "answer_comparison": answer_comparison,
        }

        return render(request, "Course/answer_results.html", context=context)


class ExamsByCategory(URLStorageMixin, ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = 'Course/exams_by_category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        if user.is_authenticated:
            favorite_exams = Exam.objects.filter(favoriteexam__user=user).values_list('id', flat=True)
        else:
            favorite_exams = []

        context['favorite_exams'] = favorite_exams

        return context

    def get_queryset(self):
        slug = uri_to_iri(self.kwargs.get('slug'))

        exams = get_list_or_404(Exam, category__slug=slug)

        return exams


class ExamFilterView(View):
    template_name = "Course/exam_filter.html"

    def get(self, request):
        exams = Exam.objects.all()
        exam_filter = ExamFilter(request.GET, queryset=exams)

        user = self.request.user
        if user.is_authenticated:
            favorite_exams = Exam.objects.filter(favoriteexam__user=user).values_list('id', flat=True)
        else:
            favorite_exams = []

        context = {
            'exams': exam_filter.qs,
            'favorite_exams': favorite_exams
        }

        return render(request=request, template_name=self.template_name, context=context)


@method_decorator(csrf_exempt, name='dispatch')
class ToggleFavorite(View):
    def post(self, request, *args, **kwargs):
        exam_id = request.POST.get('exam_id')
        user = request.user

        try:
            exam = Exam.objects.get(id=exam_id)
            if FavoriteExam.objects.filter(exam=exam, user=user).exists():
                FavoriteExam.objects.filter(exam=exam, user=user).delete()
                return JsonResponse({'success': True, 'action': 'removed'})
            else:
                FavoriteExam.objects.create(exam=exam, user=user)
                return JsonResponse({'success': True, 'action': 'added'})
        except Exam.DoesNotExist:
            pass

        return JsonResponse({'success': False}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class RegisterInExam(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        exam_id = request.POST.get('courseId')
        user = self.request.user

        exam = Exam.objects.get(id=exam_id)

        if not Exam.objects.filter(id=exam_id, participated_users=user).exists():
            exam.participated_users.add(user)
            exam.save()

            exam.participated_users.add(user)
            exam.save()

            BoughtExam.objects.create(user=user, exam=exam)

            return JsonResponse(data={"message": f"ثبت نام در دوره {exam.name} با موفقیت انجام شد."},
                                status=200)

        else:
            return JsonResponse(data={"message": f"شما قبلا در دوره {exam.name} ثبت نام کردید."},
                                status=400)


@method_decorator(csrf_exempt, name='dispatch')
class TempExamSubmit(AuthenticatedUsersOnlyMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        slug = kwargs.get("slug")

        question_number = request.POST.get("question_number")
        selected_answer = request.POST.get("selected_answer")

        exam_section = ExamSection.objects.filter(slug=slug).last()

        try:
            temp_answer = UserTempAnswer.objects.get(
                user=user,
                question_number=question_number
            )

            temp_answer.selected_answer = selected_answer
            temp_answer.question_number = question_number
            temp_answer.save()

        except UserTempAnswer.DoesNotExist:
            UserTempAnswer.objects.create(
                user=user,
                exam_section=exam_section,
                question_number=question_number,
                selected_answer=selected_answer
            )

        return JsonResponse(
            data={
                "message": "saved!"
            },
            status=200
        )
