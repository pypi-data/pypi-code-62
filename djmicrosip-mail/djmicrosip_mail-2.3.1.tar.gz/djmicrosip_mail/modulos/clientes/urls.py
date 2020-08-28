# from django.conf.urls import patterns
from django.urls import path,include
from .views import ClienteListView, IgnorarView

urlpatterns = (
	path('clientes/', ClienteListView.as_view()),
	path('ignorar/', IgnorarView),
		
)
