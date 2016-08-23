import os
from slacker import Slacker

SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#aws')


def notify(daily_file, weekly_file, stop_time):
    slack = Slacker(SLACK_API_TOKEN)
    slack.files.upload(
        daily_file, channels=[SLACK_CHANNEL],
        title='Daily AWS Spot Price ending on {}'.format(stop_time)
    )
    slack.files.upload(
        weekly_file, channels=[SLACK_CHANNEL],
        title='Weekly AWS Spot Price ending on {}'.format(stop_time)
    )
    slack.chat.post_message('#aws', 'AWS Spot prices ending on {} are available'.format(stop_time),
                            username='AWS Bot')
