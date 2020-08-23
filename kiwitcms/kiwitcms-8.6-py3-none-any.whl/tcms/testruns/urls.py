from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^new/$', views.CreateTestRunView.as_view(), name='testruns-new'),
    re_path(r'^(?P<pk>\d+)/$', views.GetTestRunView.as_view(), name='testruns-get'),
    re_path(r'^(?P<pk>\d+)/clone/$', views.CloneTestRunView.as_view(), name='testruns-clone'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.EditTestRunView.as_view(), name='testruns-edit'),

    re_path(r'^(?P<pk>\d+)/report/$', views.TestRunReportView.as_view(),
            name='run-report'),

    re_path(r'^(?P<pk>\d+)/changestatus/$', views.ChangeTestRunStatusView.as_view(),
            name='testruns-change_status'),

    re_path(r'^(?P<pk>\d+)/assigncase/$', views.AddCasesToRunView.as_view(),
            name='add-cases-to-run'),

    re_path(r'^(?P<pk>\d+)/cc/$', views.ManageTestRunCC.as_view(), name='testruns-cc'),
    re_path(r'^search/$', views.SearchTestRunView.as_view(), name='testruns-search'),
]
