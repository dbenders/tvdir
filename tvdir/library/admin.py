from library.models import Channel, Program, Genre, Episode
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core import urlresolvers
import urllib

class ProgramAdmin(admin.ModelAdmin):
    list_display = ['nametag','genre','num_episodes','edit']
    #list_display = ['nametag','genre','edit']
    list_filter = ['channel']
    search_fields = ['name']



    def nametag(self, program):
        return "<a href='%s?%s'><table><tr><td width='65px'><img width='60px' src='%s'/></td><td style='vertical-align:middle'>%s</td></tr></table></a>" % \
            (urlresolvers.reverse("admin:library_episode_changelist"),
            urllib.urlencode(dict(program__id__exact=program.id)), program.thumbnail,unicode(program))
    nametag.allow_tags = True
    nametag.admin_order_field = 'name'

    def edit(self, channel):
        return "<a href='%s'>edit</a>" % urlresolvers.reverse("admin:library_program_change", args=(channel.id,))
    edit.allow_tags = True

    def queryset(self, request):
        qs = super(ProgramAdmin, self).queryset(request)
        return qs
        #return qs.exclude(episodes=None)

    def num_episodes(self, program):
        return program.episodes.count()
    #num_episodes.admin_order_field = 'episodes'

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['nametag','medialinks']
    list_filter = ['program']
    #search_fields = ['name']

    def nametag(self, episode):
        return "<a href='%s'><table><tr><td width='65px'><img width='60px' src='%s'/></td><td style='vertical-align:middle'>%s</td></tr></table></a>" % \
            (urlresolvers.reverse("admin:library_episode_change", args=(episode.id,)),
            episode.thumbnail,unicode(episode))
    nametag.allow_tags = True

    def medialinks(self, episode):
        answer = "<table>"
        cnt = 1
        for source in episode.sources.iterator():
            for media in source.medias.filter(live=True).iterator():
                answer += "<tr><td><a href='%s'>link %d</a></td></tr>" % (media.url,cnt)
                cnt += 1
        answer += "</table>"
        return answer
    medialinks.allow_tags = True

    def num_medias(self, episode):
        x = map(lambda x:len(x.medias.filter(live=True)),episode.sources.iterator())
        return sum(x)


    # def edit(self, channel):
    #     return "<a href='%s'>edit</a>" % urlresolvers.reverse("admin:library_channel_change", args=(channel.id,))
    # edit.allow_tags = True        

class ProgramInline(admin.TabularInline):
    model = Program
    #extra = 0
    fields = ('name','genre',)

class ChannelAdmin(admin.ModelAdmin):
    inlines = [ProgramInline]
    list_display = ['nametag','num_programs','edit']
    #list_display_links = ['name',]

    def nametag(self, channel):
        return "<a href='%s?%s'><table><tr><td width='65px'><img width='60px' src='%s'/></td><td style='vertical-align:middle'>%s</td></tr></table></a>" % \
            (urlresolvers.reverse("admin:library_program_changelist"),
            urllib.urlencode(dict(channel__id__exact=channel.id)), channel.thumbnail,unicode(channel))
    nametag.allow_tags = True

    def num_programs(self, channel):
        return channel.programs.count()

    def edit(self, channel):
        return "<a href='%s'>edit</a>" % urlresolvers.reverse("admin:library_channel_change", args=(channel.id,))
    edit.allow_tags = True        

admin.site.register(Genre)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Episode, EpisodeAdmin)
