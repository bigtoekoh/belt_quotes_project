from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime


class UserManager(models.Manager):
    def login_validator(self, postData):
        response = {
            'status' : True,
            'errors' : []
            }
        try:
            user = self.get(email = postData["email"])
        except:
            user = None
        if not user:
            response["errors"].append("Email is not registered.")
        if user:
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                response["errors"].append("Password does not match registered email.")
        if len(response["errors"]) == 0:
            response["user"] = user
            return response
        response["status"] = False
        return response
    def registration_validator(self, postData):
        response = {
            'status' : True,
            'errors' : []
            }

        if not len(postData['bday']) or postData["bday"] > str(datetime.datetime.today()):
            response["errors"].append("Not a valid date of birth.")
        if len(postData["name"]) < 2:
            response["errors"].append("Name must be at least two characters.")
        if len(postData["alias"]) < 2:
            response["errors"].append("Alias must be at least two characters.")
        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            response["errors"].append("Email is not valid.")
        if len(postData["password"]) < 8:
            response["errors"].append("Password must be at least 8 characters.")
        if postData["password"] != postData["c_password"]:
            response["errors"].append("Passwords do not match.")
        emailObject = self.filter(email = postData["email"])
        if len(emailObject) > 0:
            response["errors"].append("Email already exists.")
        if len(response["errors"]) == 0:
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(12))
            user = self.create(name = postData["name"], alias = postData["alias"], email = postData["email"], password = hashed, dob = postData["bday"], count = 0)
            response["user"] = user
            return response
        response["status"] = False
        return response

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField(default=datetime.date(2000,1,1))
    count = models.IntegerField()
    objects = UserManager()
