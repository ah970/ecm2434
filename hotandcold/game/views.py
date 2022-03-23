"""Views used in game app.

Handles actual functionality of different views.
"""

from random import choice

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from .models import Event, Player, Participation, TreasureChest
from .forms import UserRegistrationForm, UserUpdateEmailForm, EventCreationForm, TreasureChestCreationForm


def home(request):
    """Home view.

    Display the home page.

    Arguments:
    request - Django object containing request information.

    Returns:
    render - Django function to give a HTTP response with a template.
    """
    return render(request, "game/home.html", None)


def game_list(request):
    """Game list view.

    Shows a list of live games to play.

    Arguments:
    request - Django object containing request information.

    Returns:
    render - Django function to give a HTTP response with a template.
    """
    # Set the title.
    title = "Game List"

    # Get current datetime and list of events which are live.
    current_datetime = timezone.now()
    live_events_list = Event.objects.filter(start__lte=current_datetime,
            end__gte=current_datetime)

    return render(request, "game/game_list.html", {"title": title,
        "live_events_list": live_events_list})


def game(request, event_id):
    """Game view.

    If the request type is POST and the user is logged in, save the user score
    and redirect the user to the profile page. Otherwise, display the game.

    Arguments:
    request - Django object containing request information.
    event_id - ID of event to use.

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
            # Get the score, event, user and player.
            score = int(request.POST["score"])
            event = get_object_or_404(Event, pk=event_id)
            player = Player.objects.get(user=request.user)

            # Increase the player score. 
            player.points += score
            player.save()

            # Create participation.
            participation = Participation(event=event, player=player, score=score)
            participation.save()

            # Redirect to the profile view.
            return redirect("profile")

    # Get event and check if event is live.
    event = get_object_or_404(Event, pk=event_id)
    if not event.get_status() == "Live":
        # Event is not live, do not allow user to go further.
        raise PermissionDenied

    # Show the game.
    return render(request, "game/game.html", {"event": event, "title": title})


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
            # Show error messages.
            display_error_messages(request, form)

    # Create an empty registration form and show it.
    form = UserRegistrationForm()
    return render(request, "game/register.html", {"form": form, "title": title})


def user_details(request, username):
    """User details view.

    Show information about a specific user (given by username). Similar to the
    user profile view but does not include links to change details.

    Arguments:
    request - Django object containing request information.
    username (str) - username of user to view.

    Returns:
    render - Django function to give a HTTP response with a template.
    """
    # Check if user is logged in.
    if not request.user.is_authenticated:
        # User is not logged in, show HTTP 403.
        raise PermissionDenied

    # Get user by username.
    user = get_object_or_404(User, username=username)

    # Set title to include username.
    title = "Profile: " + username

    return render(request, "game/user.html", {"title": title, "show_user": user})


def update_user_email(request):
    """Update user view.

    If the request type is POST and the user is logged in, update the users
    email based on the form data and redirect back to the user profile view.
    Otherwise, display the user update email form.

    Arguments:
    request - Django object containing request information.

    Returns:
    redirect - Django function to redirect the user to another view (profile).
    OR
    render - Django function to give a HTTP response with a template.
    """
    # Check if user is logged in.
    if not request.user.is_authenticated:
        # User is not logged in, show HTTP 403.
        raise PermissionDenied

    # Set title.
    title = "Update Email"

    # Check the request type.
    if request.method == "POST":
        # Create a form with the POST data and the logged in user.
        form = UserUpdateEmailForm(request.POST)

        # Check form validity.
        if form.is_valid():
            # Get user and email.
            user = request.user
            email = form.cleaned_data.get("email")
            
            # Save the new user details.
            user.email = email
            user.save()

            # Show message of success to user.
            messages.success(request, "User email updated successfully!")

            # Redirect to the profile view.
            return redirect("user", username=user.username)
        else:
            # Show error messages.
            display_error_messages(request, form)

    # Create an empty update form and show it.
    form = UserUpdateEmailForm()
    return render(request, "game/update_user.html", {"title": title, "form": form})


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
    redirect - Django function to redirect the user to another view (list
    events).
    OR
    render - Django function to give a HTTP response with a template.
    """
    # Check if the user is a game master.
    check_user_is_game_master(request)

    # Set the title.
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

            # Redirect to the list events view.
            return redirect("list events")
        else:
            # Show error messages.
            display_error_messages(request, form)


    # Create an empty event creation form and show it.
    form = EventCreationForm()
    return render(request, "game/modify_object.html", {
        "form": form,
        "title": title,
        "modification": "Create",
        "object_type": "Event"})


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
    # Check if the user is a game master.
    check_user_is_game_master(request)

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
            # Show error messages.
            display_error_messages(request, form)

    # Create a populated event creation form and show it.
    form = EventCreationForm(initial={
        "title": event.title,
        "description": event.description,
        "start": event.start,
        "end": event.end,
        "latitude": event.latitude,
        "longitude": event.longitude,
        })
    return render(request, "game/modify_object.html", {
        "title": title,
        "form": form,
        "object": event,
        "modification": "Update",
        "object_type": "Event"})


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
    # Check if the user is a game master.
    check_user_is_game_master(request)

    # Delete the object.
    Event.objects.filter(pk=event_id).delete()

    # Display message informing the user object has been deleted.
    messages.success(request, "Event " + str(event_id) + " deleted!")

    # Redirect back to event list page.
    return redirect("list events")


