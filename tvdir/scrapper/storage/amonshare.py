import urllib
from bs4 import BeautifulSoup
import re

class Storage(object):
    def get_file(self, video_id):
        url = "http://amonshare.com/%s" % video_id
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, from_encoding='latin-1')
        data = {}
        for elem in soup.form('input'):
            if elem.get('name'):
                data[elem.get('name')] = elem.get('value')
        html = urllib.urlopen(url, urllib.urlencode(data)).read()

        soup = BeautifulSoup(html, from_encoding='latin-1')
        data = {}
        for elem in soup.form('input'):
            if elem.get('name'):
                data[elem.get('name')] = elem.get('value')
        html = urllib.urlopen(url, urllib.urlencode(data)).read()
        video_url = re.findall('href="([^"]+).mp4"', html)[0] + ".mp4"
        return video_url
