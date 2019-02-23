# Python imports
import os

# Django and Library imports
from moviepy.editor import VideoFileClip
from django.conf import settings
from django.core.files import File
from django.core.validators import MinValueValidator
from django.db import models

# Custom imports
from accounts.models import UserModel
from common.models import BaseModel
from .utils import update_filename, get_extension, format_filename, VIDEO_UPLOAD_PATH
from .validators import validate_file_extension

class VideoModel(BaseModel):
    """
    Model class that stores the videos
    """
    THUMBNAIL_STORAGE_LOCATION = 'thumbnail'

    title = models.CharField(null=False,blank=False,max_length=80,unique=True)
    video_file = models.FileField(upload_to=update_filename,validators=[validate_file_extension])
    generated_link = models.CharField(null=True,blank=True,default='',max_length=180,editable=False)
    views = models.IntegerField(validators=[MinValueValidator(0)],default=0)
    public_access = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING,related_name='video_related_user')
    thumbnail = models.ImageField(upload_to=THUMBNAIL_STORAGE_LOCATION,blank=True)

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

    @property
    def get_thumbnail(self):
        # Enhancement:Change this to a celery task to improve performance
        if not self.thumbnail:
            video_path = os.path.join(settings.MEDIA_ROOT,str(self.video_file))
            clip = VideoFileClip(video_path)
            image_extention = '.jpg'
            thumbnail_path = os.path.join(settings.MEDIA_ROOT,self.THUMBNAIL_STORAGE_LOCATION,self.title+image_extention)
            thumnail_time = int(clip.duration)/2
            clip.save_frame(thumbnail_path, t=thumnail_time)
            self.thumbnail.save(
                os.path.basename(thumbnail_path),
                File(open(thumbnail_path, 'rb'))
            )
            self.save()
        return self.thumbnail

    @property
    def get_thumbnails_with_playtime(self):
        # Enhancement:Change this to a celery task to improve performance
        video_path = os.path.join(settings.MEDIA_ROOT, str(self.video_file))
        clip = VideoFileClip(video_path)
        image_extention = '.jpg'
        # Get the three thumbnails
        thumnail_time = int(clip.duration / 4)
        subtract_value = int(clip.duration / 10)
        thumbnails_with_playtime = []
        for count in range(0,4):
            thumbnail_path = os.path.join(settings.SEQUENTIAL_THUMBNAILS_LOCATION,self.title+'_{}'.format(count) \
                                          + image_extention)
            clip.save_frame(thumbnail_path, t=thumnail_time-subtract_value)
            thumbnail_src = os.path.join(settings.SEQUENTIAL_THUMBNAILS_URL,self.title+'_{}'.format(count)+ image_extention)
            thumbnails_with_playtime.append([thumbnail_src,thumnail_time-subtract_value])
            thumnail_time += int(clip.duration / 4)

        return thumbnails_with_playtime


    def save(self, *args, **kwargs):
        """
        Overridden model save method to save the generated_link of the uploaded video
        """
        # Set the generated link
        extention = get_extension(str(self.video_file))
        formated_title = format_filename(self.title)
        file_name = formated_title + extention
        self.generated_link = os.path.join(settings.MEDIA_URL,VIDEO_UPLOAD_PATH,file_name)
        super(VideoModel, self).save(*args, **kwargs)


# TODO: Use the below models in relation with a video
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