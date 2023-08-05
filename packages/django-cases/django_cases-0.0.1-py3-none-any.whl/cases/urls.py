from django.urls import path
from . import views

from django.conf import settings
from django.views.static import serve
from django.conf.urls import url


app_name = 'cases'

urlpatterns = [
    path('case_details_lightbox/<int:id>/<skel_path:str>', views.case_details_lightbox, name='case_details_lightbox'),
    path('case_details_newpage/<int:id>/<skel_path:str>', views.case_details_newpage, name='case_details_newpage'),

    path('test_details/<int:id>/', views.test_details, name='test_details'),
    path('', views.test, name='test'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
