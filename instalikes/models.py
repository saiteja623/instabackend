from django.db import models
from django.contrib.auth.models import User, AbstractUser
from PIL import Image

# Create your models here.


class date(models.Model):
    title = models.CharField(max_length=225, default=" ")
    time = models.DateTimeField(auto_now_add=True)


class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=225, default="")
    desc = models.TextField(blank=True)
    image = models.ImageField(default="default.png")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.width > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class customUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("customUser", blank=True)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        customUser, related_name="from_user", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        customUser, related_name="to_user", on_delete=models.CASCADE
    )


class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    figcaption = models.CharField(max_length=225, default="")
    likes = models.IntegerField(max_length=1000, default=0)
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=225, null=True)


class likedby(models.Model):
    image = models.ForeignKey(post, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)


class commentsby(models.Model):
    image = models.ForeignKey(post, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000)


class saved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    post = models.ForeignKey(post, on_delete=models.CASCADE, related_name="postsaved")


class images(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    image = models.ImageField()

