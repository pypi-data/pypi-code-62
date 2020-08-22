from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def AccountView(request):
    template_name = 'djangoadmin/djangoadmin/account_view_dashboard.html'
    context = {"userdetail": request.user}
    return render(request, template_name, context)