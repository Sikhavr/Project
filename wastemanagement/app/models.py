from django.db import models

class usersignup(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class driversignup(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


class dustbin(models.Model):
    place=models.CharField(max_length=50)
    location=models.CharField(max_length=50)

class dailywaste(models.Model):
    place=models.CharField(max_length=50)
    route=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    plastic_waste=models.CharField(max_length=50)
    food_waste=models.CharField(max_length=50)

class complaint_register(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    place=models.CharField(max_length=50)
    date=models.DateTimeField()
    complaint=models.CharField(max_length=200)

class DriverMessage(models.Model):
    driver = models.ForeignKey(driversignup, on_delete=models.CASCADE)
    complaint = models.ForeignKey(complaint_register, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Complaint(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField()
    place = models.CharField(max_length=50)
    status = models.CharField(max_length=20)

# Create your models here.
