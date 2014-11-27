__author__ = 'Niklas Aronsson'

import logging
from django.core.management.base import BaseCommand, CommandError
from django.template import loader, Context, Template
from django.core.mail import EmailMessage
from django.core import mail
from sportApp.models import Player
import sportApp.model_queries as mq

logging.basicConfig(format='%(name)s:%(levelname)s:%(lineno)s:%(message)s', level=logging.INFO)
logger = logging.getLogger('SendEmailCommand')

APP_URL = "http://integration.ld.sw.ericsson.se/TableApp/"


class Command(BaseCommand):
    help = "Sends an email with the upcoming games for each player."

    def handle(self, *args, **options):
        emails_to_send = []
        for player in Player.objects.filter(active=True):
            if player.email:
                games_to_play = mq.get_todays_games_for_player(player.id)
                if games_to_play:
                    logger.info(u"Player {0} have {1} games to play.".format(player.name, len(games_to_play)))
                    mail_template = loader.get_template('upcoming_games_email_template.html')
                    context = Context({'unplayed_games': games_to_play,
                                       'player': player,
                                       'app_url': APP_URL})
                    rendered = mail_template.render(context)
                    this_mail = EmailMessage(u"Table Hockey League: Today's Matches for {0}".format(player.name),
                                             rendered,
                                             "hockey_admin@noreply.com", [player.email])
                    this_mail.content_subtype = "html"  # Main content is now text/html
                    emails_to_send.append(this_mail)
                    #print rendered
                else:
                    logger.info(u"Player {0} have no games to play.".format(player.name))
                    continue
            else:
                logger.info(u"No email saved for: {0}".format(player.name))
        logger.info("Send emails!")
        connection = mail.get_connection()
        connection.send_messages(emails_to_send)
        logger.info("Emails sent!")