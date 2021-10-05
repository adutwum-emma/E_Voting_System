from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta

class Election(models.Model):

    election_name = models.CharField(max_length=50)
    electoral_commission = models.ForeignKey(User, on_delete=models.CASCADE)
    time_to_start = models.DateTimeField()
    time_to_end = models.DateTimeField()
    has_started = models.BooleanField(default=False)
    has_closed = models.BooleanField(default=False)
    real_time_started = models.DateTimeField(auto_now_add=True)
    real_time_ended = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        
        return self.election_name + " " + str(self.time_to_start)
    
    class Meta:

        verbose_name_plural = "Elections"
        ordering = ["election_name", "time_to_start"]
    
    @property

    def time_remaining(self):
        
        time_remaining = self.time_to_end - self.time_to_start

        return time_remaining

class Category(models.Model):

    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50)

    def __str__(self):
        
        return self.category_name
    
    class Meta:

        verbose_name_plural = "Categories"
        ordering = ["category_name"]

class Candidate(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=1)
    profile_pic = models.ImageField(upload_to="Candidate_Pics")

    def __str__(self):

        return self.first_name + " " + self.last_name

    class Meta:

        ordering = ["category"]
        verbose_name_plural = "Candidates"

class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    time_voted = models.DateTimeField(auto_now=True)


    def __str__(self):

        return str(self.time_voted)
    
    class Meta:
        ordering = ["category"]
        verbose_name_plural = "Votes"
    
    @property

    def percentage(total, individual_count):

        operation = (self.candidate.count/total) * 100

        return operation

class Voter(models.Model):

    user_name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1)
    email = models.EmailField()
    dob = models.DateField()
    has_voted = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)

    def __str__(self):

        return self.user_name + " " + self.first_name
    
    class Meta:

        verbose_name_plural = "Voters"
        ordering = ["user_name", "first_name", "last_name"]
    
    @property

    def age(self):
        my_date = date.today()
        the_days = my_date - self.dob
        age = int(the_days.days / 365)

        return age


class Current_Election(models.Model):

    election = models.OneToOneField(Election, on_delete=models.CASCADE)


    def __str__(self):

        return str(self.id)
    
    @property
    def the_id(self):

        return str(self.election.id)