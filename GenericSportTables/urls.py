from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'sportApp.views.home', name='home'),
    url(r'^rankings/$', 'sportApp.views.rankings', name='rankings'),
    url(r'^show_tournament_data/(?P<tournament_id>\d.*?)/(?P<division_id>\d.*?)/$',
        'sportApp.views.show_tournament_data',
        name='show_tournament_data'),
    url(r'^edit_match_data/(?P<match_id>\d.*?)/(?P<tournament_id>\d.*?)/(?P<division_id>\d.*?)/$',
        'sportApp.views.edit_match_data',
        name='edit_match_data'),
    url(r'^register_player/$', 'sportApp.views.register_player', name='register_player'),
    url(r'^active_players/$', 'sportApp.views.active_players', name='active_players'),
    url(r'^new_tournament/$', 'sportApp.views.new_tournament', name='new_tournament'),
    url(r'^tournaments/$', 'sportApp.views.tournaments', name='tournaments'),
    url(r'^generate_games/(?P<tournament_id>\d.*?)/$', 'sportApp.views.generate_games', name='generate_games'),
    url(r'^upload_player_list/$', 'sportApp.views.upload_player_list', name='upload_player_list'),
    url(r'^randomize_players/$', 'sportApp.views.randomize_players', name='randomize_players'),
    url(r'^generate_divisions/$', 'sportApp.views.generate_divisions', name='generate_divisions'),
    url(r'^show_default_player/$', 'sportApp.views.show_default_player', name='show_default_player'),
    url(r'^log_in$', 'sportApp.views.log_in', name='log_in'),
    url(r'^log_out', 'sportApp.views.log_out', name='log_out'),
    url(r'^show_player_data/(?P<player_id>\d.*?)$', 'sportApp.views.show_player_data', name='show_player_data'),
    url(r'^make_player_default/(?P<player_id>\d.*?)$', 'sportApp.views.make_player_default', name='make_player_default'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
