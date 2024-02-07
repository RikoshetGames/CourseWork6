from django.urls import path
from shed.apps import ShedConfig
from shed.views import MessageListView, MessageCreateView, MessageUpdateView, \
    MessageDetailView, MessageDeleteView, MailCreateView, MailUpdateView, MailDeleteView, MailListView, \
    MailDetailView, ClientListView, ClientCreateView, ClientUpdateView, MailUpdateModeratorView, \
    HomeView

app_name = ShedConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('mail_list', MailListView.as_view(), name='mail_list'),
    path('mail_add/', MailCreateView.as_view(), name='mail_add'),
    path('mail_view/<int:pk>', MailDetailView.as_view(), name='mail_view'),
    path('mail_edit/<int:pk>/', MailUpdateView.as_view(), name='mail_edit'),
    path('mail_mod_edit/<int:pk>/', MailUpdateModeratorView.as_view(), name='mail_mod_edit'),
    path('mail_delete/<int:pk>/', MailDeleteView.as_view(), name='mail_delete'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_add/', MessageCreateView.as_view(), name='message_add'),
    path('message_edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message_view/<int:pk>/', MessageDetailView.as_view(), name='message_view'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client_add/', ClientCreateView.as_view(), name='client_add'),
    path('client_edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
]