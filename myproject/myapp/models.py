# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Languages(models.Model):
    languageid = models.AutoField(db_column='LanguageId', primary_key=True)  # Field name made lowercase.
    languagename = models.CharField(db_column='LanguageName', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Languages'


class Levels(models.Model):
    levelid = models.AutoField(db_column='LevelId', primary_key=True)  # Field name made lowercase.
    levelname = models.CharField(db_column='LevelName', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Levels'


class Postcontent(models.Model):
    postcontentid = models.AutoField(db_column='PostContentId', primary_key=True)  # Field name made lowercase.
    postid = models.ForeignKey('Posts', models.DO_NOTHING, db_column='PostId')  # Field name made lowercase.
    languageid = models.ForeignKey(Languages, models.DO_NOTHING, db_column='LanguageId')  # Field name made lowercase.
    levelid = models.ForeignKey(Levels, models.DO_NOTHING, db_column='LevelId')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255)  # Field name made lowercase.
    content = models.TextField(db_column='Content')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PostContent'
        unique_together = (('postid', 'languageid', 'levelid'),)


class Posts(models.Model):
    postid = models.AutoField(db_column='PostId', primary_key=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='UpdatedAt', blank=True, null=True)  # Field name made lowercase.
    authorid = models.ForeignKey('Users', models.DO_NOTHING, db_column='AuthorId')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=9, blank=True, null=True)  # Field name made lowercase.
    image = models.TextField(db_column='Image', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Posts'


class Questions(models.Model):
    questionid = models.AutoField(db_column='QuestionId', primary_key=True)  # Field name made lowercase.
    postcontentid = models.ForeignKey(Postcontent, models.DO_NOTHING, db_column='PostContentId')  # Field name made lowercase.
    questiontext = models.TextField(db_column='QuestionText')  # Field name made lowercase.
    answer = models.TextField(db_column='Answer', blank=True, null=True)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Questions'


class Sitestats(models.Model):
    statid = models.AutoField(db_column='StatId', primary_key=True)  # Field name made lowercase.
    totalviews = models.BigIntegerField(db_column='TotalViews', blank=True, null=True)  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sitestats'


class Users(models.Model):
    userid = models.AutoField(db_column='UserId', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', unique=True, max_length=50)  # Field name made lowercase.
    passwordhash = models.CharField(db_column='PasswordHash', max_length=255)  # Field name made lowercase.
    createdat = models.DateTimeField(db_column='CreatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'
