from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Post(models.Model):
	body = models.TextField()
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	created_on = models.DateTimeField(default = timezone.now)
	history = HistoricalRecords()

class Comment(models.Model):
	body = models.TextField()
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	post = models.ForeignKey('Post',on_delete = models.CASCADE)
	created_on = models.DateTimeField(default = timezone.now)

# class Version(models.Model):
# 	post = models.ForeignKey(Post, on_delete = models.CASCADE)
# 	text = models.TextField()
# 	created = models.DateTimeField(default = timezone.now)

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True, verbose_name='user',related_name = 'profile',on_delete=models.CASCADE)
	bio = models.CharField(max_length = 100, null=True)
	dp = models.ImageField(default = 'profile_images/default.jpg', upload_to = 'profile_images/%Y-%m-%d')
	name = models.CharField(max_length = 30, null=True)
	followers = models.ManyToManyField(User, blank = True, related_name = 'following')
	mail_followers = models.ManyToManyField(User, blank = True, related_name = 'mail_following')

from django.db.models.signals import post_save #Import a post_save signal when a user is created
#from django.contrib.auth.models import User # Import the built-in User model, which is a sender
from django.dispatch import receiver # Import the receiver
#from .models import Profile


@receiver(post_save, sender=User) 
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# def get_username(self):
#     return self.username

# User.add_to_class("__repr__", get_username)
