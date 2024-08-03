from django.contrib import admin
from .models import Event, RSVP, UserProfile, Invitation

admin.site.register(Event)
admin.site.register(RSVP)
admin.site.register(UserProfile)
admin.site.register(Invitation)