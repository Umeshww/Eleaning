from django.db import models

# Create your models here.
class logindata(models.Model):
    email = models.EmailField(max_length=100,primary_key=True)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)
    def __str__(self):
        return self.email

class admindata(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    email = models.EmailField(max_length=100,primary_key=True)
    contact = models.TextField(max_length=100)
    def __str__(self):
        return self.email
class studentdata(models.Model):
    name = models.CharField(max_length=100)
    contact = models.TextField(max_length=100)
    email = models.EmailField(max_length=100,primary_key=True)
    phone = models.TextField(max_length=100)
    address = models.TextField(max_length=100)
    gender = models.TextField(max_length=100)
    def __str__(self):
        return self.email

class coursedata(models.Model):
    course_id = models.IntegerField(auto_created=0,primary_key=True)
    coursename = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()
    video_file = models.FileField(upload_to='videos/')
    pic = models.FileField(upload_to='images/')
    details = models.TextField()
    def __str__(self):
        return self.coursename

class paydata(models.Model):
    id = models.IntegerField(auto_created=0,primary_key=True)
    course_id = models.IntegerField()
    course_name = models.CharField(max_length=100)
    student_email = models.EmailField(max_length=100)
    utr = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    dates = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.student_email} - {self.course_id}"

class videodata(models.Model):
    id = models.IntegerField(auto_created=0,primary_key=True)
    course_id = models.IntegerField()
    video_file = models.FileField(upload_to='videos/')
    thum = models.FileField(upload_to='images/')
    topic = models.CharField(max_length=100)
    def __int__(self):
        return self.course_id

class upidata(models.Model):
    upi = models.CharField(max_length=100)
    upi_name = models.CharField(max_length=100)
    def __str__(self):
        return self.upi_name

class notesdata(models.Model):
    id = models.IntegerField(auto_created=0,primary_key=True)
    course_id = models.IntegerField()
    note_file = models.FileField(upload_to='notes/')
    title = models.CharField(max_length=100)
    def __int__(self):
        return self.course_id