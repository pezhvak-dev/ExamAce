import random
from uuid import uuid4

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from Account.forms import OTPRegisterForm, CheckOTPForm, RegularLogin, ForgetPasswordForm, ChangePasswordForm
from Account.mixins import NonAuthenticatedUsersOnlyMixin, AuthenticatedUsersOnlyMixin
from Account.models import CustomUser, OTP
from Account.variables import Numbers as AccountMaxAndMinLengthStrings
from Account.variables import Strings as AccountModelVerboseNameStrings
from Account.variables import ErrorTexts as AccountValidationErrorStrings
from Home.sms import send_register_sms, send_forget_password_sms


class OTPRegisterView(FormView):
    template_name = "Account/register.html"
    form_class = OTPRegisterForm

    def form_valid(self, form):
        sms_code = random.randint(a=AccountMaxAndMinLengthStrings.sms_code_random_min,
                                  b=AccountMaxAndMinLengthStrings.sms_code_random_max)
        mobile_phone = form.cleaned_data.get('mobile_phone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        uuid = str(uuid4())

        OTP.objects.create(mobile_phone=mobile_phone, sms_code=sms_code, uuid=uuid, username=username,
                           password=password, otp_type=AccountModelVerboseNameStrings.register_mode_en)

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
            form.add_error(field="mobile_phone_or_username", error=AccountValidationErrorStrings.no_accounts_were_found)

            return self.form_invalid(form)

        return super().form_valid(form)

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
        message = AccountValidationErrorStrings.successful_job(job=AccountModelVerboseNameStrings.password_change)
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

        sms_code = random.randint(a=AccountMaxAndMinLengthStrings.sms_code_random_min,
                                  b=AccountMaxAndMinLengthStrings.sms_code_random_max)
        uuid = str(uuid4())

        OTP.objects.create(username=username, mobile_phone=mobile_phone, sms_code=sms_code, uuid=uuid,
                           otp_type=AccountModelVerboseNameStrings.forget_password_mode_en)

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

        if OTP.objects.filter(uuid=uuid, sms_code=sms_code,
                              otp_type=AccountModelVerboseNameStrings.register_mode_en).exists():
            otp = OTP.objects.get(uuid=uuid)

            mobile_phone = otp.mobile_phone
            username = otp.username
            password = otp.password
            slug = otp.slug

            user = CustomUser.objects.create_user(mobile_phone=mobile_phone, username=username)

            user.set_password(password)
            user.save()

            login(request=request, user=user)

            otp = OTP.objects.get(uuid=uuid)
            otp.delete()

            return redirect(to="account:profile")

        elif OTP.objects.filter(uuid=uuid, sms_code=sms_code,
                                otp_type=AccountModelVerboseNameStrings.forget_password_mode_en).exists():

            return redirect(reverse(viewname="account:change_password") + f"?uuid={uuid}")

        elif OTP.objects.filter(uuid=uuid, sms_code=sms_code,
                                otp_type=AccountModelVerboseNameStrings.delete_account_mode_en).exists():
            otp = OTP.objects.get(uuid=uuid)
            username = otp.username

            user_to_be_deleted = CustomUser.objects.get(username=username)

            user_to_be_deleted.delete()
            otp.delete()

            return redirect(to="home:home")

        else:
            form.add_error(field="sms_code", error=AccountValidationErrorStrings.sms_code_invalid)

            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ProfileDetailView(AuthenticatedUsersOnlyMixin, TemplateView):
    template_name = 'Account/profile.html'
