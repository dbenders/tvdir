#-*- encoding: utf8
import urllib
import simplejson
import bs4
from bs4 import BeautifulSoup
import re
import urlparse

import random
import os
from datetime import time

from django.conf import settings

import scrapper.models
import library.models
from scrapper.storage import *

class Scrapper(object):

    def scrap_provider(self, provider):
        provider.name = provider.name or "miratuserie"
        provider.copyright = provider.copyright or "pirated"
        provider.save()

        section = scrapper.models.ProviderSection.objects.get_or_create(provider=provider, name='main')[0]
        section.url = section.url or provider.url
        channel = library.models.Channel.objects.get_or_create(name='miratuserie')[0]
        section.channel = channel
        section.save()
        
    def scrap_section(self, section):
        html = urllib.urlopen(section.url).read()
        html = html[html.index('<html'):]
        soup = BeautifulSoup(html, from_encoding='latin-1')
        for elem in soup.ul('li'):
            url = elem.a.get('href')
            print url
            program_source = scrapper.models.ProgramSource.objects.get_or_create(section=section, url=url)[0]
            try:
                name = url[url.index('mira')+4:url.index('.com')]
                program = library.models.Program.objects.get_or_create(channel=section.channel, name=name)[0]
                program_source.program = program
                program_source.name = program_source.name or name
                program_source.save()
                program.thumbnail = program.thumbnail or urllib.basejoin(elem.a.get('href'),elem.img.get('src'))
                program.save()
            except: pass

    def scrap_program(self, program):
        url = program.url
        html = urllib.urlopen(url).read()
        html = html[html.index('<html'):]
        soup = BeautifulSoup(html, from_encoding='latin-1')
        for season in soup.find('ul',attrs={'id':'nav'})('li'):
            print "season %s..." % season.a.text
            self.scrap_season(program, int(season.a.text), urllib.basejoin(url,season.a.get('href')))

    def scrap_season(self, program, num, url):
        html = urllib.urlopen(url).read()
        html = html[html.index('<html'):]
        soup = BeautifulSoup(html, from_encoding='latin-1')        
        for cap in soup('div','capitulo'):
            try:
                p = cap.h3.a.text.split(':')
                episode_url = urllib.basejoin(program.url, cap.h3.a.get('href'))
                episode_num = int(p[0].lower().split('x')[-1])
                episode_name = p[1].strip()
                print cap.h3.a.text
                episode_source = scrapper.models.EpisodeSource.objects.get_or_create(program=program, url=episode_url)[0]
                episode = library.models.Episode.objects.get_or_create(program=program.program, season=num, number=episode_num)[0]
                episode_source.episode = episode
                episode_source.save()


                episode.name = episode.name or episode_name
                episode.thumbnail = episode.thumbnail or cap.img.get('src')
                episode.description = episode.description or cap.p.text
                episode.save()
                self.scrap_episode(episode_source)
            except Exception,e:
                print e

    def scrap_file(self, site, episode, url):
        try:
            storage = eval('%s.Storage' % site)()
            media_url = storage.get_file(url)
            m = scrapper.models.EpisodeMedia.objects.get_or_create(episode=episode,url=media_url)[0]
            m.save()
        except Exception,e:
            print "ERROR: %s with site %s" % (e,site)

    def scrap_vidbull(self, episode, video_id):
        import ipdb; ipdb.set_trace()
        url = "http://vidbull.com/%s" % video_id
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, from_encoding='latin-1')
        data = {}
        for elem in soup.find('form',attrs={'name':'F1'})('input'):
            if elem.get('name'):
                data[elem.get('name')] = elem.get('value')
        
        html = urllib.urlopen(url, urllib.urlencode(data)).read()
        soup = BeautifulSoup(html, from_encoding='latin-1')
        data = {}
        for elem in soup.form('input'):
            if elem.get('name'):
                data[elem.get('name')] = elem.get('value')

        html = urllib.urlopen(url, urllib.urlencode(data)).read()
        video_url = re.findall('a href="(.*?mp4)"', html)[0]

        media = HttpMediaFile(episode=episode)
        media.save()

        episode.subtitles = "http://sc.miratuserie.com/episodes/subs/%s.srt" % video_id.split('.')[0]
        episode.save()


    def scrap_episode(self, episode):
        print "S%02dS%02dE" % (episode.episode.season,episode.episode.number)
        html = urllib.urlopen(episode.url).read()
        html = html[html.index('<html'):]
        soup = BeautifulSoup(html, from_encoding='latin-1')        

        frame_url = soup.find('iframe','servidores').get('src')
        if frame_url.startswith('//'): frame_url = 'http:' + frame_url
        frame_html = urllib.urlopen(frame_url).read()

        p = re.findall("verVid\('([^']+)','([^']+)'", frame_html)
        for site in p:
            self.scrap_file(site[1],episode,site[0])

