from django.urls import path
from . import views

from django.conf import settings
from django.views.static import serve
from django.conf.urls import url


app_name = 'cases'

urlpatterns = [
    path('case_details/<int:id>/<str:app_name>/', views.case_details, name='case_details'),

    path('', views.test, name='test'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
