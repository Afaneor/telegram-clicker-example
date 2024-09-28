# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey('Posts', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class Friends(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    friend = models.ForeignKey('Users', models.DO_NOTHING, related_name='friends_friend_set', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'friends'


class Likes(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey('Posts', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'likes'


class Posts(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.TextField(unique=True)
    email = models.TextField(unique=True)
    password = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    profile_picture = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
