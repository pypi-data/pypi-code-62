from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import add_message
from django.contrib.auth.models import Group


@login_required()
def JoinRoleView(request, pk):
    if Group.objects.filter(pk=pk).exists():
        role = Group.objects.get(pk=pk)
        request.user.groups.add(role)
        message = f"Thank you for joining us as {role.name}."
        add_message(request, messages.SUCCESS, message, extra_tags="success")
        return redirect("djangoadmin:account_view")
    message = f"You are unable to join us as {role.name}."
    messages.add_message(request, messages.WARNING, message, extra_tags="warning")
    return redirect("djangoadmin:account_view")