from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class NonAuthenticatedUsersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        redirect_url = request.session.get('current_url')

        if redirect_url is not None:
            return redirect(redirect_url)

        return redirect("home:home")


class AuthenticatedUsersOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "ابتدار وارد حساب کاربری خود شوید.")

            redirect_url = request.session.get('current_url')

            if redirect_url is not None:
                return redirect(redirect_url)

            return redirect("home:home")

        return super(AuthenticatedUsersOnlyMixin, self).dispatch(request, *args, **kwargs)


class StaffOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_superuser or not user.is_staff:
            redirect_url = reverse("home:temp_info")
            message = "این بخش فقط مخصوص ادمین های وبسایت است."
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
            message = "این بخش فقط مخصوص کاربران معمولی وبسایت است."
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
            message = "این بخش فقط مخصوص کاربران معمولی وبسایت است."
            success = "no"
            failure = "yes"
            next_url = reverse('account:profile')
            return redirect(
                redirect_url + f'?message={message}&success={success}&failure={failure}&next_url={next_url}')

        return super(SuperUserOnlyMixin, self).dispatch(request, *args, **kwargs)()
