from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='events_attending')
    collaborators = models.ManyToManyField(User, related_name='events_collaborating', blank=True)
    image = models.ImageField(upload_to='event_images/', blank=True)

class RSVP(models.Model):
    STATUS_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default="maybe")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    events_attending = models.ManyToManyField('Event', related_name='attendees_profiles', blank=True)
    is_collaborator = models.BooleanField(default=False)

class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_sent')
    date_sent = models.DateTimeField(auto_now_add=True)