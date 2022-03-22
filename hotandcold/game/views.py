"""Views used in game app.

Handles actual functionality of different views.
"""

from random import choice

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render, get_object_or_404

from .models import Event, Player
from .forms import UserRegistrationForm, EventCreationForm


def test(request):
    return render(request, "game/extended.html", {"title": "Extended Page"})


def home(request):
    """Home view.

    Display the home page.

    Arguments:
    request - Django object containing request information.

    Returns:
    render - Django function to give a HTTP response with a template.
    """
    player_score_list = Player.objects.order_by("-points")[:10]
    context = {"player_score_list": player_score_list}
    return render(request, "game/home.html", context)


def log_in(request):
    """Login view.

    If the request type is POST, login the user and redirect them to the
    home view. Otherwise, display the user login form.

    Arguments:
    request - Django object containing request information.

    Returns:
    render - Django function to give a HTTP response with a template.
    """
    title = "Login"

    # Check the request type.
    if request.method == "POST":
        # Create a form with the POST data.
        form = AuthenticationForm(request, data=request.POST)

        # Check form validity.
        if form.is_valid():
            # Get username and password from form.
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Attempt to authenticate the user.
            user = authenticate(username=username, password=password)
            # Check if the user actually exists.
            if user is not None:
                # Log the user in.
                login(request, user)

                # Redirect to the home view.
                return redirect("home")
        else:
            # Form invalid, show error message.
            messages.warning(request, "Username/password incorrect!")
    
    # Create an empty login form and show it.
    form = AuthenticationForm()
    return render(request, "game/login.html", {"form": form, "title": title})


def log_out(request):
    """Logout the currently logged in user.

    If no one is currently logged in, nothing happens and the user is
    redirected to the home view.

    Arguments:
    request - Django request object containing request information.

    Returns:
    redirect - Django function to redirect user to another view (home).
    """
    logout(request)
    return redirect("home")


def register(request):
    """Account creation/registration view.

    If the request type is POST, register the user, login the user, and
    redirect them to the home page. Otherwise, display the user registration
    form.
    
    Arguments:
    request - Django object containing request information.

    Returns:
    redirect - Django function to redirect the user to another view (home).
    OR
    render - Django function to give a HTTP response with a template.
    """
    title = "Account Creation"

    # Check the request type.
    if request.method == "POST":
        # Create a form with the POST data.
        form = UserRegistrationForm(request.POST)

        # Check form validity.
        if form.is_valid():
            # Create user and relevant player.
            user = form.save()
            player = Player(user=user)
            player.save()

            # Log the user in.
            login(request, user)
            
            # Redirect to the home view.
            return redirect("home")
        else:
            # Form invalid, show generic error message.
            messages.warning(request, "Please correct the errors below!")

            # Iterate through list of errors to show specific problems.
            for field, message in form.errors.items():
                messages.warning(request, field + ": " + message[0])

    # Create an empty registration form and show it.
    form = UserRegistrationForm()
    return render(request, "game/register.html", {"form": form, "title": title})


def game(request):
    """Game view.

    If the request type is POST and the user is logged in, save the user score
    and redirect the user to the profile page. Otherwise, display the game.

    Arguments:
    request - Django object containing request information.

    Returns:
    redirect - Django function to redirect the user to another view (profile).
    OR
    render - Django function to give a HTTP response with a template.
    """
    title = "Game"

    # Check the request type.
    if request.method == "POST":
        # Check if the user is logged in.
        if request.user.is_authenticated:
            # Get the score, user and player.
            score = int(request.POST["score"])
            current_user = request.user
            current_player = Player.objects.get(user=current_user)

            # Increase the player score. 
            current_player.points += score
            current_player.save()

            # Redirect to the profile view.
            return redirect("profile")

    # Select a random event from the list of events and use that as the event
    # the user partipates in.
    event_list = Event.objects.all()
    event = choice(event_list)

    # Show the game.
    return render(request, "game/game.html", {"event": event, "title": title})


def list_events(request):
    """List events view.

    Shows a list of all events.

    Arguments:
    request - Django object containing request information.

    Returns:
    render - Django function to give a HTTP response with a template.
    """
    title = "List Events"

    # Get list of events ordered by the end datetime.
    events_list = Event.objects.order_by("end")

    return render(request, "game/list_events.html", {
        "title": title,
        "events_list": events_list,
        })


def event_details(request, event_id):
    """Event details view.

    Shows details relating to a specific event.

    Arguments:
    request - Django object containing request information.
    event_id (int) - ID of the event to show.

    Returns:
    render - Django function to give a HTTP response with a template.
    """
    # Get specific event.
    event = get_object_or_404(Event, pk=event_id)

    # Set title to include event title.
    title = "List Events: " + event.title

    return render(request, "game/event_details.html", {
        "title": title,
        "event": event,
        })


