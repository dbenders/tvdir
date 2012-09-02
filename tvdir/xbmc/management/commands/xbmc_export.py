from django.core.management.base import BaseCommand, CommandError
from library.models import Channel, Episode
import os

class Command(BaseCommand):
    help = 'Export library for xbmc'

    def get_serie_nfo(self, program):
        answer = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n<tvshow>"
        answer += "<title>%s</title>\n" % program.name
        if program.description:
            answer += "<plot>%s</plot>\n" % program.description
        if program.thumbnail:
            answer += "<thumb>%s</thumb>\n" % program.thumbnail
        answer += "<studio>%s</studio>\n" % program.channel.name
        answer += "</tvshow>"
        return answer

    def get_nfo(self, episode):
        answer = u"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n<episodedetails>"
        if episode.name:
            answer += u"<title>%s</title>\n" % (episode.name or '')
        answer += u"<season>%d</season>\n" % (episode.season or 1)
        answer += u"<episode>%d</episode>\n" % (episode.number or 1)
        if episode.description:
            answer += u"<plot>%s</plot>\n" % episode.description
        if episode.thumbnail:
            answer += u"<thumb>%s</thumb>\n" % episode.thumbnail.strip()
        answer += u"<studio>%s</studio>\n" % episode.program.channel.name
        answer += u"</episodedetails>"
        return answer

    def handle(self, *args, **options):
        dir = '/Users/diego/tmp/xbmc'
        for channel in Channel.objects.filter(name='CDA').all():
            channelpath = os.path.join(dir,channel.name.encode('ascii','ignore'))
            print channelpath
            try: os.makedirs(channelpath)
            except: pass
            for serie in channel.programs.all():
                if serie.episodes.count() == 0: continue
                #seriepath = os.path.join(dir,serie.name.encode('utf8'))
                seriepath = os.path.join(channelpath,serie.name.encode('ascii','ignore'))
                print seriepath
                try: os.makedirs(seriepath)
                except: pass
                if True: #not serie.discard_info: 
                    with open(os.path.join(seriepath,'tvshow.nfo'),'w') as f:
                        f.write(self.get_serie_nfo(serie).encode('utf8'))
                for episode in serie.episodes.all():
                    fname = '%s.s%02de%02d' % (episode.program.name,episode.season or 1,max(episode.number,1))
                    fname = fname.encode('ascii','ignore')
                    print fname
                    try:
                        with open(os.path.join(seriepath,fname + '.strm'),'w') as f:
                            for source in episode.sources.all():
                                for media in source.medias.all():
                                    f.write('%s\n' % media.export_url)
                        
                            with open(os.path.join(seriepath,fname + '.nfo'),'w') as f:
                                f.write(self.get_nfo(episode).encode('utf8'))
                    except Exception,e:
                        print e
                        try:
                            os.unlink(os.path.join(dir,fname + '.strm'))
                        except: pass
                        try:
                            os.unlink(os.path.join(dir,fname + '.nfo'))
                        except: pass

        self.stdout.write('Successfully exported all episodes.\n')