def list_treasure_chests(request):
    """TreasureChest list view.

    Shows a list of all treasure chests.

    Arguments:
    request - Django object containing request information.

    Returns:
    render - Django function to give a HTTP response with a template.
    """
    # Check if the user is a game master.
    check_user_is_game_master(request)

    # Set title.
    title = "List Treasure Chests"

    # Get list of treasure chests.
    treasure_chests_list = TreasureChest.objects.all()

    return render(request, "game/list_treasure_chests.html", {
        "title": title,
        "treasure_chests_list": treasure_chests_list,
        })


def treasure_chest_details(request, treasure_chest_id):
    """Treasure chest details view.

    Shows details relating to a specific treasure chest.

    Arguments:
    request - Django object containing request information.
    treasure_chest_id (int) - ID of the treasure chest to show.
    """
    # Check if the user is a game master.
    check_user_is_game_master(request)

    # Get specific treasure chest.
    treasure_chest = get_object_or_404(TreasureChest, pk=treasure_chest_id)

    # Set title to include treasure chest name.
    title = "List Treasure Chests: " + treasure_chest.name

    return render(request, "game/treasure_chest_details.html", {
        "title": title,
        "treasure_chest": treasure_chest,
        })


def create_treasure_chest(request):
    """Treasure chest creation view.
    
    If the request type is POST, create the treasure chest and redirect the
    user to the treasure chest list view. Otherwise, display the treasure
    chest creation form.

    Arguments:
    request - Django object containing request information.

    Returns:
    redirect - Django function to redirect the user to another view (list
    treasure chests).
    OR
    render - Django function to give a HTTP response with a template.
    """
    # Check if the user is a game master.
    check_user_is_game_master(request)

    # Set title.
    title = "Create Treasure Chest"

    # Check the request type.
    if request.method == "POST":
        # Create a form with the POST data.
        form = TreasureChestCreationForm(request.POST)

        # Check form validity.
        if form.is_valid():
            # Get fields from form.
            name = form.cleaned_data.get("name")
            points = form.cleaned_data.get("points")
            latitude = form.cleaned_data.get("latitude")
            longitude = form.cleaned_data.get("longitude")

            # Create treasure chest with fields.
            treasure_chest = TreasureChest(name=name, points=points,
                    latitude=latitude, longitude=longitude)
            treasure_chest.save()

            # Show message of success to user.
            messages.success(request, "Treasure chest created successfully!")

            # Redirect to the list treasure chests view.
            return redirect("list treasure chests")
        else:
            # Show error messages.
            display_error_messages(request, form)

    # Create an empty treasure chest creation form and show it. 
    form = TreasureChestCreationForm()
    return render(request, "game/modify_object.html", {
        "title": title,
        "form": form,
        "modification": "Create",
        "object_type": "Treasure Chest",
        })


