from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from djangoadmin.modelforms import UserModelForm
from djangoadmin.modelforms import EditProfileModelForm


@login_required()
def EditProfileView(request):
    user = request.user
    template_name = 'djangoadmin/djangoadmin/edit_profile_view_form.html'
    if request.method == "POST":
        userchangeform = EditProfileModelForm(request.POST or None, instance=request.user)
        userform = UserModelForm(request.POST or None, request.FILES or None, instance=request.user.usermodel)
        if userchangeform.is_valid() and userform.is_valid():
            userchangeform.save()
            userform.save()
            messages.success(request, f"Hello!, {user.first_name}, Your profile edited successfully.", extra_tags='success')
            return redirect('djangoadmin:profile_view')
        else:
            messages.error(request, f"Hello!, {user.first_name}, Somthing went wrong, Try again.", extra_tags='error')
            return redirect('djangoadmin:edit_profile_view')
    else:
        userchangeform = EditProfileModelForm(instance=request.user)
        userform = UserModelForm(instance=request.user.usermodel)
        context = { 'userchangeform': userchangeform, 'userform': userform }
        return render(request, template_name, context)