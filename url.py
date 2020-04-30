from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Index.as_view(),name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('send-message/<int:id>/', views.SendMessage.as_view(), name='send_message'),
    path('my-messages/', views.MyMessages.as_view(), name='my-messages'),
    path('admin-page/', views.Admin.as_view(),name='admin-page')
]
