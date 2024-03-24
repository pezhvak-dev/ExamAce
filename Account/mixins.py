from django.shortcuts import redirect
from django.urls import reverse

from Account.variables import ErrorTexts as AccountValidationErrorStrings


class NonAuthenticatedUsersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("account:profile")
        return super(NonAuthenticatedUsersOnlyMixin, self).dispatch(request, *args, **kwargs)


class AuthenticatedUsersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            referring_url = request.META.get('HTTP_REFERER', None)
            request.session['referring_url'] = referring_url

            redirect_url = reverse("home:temp_info")
            message = AccountValidationErrorStrings.log_in_first
            success = "no"
            failure = "yes"
            next_url = reverse('account:login')
            return redirect(
                redirect_url + f'?message={message}&success={success}&failure={failure}&next_url={next_url}')
        return super(AuthenticatedUsersOnlyMixin, self).dispatch(request, *args, **kwargs)


class StaffOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_superuser or not user.is_staff:
            redirect_url = reverse("home:temp_info")
            message = AccountValidationErrorStrings.staff_only
            success = "no"
            failure = "yes"
            next_url = reverse('account:profile')
            return redirect(
                redirect_url + f'?message={message}&success={success}&failure={failure}&next_url={next_url}')

        return super(StaffOnlyMixin, self).dispatch(request, *args, **kwargs)


class NonStaffOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if user.is_superuser or user.is_staff:
            redirect_url = reverse("home:temp_info")
            message = AccountValidationErrorStrings.non_staff_only
            success = "no"
            failure = "yes"
            next_url = reverse('account:profile')
            return redirect(
                redirect_url + f'?message={message}&success={success}&failure={failure}&next_url={next_url}')

        return super(NonStaffOnlyMixin, self).dispatch(request, *args, **kwargs)


class SuperUserOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_superuser:
            redirect_url = reverse("home:temp_info")
            message = AccountValidationErrorStrings.non_staff_only
            success = "no"
            failure = "yes"
            next_url = reverse('account:profile')
            return redirect(
                redirect_url + f'?message={message}&success={success}&failure={failure}&next_url={next_url}')

        return super(SuperUserOnlyMixin, self).dispatch(request, *args, **kwargs)()
