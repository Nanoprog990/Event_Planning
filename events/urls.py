from django.urls import path
from .views import user_profile, register, update_profile, event_list, event_detail, create_event, edit_event, delete_event, rsvp_event, my_events, grant_collaborator_status, send_invitation

urlpatterns = [
    path('register/', register, name='register'),
    path('user_profile/', user_profile, name='user_profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('', event_list, name='event_list'),
    path('event/<int:event_id>/', event_detail, name='event_detail'),
    path('event/<int:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('create_event/', create_event, name='create_event'),
    path('delete/<int:event_id>/', delete_event, name='delete_event'),
    path('edit/<int:event_id>/', edit_event, name='edit_event'),
    path('my-events/', my_events, name='my_events'),
    path('event/<int:event_id>/grant_collaborator_status/', grant_collaborator_status, name='grant_collaborator_status'),
    path('event/<int:event_id>/send_invitation/', send_invitation, name='send_invitation'),
]