from django.core.validators import MinValueValidator
from django.db import models

from common.models import BaseModel
from accounts.models import UserModel

class VideoModel(BaseModel):
    title = models.CharField(null=False,blank=False,max_length=80,unique=True)
    video_file = models.FileField(upload_to='')
    generated_link = models.CharField(null=True,blank=True,default='',max_length=180)
    views = models.IntegerField(validators=[MinValueValidator(0)],default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    @property
    def get_number_of_likes(self):
        return self.likes_related_video.active_objects.count()

    @property
    def get_number_of_dislikes(self):
        return self.dislikes_related_video.active_objects.count()

    @property
    def get_comments(self):
        return self.comment_related_video.active_objects.values_list('comment',flat=True)

class LikeModel(BaseModel):
    user = models.ForeignKey(UserModel,on_delete=models.DO_NOTHING,related_name='likes_related_user')
    video = models.ForeignKey(VideoModel, on_delete=models.DO_NOTHING,related_name='likes_related_video')
    liked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'


class DislikeModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING,related_name='dislikes_related_user')
    video = models.ForeignKey(VideoModel, on_delete=models.DO_NOTHING,related_name='dislikes_related_video')
    disliked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Dislike'
        verbose_name_plural = 'Dislikes'


class CommentModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING,related_name='comment_related_user')
    video = models.ForeignKey(VideoModel, on_delete=models.DO_NOTHING,related_name='comment_related_video')
    comment = models.TextField(null=True, blank=True, default='', max_length=280)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'