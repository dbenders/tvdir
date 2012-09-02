
from django.db import models
from django.conf import settings

#from library.utils import SubclassingModelManager, SubclassingModel

class Person(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Channel(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.URLField(null=True, blank=True)
    description = models.CharField(max_length=4096, null=True, blank=True)

    def __unicode__(self):
        return self.name

class Program(models.Model):
    channel = models.ForeignKey(Channel, null=True, blank=True, related_name='programs')
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=4096, null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True)

    director = models.ForeignKey(Person, related_name='directed', null=True, blank=True)
    actors = models.ManyToManyField(Person, related_name='acted', blank=True)

    @property
    def num_episodes(self):
        return self.episode_set.count()

    def thumbnailtag(self):
        if self.thumbnail:
            return "<img src='%s'/>" % self.thumbnail
        else:
            return ""
    thumbnailtag.allow_tags = True   

    def __unicode__(self):
        return self.name

    def selflink(self):
        if self.id:
            return "<a href='/admin/library/serie/%s'>Edit</a>" % str(self.id)
        else:
            return "Not present"

    selflink.allow_tags = True        

class Episode(models.Model):
    program = models.ForeignKey(Program, related_name='episodes')
    season = models.IntegerField(null=True, blank=True)
    number = models.IntegerField()
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=4096, null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    duration = models.TimeField(null=True, blank=True)
    air = models.DateField(null=True, blank=True)

    def __unicode__(self):
        answer = ""
        answer += "Season %d, " % self.season if self.season else ""
        answer += "Episode %d" % self.number if self.number else ""
        answer += ": %s" % self.name if self.name else ""
        answer += " (%s)" % str(self.duration) if self.duration else ""
        return answer

    def selflink(self):
        if self.id:
            return "<a href='/admin/library/episode/%s'>edit</a>" % str(self.id)
        else:
            return "Not present"

    selflink.allow_tags = True        

    def thumbnailtag(self):
        if self.thumbnail:
            return "<img src='%s'/>" % self.thumbnail
        else:
            return ""
    thumbnailtag.allow_tags = True   


