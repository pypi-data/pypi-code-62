from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group


class RolesManagementView(LoginRequiredMixin, ListView):
    template_name = "djangoadmin/djangoadmin/roles_management_dashboard.html"
    model = Group
    context_object_name = "group_list"