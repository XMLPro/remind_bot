from slacker import Slacker
import slackbot_settings

slack = Slacker(slackbot_settings.API_TOKEN)


def message(mes, channel="remind_bot"):
    slack.chat.post_message(channel, mes, as_user=True)
