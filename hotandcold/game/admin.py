"""Administration dashboard configuration for game app.

Adds models to admin dashboard.
"""

from django.contrib import admin

from .models import Player, Event, Participation, TreasureChest


# Add Player, Event and Participation models to the admin dashboard.
admin.site.register(Player)
admin.site.register(Event)
admin.site.register(Participation)
admin.site.register(TreasureChest)