def create_event(request):
    """Event creation view.

    If the request type is POST, save the event and redirect the user to the
    create event view. Otherwise, display the event creation form.

    Arguments:
    request - Django object containing request information.

    Returns:
    redirect - Django function to redirect the user to another view (create
    event).
    OR
    render - Django function to give a HTTP response with a template.
    """
    title = "Create Event"

    # Check the request type.
    if request.method == "POST":
        # Create a form with the POST data.
        form = EventCreationForm(request.POST)

        # Check form validity.
        if form.is_valid():
            # Get fields from form.
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            start = form.cleaned_data.get("start")
            end = form.cleaned_data.get("end")
            latitude = form.cleaned_data.get("latitude")
            longitude = form.cleaned_data.get("longitude")

            # Create event with fields.
            event = Event(title=title, description=description,
                    start=start, end=end, latitude=latitude, longitude=longitude)
            event.save()

            # Show message of success to user.
            messages.success(request, "Event saved successfully!")

            # Redirect to the create event view.
            return redirect("create event")
        else:
            # Form invalid, show generic error message.
            messages.warning(request, "Please correct the errors below!")

            # Iterate through list of errors to show specific problems.
            for field, message in form.errors.items():
                messages.warning(request, field + ": " + message[0])

    # Create an empty event creation form and show it.
    form = EventCreationForm()
    return render(request, "game/create_event.html", {"form": form, "title": title})


def update_event(request, event_id):
    """Event update view.

    If the request type is POST, update the event and redirect the user to the
    events detail page. Otherwise, display the event creation form.

    Arguments:
    request - Django object containing request information.
    event_id (int) - ID of Event to update.

    Returns:
    redirect - Django function to redirect the user to another view (event
    details).
    OR
    render - Django function to give a HTTP response with a template.
    """
    # Get specific event. 
    event = get_object_or_404(Event, pk=event_id)

    # Set title to include event title.
    title = "Update Event: " + event.title 

    # Check the request type.
    if request.method == "POST":
        # Create a form with the POST data.
        form = EventCreationForm(request.POST)

        # Check form validity.
        if form.is_valid():
            # Get fields from the form and update the event.
            event.title = form.cleaned_data.get("title")
            event.description = form.cleaned_data.get("description")
            event.start = form.cleaned_data.get("start")
            event.end = form.cleaned_data.get("end")
            event.latitude = form.cleaned_data.get("latitude")
            event.longitude = form.cleaned_data.get("longitude")

            # Save the event.
            event.save()

            # Show message of success to user.
            messages.success(request, "Event updated successfully!")

            # Redirect back to details page.
            return redirect("event details", event_id=event_id)
        else:
            # Form invalid, show generic error message.
            messages.warning(request, "Please correct the errors below!")

            # Iterate through list of errors to show specific problems.
            for field, message in form.errors.items():
                messages.warning(request, field + ": " + message[0])

    # Create a populated event creation form and show it.
    form = EventCreationForm(initial={
        "title": event.title,
        "description": event.description,
        "start": event.start,
        "end": event.end,
        "latitude": event.latitude,
        "longitude": event.longitude,
        })
    return render(request, "game/update_event.html", {
        "title": title,
        "form": form,
        "event": event})

def delete_event(request, event_id):
    """Event deletion view.

    Delete the event specified by the event ID and redirect the user to the
    events list.

    Arguments:
    request - Django object containing request information.
    event_id (int) - ID of Event to delete.

    Returns:
    redirect - Django function to redirect the user to another view (list
    events).
    """
    # Delete the object.
    Event.objects.filter(pk=event_id).delete()

    # Display message informing the user object has been deleted.
    messages.success(request, "Event " + str(event_id) + " deleted!")

    # Redirect back to event list page.
    return redirect("list events")

def profile(request):
    """User profile view.

    Display the user.

    Arguments:
    request - Django object containing request information.

    Returns:
    render - Django function to give a HTTP response with a template.
    """
    title = "Profile"
    return render(request, "game/profile.html", {"title": title})


def leaderboard(request):
    """Leaderboard view.

    Display the top 10 players by total score.

    Arguments:
    request - Django object containing request information.

    Returns:
    render - Django function to give a HTTP response with a template.
    """
    title = "Leaderboard"

    top_players_list = Player.objects.order_by("-points")[:10]
    return render(request, "game/leaderboard.html",
            {"top_players_list": top_players_list, "title": title})
