from django.db import models
# Create your models here.
# import short_url

class Post(models.Model):
    title = models.CharField(max_length=200,help_text="Enter the title")
    description = models.TextField(help_text='Enter a brief description of this post')
    date = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=2000,null=True,blank = True)
    image = models.ImageField(upload_to = 'images', null=True,blank = True) 
    
    class Meta:
        get_latest_by = "date"
    def save(self, *args, **kwargs): 
       
        super(Post, self).save(*args, **kwargs) 
    
    def __str__(self):
        return self.title + '  ' + self.description
    
    
        
    
    



    