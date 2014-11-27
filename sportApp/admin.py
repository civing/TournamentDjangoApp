from django.contrib import admin
from sportApp.models import Player, Game, Division, Tournament


def delete_tournament_games(modeladmin, request, queryset):
    for obj in queryset:
        for g in obj.games.all():
            g.delete()
delete_tournament_games.short_description = "Delete associated games."


def delete_tournament_and_games(modeladmin, request, queryset):
    for obj in queryset:
        for g in obj.games.all():
            g.delete()
        obj.delete()
delete_tournament_and_games.short_description = "Delete tournament and all associated games."


class TournamentAdmin(admin.ModelAdmin):
        list_display = ['name', 'start_date', 'end_date', 'active']
        actions = [delete_tournament_games, delete_tournament_and_games]

admin.site.register(Player)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Division)
admin.site.register(Game)