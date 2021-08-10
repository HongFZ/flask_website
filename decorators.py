#encoding: utf-8
from flask import session,redirect,url_for
from functools import wraps
import config

def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.TEACHER_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return inner