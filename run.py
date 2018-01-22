from slacker import Slacker
import slackbot_settings
from bottle import *
from database import *
import datetime
import json

slack = Slacker(slackbot_settings.API_TOKEN)


def message(mes, channel="remind_bot"):
    slack.chat.post_message(channel, mes, as_user=True)


def is_unique(schedule_model_instance):
    return not Schedule.select().where(
            (Schedule.date == schedule_model_instance.date) &
            (Schedule.message == schedule_model_instance.message)).exists()


@post("/schedule")
def schedule():
    schedule = request.params.schedule
    date_format = request.params.date_format
    message = request.params.message or "remind"
    print(message)
    date = datetime.datetime.strptime(schedule, date_format)
    try:
        s = Schedule(date=date, message=message)
        if is_unique(s):
            s.save()
            return "1"
    except Exception as e:
        print(e)
    return "0"


@post("/schedule/delete")
def delete_schedule():
    try:
        for s in Schedule.select():
            s.delete_instance()
        return "1"
    except Exception as e:
        print(e)
        return "0"


@get("/schedule/list")
def schedule_list():
    date_format = "%Y/%m/%d %H:%M"
    data = []
    for s in Schedule.select():
        data.append({
            "date_format": date_format,
            "schedule": s.date.strftime(date_format),
            "created_at": s.created_at.strftime(date_format),
            "message": s.message,
            })
    return json.dumps(data)


run(host="0.0.0.0", port=8080)
