from slacker import Slacker
import slackbot_settings
from bottle import *
from database import *
import datetime
import json
import threading
import time

slack = Slacker(slackbot_settings.API_TOKEN)


def message(mes, channel="remind_bot"):
    slack.chat.post_message(channel, mes, as_user=True)


class PerHalfHour(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True


    def run(self):
        print("check")
        while self.running:
            for s in Schedule.select().where(Schedule.date < (datetime.datetime.now() + datetime.timedelta(hours=2))):
                message(s.message)
                if s.date < datetime.datetime.now():
                    s.delete_instance()
            time.sleep(60 * 30)

    def kill(self):
        self.running = False


def is_unique(schedule_model_instance):
    return not Schedule.select().where(
            (Schedule.date == schedule_model_instance.date) &
            (Schedule.message == schedule_model_instance.message)).exists()


@post("/schedule")
def schedule():
    schedule = request.params.schedule
    date_format = request.params.date_format
    message = request.params.message or "remind"
    date = datetime.datetime.strptime(schedule, date_format)
    if date <= datetime.datetime.now():
        return "0"
    try:
        s = Schedule(date=date, message=message)
        if is_unique(s):
            s.save()
            print(message)
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


per_half_hour = PerHalfHour()
per_half_hour.start()
run(host="0.0.0.0", port=8080)
per_half_hour.kill()
