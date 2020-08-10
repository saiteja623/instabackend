from django.contrib import admin

# Register your models here.
from .models import likedby, userProfile, customUser, date, post,images

# Register your models here.
admin.site.register(likedby)
admin.site.register(userProfile)
admin.site.register(customUser)
admin.site.register(date)
admin.site.register(images)
admin.site.register(post)
