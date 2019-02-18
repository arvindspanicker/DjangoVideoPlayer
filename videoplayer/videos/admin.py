from django.contrib import admin
from videos import models


@admin.register(models.VideoModel)
class VideosModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'video_file', 'generated_link', 'views')
    list_filter = ('title', 'views',)
    readonly_fields = ('generated_link', 'views')


@admin.register(models.LikeModel)
class LikesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'video', 'liked')
    list_filter = ('user', 'video')
    readonly_fields = ('user', 'video')

@admin.register(models.DislikeModel)
class DisLikesModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'video', 'disliked')
    list_filter = ('user', 'video')
    readonly_fields = ('user', 'video')


@admin.register(models.CommentModel)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'video', 'comment')
    list_filter = ('user', 'video')
    readonly_fields = ('user', 'video')
