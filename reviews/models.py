import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# Create your models here.
# django-admin startproject mysite
# python manage.py startapp polls
# Edit model ####
# python manage.py makemigrations reviews
# python manage.py sqlmigrate reviews 0001
# python manage.py check
# python manage.py migrate
# python manage.py createsuperuser
# python manage.py runserver 80


class ReviewStatus(models.Model):
    name = models.CharField(max_length=16)
    status = models.ForeignKey("ReviewStatus", on_delete=models.CASCADE, related_name='reviewstatus_to_reviewstatus_status_fk')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewstatus_to_user_created_by_fk')
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewstatus_to_user_changed_by_fk')
    created_at = models.DateTimeField('date created')
    changed_at = models.DateTimeField('date changed')

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.CharField(max_length=512)
    plus_votes = models.IntegerField(default=0)
    minus_votes = models.IntegerField(default=0)
    status = models.ForeignKey(ReviewStatus, on_delete=models.CASCADE, related_name='review_to_reviewstatus_status_fk')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_to_user_created_by_fk')
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_to_user_changed_by_fk')
    created_at = models.DateTimeField('date created')
    changed_at = models.DateTimeField('date changed')

    def __str__(self):
        return ("Id: %s. Text: %s. Created by: %s. Changed by: %s") % (self.id, self.text[:10], self.created_by.username, self.changed_by.username)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

#    def was_published_recently(self):
#        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text