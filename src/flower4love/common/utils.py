# coding=utf-8

import time
import MySQLdb
from datetime import date, datetime
from django.core.mail import EmailMessage
from django.conf import settings


def get_client_ip(req_meta):
    x_forwarded_for = req_meta.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = req_meta.get('REMOTE_ADDR')
    return ip


def is_in_same_day(argtime, fixed_point=0):
    """
    判断argtime和当前时间是否是否在同一天内

    @return : True or False
    """
    # now = int(time.time())
    #argtime = int(argtime)
    if int(time.time()) - int(argtime) >= 3600 * 24:
        return False
    argtime = datetime.fromtimestamp(int(argtime))
    now = datetime.now()
    if now.day == argtime.day:
        return not (fixed_point > argtime.hour and fixed_point <= now.hour)
    else:
        if argtime.hour < fixed_point:
            return False
        return fixed_point > now.hour


def is_in_same_week(argtime, must_whole_week=False):
    argtime = datetime.fromtimestamp(int(argtime))
    now = datetime.now()
    if (now - argtime).total_seconds() > 7 * 86400 or now.year != argtime.year:
        return False
    if must_whole_week:
        if (now - argtime).total_seconds() > 7 * 86400:
            return False
        else:
            return True
    argtime_weeknum = date(argtime.year, argtime.month, argtime.day).isocalendar()[1]
    now_weeknum = date(now.year, now.month, now.day).isocalendar()[1]
    if argtime_weeknum != now_weeknum:
        return False
    return True

def send_mail(to_mail_list, subject, body, attach_file_path=None):
    sender = settings.EMAIL_HOST_USER
    print '===================start to send mail to ', to_mail_list
    mail_message = EmailMessage(subject=subject,
                                body = body,
                                from_email=sender,
                                to=to_mail_list,
                                #headers={'Reply-to':'another@example.com'}
                                )
    if attach_file_path:
        mail_message.attach_file(attach_file_path)
    mail_message.send()
    print '===================send mail done'

def create_connection(dbinfo):
    try:
        conn = MySQLdb.connect(
            host=dbinfo['HOST'],
            user=dbinfo['USER'],
            passwd=dbinfo['PASSWORD'],
            db=dbinfo['NAME'],
            port=3306,
            charset='utf8',
        )
        executer = conn.cursor()
        return executer
    except:
        print 'create connection error'
        return None