from django.contrib import admin

from .models import Player, Event, Participation


admin.site.register(Player)
admin.site.register(Event)
admin.site.register(Participation)
