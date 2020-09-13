from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	followers = models.ManyToManyField("User", related_name="following_persons")
	following = models.ManyToManyField("User", related_name="followers_persons")
	liked = models.ManyToManyField("Post", related_name="liked_posts")
	pass
	
	def serialize(self):
		return {
            "id": self.id,
            "followers": [user.username for user in self.followers.all()],
            "following": [user.username for user in self.following.all()],
			"liked": [post.id for post in self.liked.all()]
        }

		
	
class Post(models.Model):
	author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
	text = models.TextField(blank=True)
	counter = models.IntegerField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def serialize(self):
		return {
            "id": self.id,
            "author": self.author.username,
            "text": self.text,
            "counter": self.counter,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }