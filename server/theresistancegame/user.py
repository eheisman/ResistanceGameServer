"""Defines a user"""
from google.appengine.ext import db
from google.appengine.api import users

import re

allowedset = "[0-9A-Za-z.-_]"
deniedset = "[^0-9A-Za-z.-_]"

class User(db.Model):
    userkey = db.StringProperty(verbose_name="Encryption Key", required=True)
    googleacct = db.UserProperty(verbose_name="Google Account", required=True, auto_current_user_add=True)
    uname = db.StringProperty(verbose_name="In-game name", required=True)
    """Three to 16 character string.  Character set: [0-9A-Za-z.-_]"""

#TODO: Write function to validate userkey as a sha512sum
#TODO: Write a function to validate uname
