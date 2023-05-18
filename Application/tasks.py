from Application.worker import celery
from Application.models import User, Post
from datetime import datetime
from jinja2 import Template
from celery.schedules import crontab
from Application.mail_sent import send_email,main

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=7, minute=30, day_of_week=1), monthly_reminder.s() )
    sender.add_periodic_task(10.0, daily_reminder.s())


@celery.task()
def daily_reminder():
    all_user=User.query.all()
    print(all_user)
    for user in all_user:
            print(user)
            with open("mail.html", 'r') as h:
                tempe=Template(h.read())
                send_email(user.email, subject="Daily Reminder",message=tempe.render(user=user),)
    


    return "yes"

@celery.task()
def monthly_reminder():
    alluser=User.query.all()
    for user in alluser:
        p=[]
        post = Post.query.filter(post.user_id == user.user_id).all()
        p.append(post)
        n=len(p)
        if n < 3:
             
            with open("month.html", 'r') as h:
                temp=Template(h.read())
                send_email(user.email, subject="Monthly Reminder",message=temp.render(length = n,user = user),)
             

    return "yes"
