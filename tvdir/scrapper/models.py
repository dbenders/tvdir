from django.db import models
from scrapper.providers import *
from datetime import datetime
import urllib
from library.models import Channel, Genre, Program, Episode

class Scrapper(models.Model):
    name = models.CharField(max_length=30)
    klass = models.CharField(max_length=256)

    def __unicode__(self):
        return self.name

class Provider(models.Model):
    url = models.CharField(max_length=4096)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=4096, null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    scrapper = models.ForeignKey(Scrapper)
    last_scrapped = models.DateTimeField(null=True, blank=True)
    copyright = models.CharField(max_length=30, null=True, blank=True)

    def scrap(self, sections=False, programs=False, episodes=False):
        scrapper = eval(self.scrapper.klass)()
        scrapper.scrap_provider(self)
        if sections:
            for section in self.sections.all():
                section.scrap(programs, episodes)

        self.last_scrapped = datetime.now()
        self.save()

    def __unicode__(self):
        return self.name or self.url

class ProviderSection(models.Model):
    provider = models.ForeignKey(Provider, related_name='sections')
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=4096)
    last_scrapped = models.DateTimeField(null=True, blank=True)

    channel = models.ForeignKey(Channel, null=True, blank=True, related_name='sources')
    genre = models.ForeignKey(Genre, null=True, blank=True)

    def scrap(self, programs=False, episodes=False):
        scrapper = eval(self.provider.scrapper.klass)()
        scrapper.scrap_section(self)
        if programs:
            for program in self.programs.all():
                program.scrap(episodes)

        self.last_scrapped = datetime.now()
        self.save()

    def __unicode__(self):
        return "%s - %s" % (self.provider.name, self.name)

class ProgramSource(models.Model):
    section = models.ForeignKey(ProviderSection, related_name='programs')
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=4096)
    last_scrapped = models.DateTimeField(null=True, blank=True)

    program = models.ForeignKey(Program, null=True, blank=True, related_name='sources')

    def scrap(self, episodes=False):
        scrapper = eval(self.section.provider.scrapper.klass)()
        scrapper.scrap_program(self)
        if episodes:
            for episode in self.episodes.all():
                episode.scrap()

        self.last_scrapped = datetime.now()
        self.save()

    def __unicode__(self):
        return self.name

class EpisodeSource(models.Model):
    program = models.ForeignKey(ProgramSource, related_name='episodes')
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=4096)
    last_scrapped = models.DateTimeField(null=True, blank=True)

    episode = models.ForeignKey(Episode, null=True, blank=True, related_name='sources')

    def scrap(self):
        scrapper = eval(self.program.section.provider.scrapper.klass)()
        scrapper.scrap_episode(self)

        self.last_scrapped = datetime.now()
        self.save()

    def __unicode__(self):
        return unicode(self.episode)

class EpisodeMedia(models.Model):
    episode = models.ForeignKey(EpisodeSource, related_name='medias')
    order = models.IntegerField(default=1)

    mimetype = models.CharField(max_length=50, default='mp4')
    fps = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    subtitles = models.URLField(null=True, blank=True)
    live = models.BooleanField(default=True)

    transport = models.CharField(max_length=10)
    url = models.URLField(max_length=2048)

    def check_alive(self):
        print self.url
        if not self.url.startswith('http'): 
            return
        url = self.url
        if url.startswith('fox://'):
            url = 'http://' + url[6:]
        try:
            req = urllib.urlopen(url)
            if req.headers['content-type'].startswith('video'):
                self.live = True
            else:
                self.live = False
        except IOError:
            self.live = False
        self.save()

    @property
    def export_url(self):
        if self.url.startswith('fox://'):
            return "http://localhost:8080/mundofox?url=%s" % urllib.quote("http://%s" % self.url[6:])
        else:
            return self.url
