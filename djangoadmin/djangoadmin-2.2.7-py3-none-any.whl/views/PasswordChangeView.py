from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


@login_required()
def PasswordChangeView(request):
    user = request.user
    template_name = 'djangoadmin/djangoadmin/password_change_view_form.html'
    if request.method == "POST":
        passwordchangeform = PasswordChangeForm(data=request.POST, user=request.user)
        if passwordchangeform.is_valid():
            passwordchangeform.save()
            messages.success(request, f"Hello!, {user.first_name}, Your password changed successfully.", extra_tags='success')
            return redirect('djangoadmin:profile_view')
        else:
            messages.error(request, f"Hello!, {user.first_name}, Somthing went wrong, Try again.", extra_tags='error')
            return redirect('djangoadmin:password_change_view')
    else:
        passwordchangeform = PasswordChangeForm(user=request.user)
        context = { 'passwordchangeform': passwordchangeform }
        return render(request, template_name, context)