from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, get_user_model 
from django.contrib.auth.views import LoginView
from django import forms
from django.http import JsonResponse
from .models import Event, UserProfile, RSVP, Event, Invitation
from .forms import EventForm, CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, EventFilterForm, CollaboratorForm, InvitationForm
from .utils import send_notification

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('event_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'events/profile.html', {'user': user})

@login_required
def update_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': 'user_profile'})
            else:
                return redirect('user_profile')  # Redirect to profile page after successful update
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = UserProfileForm(instance=profile)
        return render(request, 'events/update_profile.html', {'form': form})
    
@login_required
def event_list(request):
    form = EventFilterForm(request.GET)
    events = Event.objects.all()

    if form.is_valid():
        if form.cleaned_data['organizer']:
            events = events.filter(organizer=form.cleaned_data['organizer'])
        if form.cleaned_data['location']:
            events = events.filter(location__icontains=form.cleaned_data['location'])

    return render(request, 'events/event_list.html', {'events': events, 'form': form})


User = get_user_model()

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_rsvp_response = None

    if request.user.is_authenticated:
        rsvp = RSVP.objects.filter(event=event, user=request.user).first()
        if rsvp:
            user_rsvp_response = rsvp.status

    # Attendees list (users who RSVP'd 'yes')
    attendees = event.attendees.all()

    # Users to invite (users who haven't RSVP'd yet)
    users_to_invite = User.objects.exclude(events_attending=event).exclude(id=event.organizer.id)

    # Potential collaborators (excluding superusers)
    potential_collaborators = User.objects.exclude(is_superuser=True).exclude(id=event.organizer.id)

    context = {
        'event': event,
        'user_rsvp_response': user_rsvp_response,
        'attendees': attendees,
        'users_to_invite': users_to_invite,
        'potential_collaborators': potential_collaborators,
    }

    return render(request, 'events/event_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES) 
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'action': 'Create'})

    
@login_required
def my_events(request):
    events = Event.objects.filter(organizer=request.user)
    rsvps = {event.id: RSVP.objects.filter(event=event) for event in events}
    context = {
        'events': events,
        'rsvps': rsvps,
    }
    return render(request, 'events/my_events.html', context)

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.user != event.organizer and not request.user.is_superuser and request.user not in event.collaborators.all():
        return redirect('login')  # Redirect to login page if user is not authorized
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {'form': form, 'action': 'edit'})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def grant_collaborator_status(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        collaborator_form = CollaboratorForm(request.POST)
        if collaborator_form.is_valid():
            user = collaborator_form.cleaned_data['user']
            event.collaborators.add(user)
            event.save()
            send_notification(
                user.email,
                'You have been granted collaborator status',
                f'You have been granted collaborator status for the event "{event.title}".'
            )
            messages.success(request, f'{user.username} has been granted collaborator status.')
        return redirect('event_detail', event_id=event_id)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_invitation(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        invitation_form = InvitationForm(request.POST)
        if invitation_form.is_valid():
            user = invitation_form.cleaned_data['user']
            Invitation.objects.create(event=event, user=user, invited_by=request.user)
            send_notification(
                user.email,
                'Event Invitation',
                f'You have been invited to the event "{event.title}".'
            )
            messages.success(request, f'Invitation sent to {user.username}.')
        return redirect('event_detail', event_id=event_id)
    
@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    status = request.POST.get('status')

    rsvp, created = RSVP.objects.get_or_create(user=request.user, event=event)
    rsvp.status = status
    rsvp.save()

    if status == 'yes':
        event.attendees.add(request.user)
    else:
        event.attendees.remove(request.user)

    try:
        subject = f'New RSVP for your event "{event.title}"'
        message = f'{request.user.username} has RSVP\'d {status} to your event "{event.title}".'
        
        send_notification(
            event.organizer.email,  # Pass the organizer's email correctly here
            subject,
            message,
        )
    except Exception as e:
        print(f"An error occurred while sending email: {e}")

    return redirect('event_detail', event_id=event.id)