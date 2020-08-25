from django.contrib import admin
from django.db import models
from django.conf import settings
import os

from .models import Post

import facebook


TOKEN='EAAHRJjlDsiABAM19XL5d8iMnjF00a90fQkydauz3zsEm9MsmfIGATTeKvLqZC0sQpEU9AYZCOTlzst4bq7Tf047IttiwUzizhESzfOZAoTtGfEnPYPUARcpj9jrzIW4YyCFyWe2bA27qmAWyw5hQOIRcOUjhI0jgxKG05gJriARWFMjsEnTI3YHfk2kTG8ZD'


BASE_PROJECT_DIR = os.path.dirname(os.path.abspath(__file__ + '../../')).replace('\\','/')


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','image','url')

    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        # self.post_to_facebook(obj)
        super().save_model(request, obj, form, change)
        post_obj = Post.objects.latest('date')
        # self.post_to_facebook(post_obj)
        
    def post_to_facebook(self,object):
        graph = facebook.GraphAPI(access_token=TOKEN)
        if not object.image and not object.url:
            graph.put_object(
            parent_object="me",
            connection_name="feed",
            message="{0}\n{1}".format(object.title,object.description))
        elif object.image and object.url:
            graph.put_photo(image=open('{0}{1}'.format(BASE_PROJECT_DIR,object.image.url), 'rb'),message='{0}\n{1}\n{2}'.format(object.title,object.description,object.url))
        elif object.image and not object.url:
            graph.put_photo(image=open('{0}{1}'.format(BASE_PROJECT_DIR,object.image.url), 'rb'),message='{0}\n{1}'.format(object.title,object.description))
        elif not object.image and object.url:
            graph.put_object(
            parent_object="me",
            connection_name="feed",
            message="{0}\n{1}".format(object.title,object.description),
            link="{0}".format(object.url))
            
            