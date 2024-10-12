from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
    body = models.TextField()
    # title = models.CharField(max_length=100,null=True,blank=True)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class meta:
        ordering = ['-created']

    def __str__(self):
        return self.slug


    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id,self.slug))

    def like_counts(self):
        return self.pvotes.count()

    def user_can_like(self,user):
        user_like = user.votes.filter(post=self)
        if user_like.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='pcomments')
    reply = models.ForeignKey('self',models.CASCADE,related_name='rcomments',null=True,blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}--{self.body[:30]}"



class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='pvotes')

    def __str__(self):
        return f"{self.user} Liked {self.post}"
