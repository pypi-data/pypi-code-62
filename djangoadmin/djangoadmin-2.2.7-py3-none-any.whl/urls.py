from django.urls import include, reverse_lazy
from django.conf.urls import re_path
from django.urls import include
from djangoadmin import views
from django.contrib.auth import views as auth_views

app_name = "djangoadmin"


urlpatterns = [
    # urlpatterns for rest_api.
    re_path(r'^api/', include('djangoadmin.rest_api.urls')),
    # normal views.
    re_path(r'^account/$', views.AccountView, name='account_view'),
    re_path(r'^profile/$', views.ProfileView, name='profile_view'),
    re_path(r'^profile/edit/$', views.EditProfileView, name="edit_profile_view"),
    re_path(r'^register/$', views.SignupView, name="signup_view"),
    re_path(r'^login/$', views.LoginView, name="login_view"),
    re_path(r'^password-change/$', views.PasswordChangeView, name="password_change_view"),
    re_path(r'^password-reset/$', auth_views.PasswordResetView.as_view(template_name="djangoadmin/djangoadmin/password_reset_view.html", email_template_name='djangoadmin/djangoadmin/password_reset_email.html', success_url=reverse_lazy('djangoadmin:password_reset_done')), name="password_reset"),
    re_path(r'^password-reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name="djangoadmin/djangoadmin/password_reset_done_view.html"), name="password_reset_done"),
    re_path(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(template_name="djangoadmin/djangoadmin/password_reset_confirm_view.html", success_url=reverse_lazy('djangoadmin:password_reset_complete')), name="password_reset_confirm"),
    re_path(r'^password-reset-complete/$', auth_views.PasswordResetCompleteView.as_view(template_name="djangoadmin/djangoadmin/password_reset_complete_view.html"), name="password_reset_complete"),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name="logout_view"),
    re_path(r'^join/(?P<pk>[\w-]+)/$', views.JoinRoleView, name="join_role_view"),
    re_path(r'^leave/(?P<pk>[\w-]+)/$', views.LeaveRoleView, name="leave_role_view"),
    re_path(r'^roles/$', views.RolesManagementView.as_view(), name="roles_management_view"),
]