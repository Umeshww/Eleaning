from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

# Register your models here.
admin.site.register(admindata)
admin.site.register(logindata)
admin.site.register(studentdata)
admin.site.register(coursedata)
admin.site.register(paydata)
admin.site.register(videodata)
admin.site.register(upidata)
admin.site.register(notesdata)



