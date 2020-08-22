from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from djangoadmin.modelforms import SigninModelForm


def LoginView(request):
    template_name = 'djangoadmin/djangoadmin/login_view_form.html'
    if request.method == 'POST':
        authenticationform = SigninModelForm(data=request.POST)
        if authenticationform.is_valid():
            user = authenticationform.get_user()
            login(request, user)
            if 'next' in request.POST:
                messages.success(request, f"{user.first_name} Loged in successfully.", extra_tags='success')
                return redirect(request.POST.get('next'))
            else:
                messages.success(request, f"{user.first_name} Loged in successfully.", extra_tags='success')
                return redirect('djangoadmin:account_view')
        else:
            messages.error(request, 'Something went wrong, please try again', extra_tags='warning')
            return redirect('djangoadmin:login_view')
    else:
        authenticationform = SigninModelForm()
        context = { 'authenticationform': authenticationform }
        return render(request, template_name, context)