def update_treasure_chest(request, treasure_chest_id):
    """Treasure chest update view.

    If the request type is POST, update the treasure chest and redirect the
    user to the treasure chest details page. Otherwise, display the treasure
    chest creation form.

    Arguments:
    request - Django object containing request information.
    treasure_chest_id (int) - ID of treasure chest to update.

    Returns:
    redirect - Django function to redirect the user to another view (treasure
    chest details).
    OR
    render - Django function to give a HTTP response with a template.
    """
    # Check if the user is a game master.
    check_user_is_game_master(request)

    # Get specific treasure chest.
    treasure_chest = get_object_or_404(TreasureChest, pk=treasure_chest_id)

    # Set title to include treasure chest name.
    title = "Update Treasure Chest: " + treasure_chest.name

    # Check the request type.
    if request.method == "POST":
        # Create a form with the POST data.
        form = TreasureChestCreationForm(request.POST)

        # Check form validity.
        if form.is_valid():
            # Get fields from the form and update the treasure chest.
            treasure_chest.name = form.cleaned_data.get("name")
            treasure_chest.points = form.cleaned_data.get("points")
            treasure_chest.latitude = form.cleaned_data.get("latitude")
            treasure_chest.longitude = form.cleaned_data.get("longitude")

            # Save the treasure chest.
            treasure_chest.save()

            # Show message of success to user.
            messages.success(request, "Treasure Chest updated successfully!")
            
            # Redirect back to details page.
            return redirect("treasure chest details", treasure_chest_id=treasure_chest_id)
        else:
            # Show error messages.
            display_error_messages(request, form)

    # Create a populated treasure chest creation form and show it.
    form = TreasureChestCreationForm(initial={
        "name": treasure_chest.name,
        "points": treasure_chest.points,
        "latitude": treasure_chest.latitude,
        "longitude": treasure_chest.longitude,
        })
    return render(request, "game/update_treasure_chest.html", {
        "title": title,
        "form": form,
        "object": treasure_chest,
        "modification": "Update",
        "object_type": "Treasure Chest"})


def delete_treasure_chest(request, treasure_chest_id):
    """Treasure chest deletion view.

    Delete the treasure specified by the treasure chest ID and redirect the
    user to the treasure chest list.

    Arguments:
    request - Django object containing request information.
    treasure_chest_id -  ID of treasure chest to delete.

    Returns:
    redirect - Django function to redirect the user to another view (list
    treasure chests).
    """
    # Check if the user is a game master.
    check_user_is_game_master(request)

    # Delete the treasure chest.
    TreasureChest.objects.filter(pk=treasure_chest_id).delete()

    # Display message informing the user object has been deleted.
    messages.success(request, "Treasure Chest " + str(treasure_chest_id) + " deleted!")
    
    # Redirect the user back to the treasure chest list page.
    return redirect("list treasure chests")


def check_user_is_game_master(request):
    """Check the privileges of the user.

    Checks the user is authenticated and they are a game master. If they are
    not, then send a HTTP 403 response.

    Arguments:
    request - Django object containing request information.

    Returns:
    None.
    """
    if not request.user.is_authenticated:
        raise PermissionDenied

    if not request.user.player.is_game_master:
        raise PermissionDenied


def display_error_messages(request, form):
    """Display error messages from forms.

    Iterates through all the errors in a form and displays each of them as a
    new message.

    Arguments:
    request - Django object containing request information.
    form - Django form to get errors from.

    Returns:
    None.
    """
    # Form invalid, show generic error message.
    messages.warning(request, "Please correct the errors below!")

    # Iterate through list of errors to show specific problems.
    for field, message in form.errors.items():
        messages.warning(request, field + ": " + message[0])
