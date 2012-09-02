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
import urlparse

from django.conf import settings

import scrapper.models
import library.models
from scrapper.storage import *

class Scrapper(object):

    def scrap_provider(self, provider):
        provider.name = provider.name or "crackle"
        provider.copyright = provider.copyright or "free"
        provider.save()

        parsed_url = urlparse.urlparse(provider.url)

        html = urllib.urlopen(provider.url).read()
        soup = BeautifulSoup(html, from_encoding='utf-8')
        for elem in soup.find('div','contents')('li'):
            section = scrapper.models.ProviderSection.objects.get_or_create(provider=provider, name=elem.a.text)[0]
            data = dict(urlparse.parse_qs(parsed_url.fragment))
            data['fa'] = re.findall('\(([0-9]+)\)', elem.a['href'])[0]
            fragment = urllib.urlencode(data)
            section.url = urlparse.urlunparse((parsed_url.scheme, parsed_url.netloc, 
                parsed_url.path, parsed_url.params, parsed_url.query, fragment))
            section.channel = section.channel or library.models.Channel.objects.get_or_create(name='Crackle')[0]
            section.save()
        
    def scrap_section(self, section):
        #html = urllib.urlopen(section.url).read()
        #soup = BeautifulSoup(html, from_encoding='utf-8')
        #import ipdb; ipdb.set_trace()
        #rssurl = urllib.basejoin(section.url, soup.find('a',attrs={'title':'RSS 2.0'})['href'])
        rssurl = section.url
        rss = urllib.urlopen(rssurl).read()
        soup = BeautifulSoup(rss, from_encoding='utf-8')

        for elem in soup('item'):
            thumbnail = elem.find('media:thumbnail')['url']
            program_source = scrapper.models.ProgramSource.objects.get_or_create(section=section, url=thumbnail)[0]

            name = elem.title.text
            program_source.name = name

            program = library.models.Program.objects.get_or_create(channel=section.channel, name=name)[0]
            program.thumbnail = thumbnail
            program.name = name
            program.description = elem.description.text
            program.save()

            program_source.program = program
            program_source.save()

    def scrap_program(self, program):
        print program.name
        episode_source = scrapper.models.EpisodeSource.objects.get_or_create(program=program, url=program.url)[0]
        episode = library.models.Episode.objects.get_or_create(program=program.program, season=1, number=1)[0]
        episode_source.episode = episode
        episode_source.save()

        r = re.compile('http://images-(.*?)\.crackle.com(/.*?)_.*')
        g = r.findall(program.url)[0]
        url = 'rtmp://stream_auth-%s.akamai.crackle.com:443/ondemand/mp4:crackle%s_360p' % g
        m = scrapper.models.EpisodeMedia.objects.get_or_create(episode=episode_source,url=url)[0]
