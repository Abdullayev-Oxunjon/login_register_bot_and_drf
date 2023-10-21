from django.contrib import admin

from app.models import User, Person, Group

admin.site.register(
    [User,
     Person,
     Group]
)
