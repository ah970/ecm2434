"""Models used in game app.

Used for creating and storing persistent structured data in the database.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Player(models.Model):
    """Player model.

    Extends the user model, used to contain game specific information.

    Model attributes:
    user - Actual user that is related to this Player.
    points - Total number of points score.
    is_game_master - Flag to check if this Player is a game master.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    is_game_master = models.BooleanField(default=False)


class Event(models.Model):
    """Event model.

    Used for containing locations, start/end times and other information. The
    precision for location data is based on maximum possible precision
    available from Google Maps.

    Model attributes:
    title - Name of Event.
    description - Description of Event.
    start - Datetime of start of Event.
    end - Datetime of end of Event.
    latitude - Latitude of Event location.
    longitude - Longitude of Event location.
    """
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)

    def get_status(self):
        """Return a string status of the event.

        The status has one of 3 values:
        "Live" - the event is currently active.
        "Past" - the event happened in the past.
        "Future" - the event will occur in the future.
    
        Arugments:
        self - Event object.
    
        Returns:
        status (str) - status of Event.
        """
        # Get the current date and time.
        current_datetime = timezone.now()

        # Current date is before the start of the Event.
        if current_datetime < self.start:
            return "Future"
        # Current date between start and end of the Event.
        elif self.start <= current_datetime <= self.end:
            return "Live"
        else:
            return "Past"


class Participation(models.Model):
    """Participation model

    Used for matching Players to Events with a score.

    Model attributes:
    player - Player related to this Participation.
    event - Event
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
