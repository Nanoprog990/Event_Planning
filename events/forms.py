from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Event, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(required=False, widget=forms.Textarea)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Create the associated UserProfile instance
            UserProfile.objects.create(
                user=user,
                bio=self.cleaned_data.get('bio', ''),
                profile_picture=self.cleaned_data.get('profile_picture', None)
            )
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

class EventFilterForm(forms.Form):
    organizer = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label="Organizer")
    location = forms.CharField(max_length=200, required=False, label="Location")

class CollaboratorForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=False), label="Select User")

class InvitationForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=False), label="Select User")
