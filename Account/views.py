import random
from uuid import uuid4

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView, UpdateView

from Account.forms import OTPRegisterForm, CheckOTPForm, RegularLogin, ForgetPasswordForm, ChangePasswordForm
from Account.mixins import NonAuthenticatedUsersOnlyMixin, AuthenticatedUsersOnlyMixin
from Account.models import CustomUser, OTP
from Home.sms import send_register_sms, send_forget_password_sms


class OTPRegisterView(FormView):
    template_name = "Account/register.html"
    form_class = OTPRegisterForm

    def form_valid(self, form):
        sms_code = random.randint(a=1000, b=9999)
        mobile_phone = form.cleaned_data.get('mobile_phone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        uuid = str(uuid4())

        OTP.objects.create(mobile_phone=mobile_phone, sms_code=sms_code, uuid=uuid, username=username,
                           password=password, otp_type="R")

        # send_register_sms(receptor=mobile_phone, sms_code=sms_code)
        print(sms_code)

        return redirect(reverse("account:check_otp") + f"?uuid={uuid}&mobile_phone={mobile_phone}")

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogInView(NonAuthenticatedUsersOnlyMixin, FormView):
    form_class = RegularLogin
    template_name = 'Account/login.html'

    def form_valid(self, form):
        request = self.request
        mobile_phone_or_username = form.cleaned_data.get('mobile_phone_or_username')
        password = form.cleaned_data.get('password')

        if mobile_phone_or_username.isdigit():
            user = CustomUser.objects.get(mobile_phone=mobile_phone_or_username)

        else:
            user = CustomUser.objects.get(username=mobile_phone_or_username)

        username = user.username

        authenticated_user = authenticate(request=request, username=username, password=password)

        if authenticated_user is not None:
            login(request=request, user=user)

        else:
            form.add_error(field="mobile_phone_or_username", error="هیچ حساب کاربری با این مشخصات یافت نشد.")

            return self.form_invalid(form)

        return redirect(reverse("account:profile", kwargs={"slug": request.user.username}))

    def get_success_url(self):
        referring_url = self.request.session.pop(key="referring_url", default=None)
        return referring_url or reverse_lazy("account:profile")


class LogOutView(View):
    def get(self, request):
        logout(request=request)
        next_url = request.GET.get("next")

        if next_url is not None:
            return redirect(next_url)

        else:
            try:
                home_url = reverse('home:home')

                return redirect(home_url)
            except:
                return redirect(to="home:home")


class ChangePasswordView(NonAuthenticatedUsersOnlyMixin, FormView):
    form_class = ChangePasswordForm
    template_name = 'Account/change_password.html'

    def form_valid(self, form):
        request = self.request
        new_password = form.cleaned_data.get('password')
        uuid = request.GET.get('uuid')

        otp = OTP.objects.get(uuid=uuid)
        mobile_phone = otp.mobile_phone

        user = CustomUser.objects.get(mobile_phone=mobile_phone)

        user.set_password(raw_password=new_password)
        user.save()

        login(request=request, user=user)

        otp.delete()

        redirect_url = reverse("home:temp_info")
        message = "رمز عبور با موفقیت تغییر یافت."
        success = "yes"
        failure = "no"
        next_url = reverse('account:profile')
        return redirect(
            redirect_url + f'?message={message}&success={success}&failure={failure}&next_url={next_url}')

    def form_invalid(self, form):
        return super().form_invalid(form)


class ForgetPasswordView(NonAuthenticatedUsersOnlyMixin, FormView):
    form_class = ForgetPasswordForm
    template_name = "Account/forget_password.html"

    def form_valid(self, form):
        mobile_phone_or_username = form.cleaned_data.get('mobile_phone_or_username')

        if str(mobile_phone_or_username).isdigit():
            user = CustomUser.objects.get(mobile_phone=mobile_phone_or_username)

        else:
            user = CustomUser.objects.get(username=mobile_phone_or_username)

        mobile_phone = user.mobile_phone
        username = user.username

        sms_code = random.randint(a=1000, b=9999)
        uuid = str(uuid4())

        OTP.objects.create(username=username, mobile_phone=mobile_phone, sms_code=sms_code, uuid=uuid,
                           otp_type="F")

        send_forget_password_sms(receptor=mobile_phone, sms_code=sms_code)

        return redirect(reverse(viewname="account:check_otp") + f"?uuid={uuid}&mobile_phone={mobile_phone}")

    def form_invalid(self, form):
        return super().form_invalid(form)


class CheckOTPView(FormView):
    form_class = CheckOTPForm
    template_name = 'Account/check_otp.html'

    def form_valid(self, form):
        request = self.request
        uuid = request.GET.get('uuid')
        sms_code = form.cleaned_data.get('sms_code')

        if OTP.objects.filter(uuid=uuid, sms_code=sms_code, otp_type="R").exists():
            otp = OTP.objects.get(uuid=uuid)

            mobile_phone = otp.mobile_phone
            username = otp.username
            password = otp.password

            user = CustomUser.objects.create_user(mobile_phone=mobile_phone, username=username)

            user.set_password(password)
            user.save()

            login(request=request, user=user)

            otp = OTP.objects.get(uuid=uuid)
            otp.delete()

            return redirect(to="account:profile")

        elif OTP.objects.filter(uuid=uuid, sms_code=sms_code, otp_type="F").exists():

            return redirect(reverse(viewname="account:change_password") + f"?uuid={uuid}")

        elif OTP.objects.filter(uuid=uuid, sms_code=sms_code, otp_type="D").exists():
            otp = OTP.objects.get(uuid=uuid)
            username = otp.username

            user_to_be_deleted = CustomUser.objects.get(username=username)

            user_to_be_deleted.delete()
            otp.delete()

            return redirect(to="home:home")

        else:
            form.add_error(field="sms_code", error="کد تایید نامعتبر است.")

            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ProfileDetailView(AuthenticatedUsersOnlyMixin, TemplateView):
    template_name = 'Account/profile.html'


class ProfileEditView(AuthenticatedUsersOnlyMixin, UpdateView):
    model = CustomUser
    template_name = 'Account/edit_profile.html'
    fields = ("full_name", "email", "about_me")
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_birth_date = CustomUser.objects.get(username=self.request.user.username).birth_date
        context['user_birth_date'] = user_birth_date

        return context

    def form_valid(self, form):
        birth_year = self.request.POST.get('birth_year', 1375)
        birth_month = self.request.POST.get('birth_month', 1)
        birth_day = self.request.POST.get('birth_day', 1)

        user = CustomUser.objects.get(username=self.request.user.username)
        user.birth_year = birth_year
        user.birth_month = birth_month
        user.birth_day = birth_day
        user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('account:profile', kwargs={'slug': self.request.user.username})
