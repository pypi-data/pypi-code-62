from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import add_message
from django.contrib.auth.models import Group


@login_required()
def LeaveRoleView(request, pk):
    if Group.objects.filter(pk=pk).exists():
        role = Group.objects.get(pk=pk)
        request.user.groups.remove(role)
        message = f"You have leaved {role.name} role."
        add_message(request, messages.SUCCESS, message, extra_tags="success")
        return redirect("djangoadmin:account_view")
    message = f"You are unable to leave {role.name} role."
    messages.add_message(request, messages.WARNING, message, extra_tags="warning")
    return redirect("djangoadmin:account_view")