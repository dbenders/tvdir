from scrapper.models import Provider, Scrapper, ProviderSection, ProgramSource, EpisodeSource
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core import urlresolvers
import urllib

class ProviderAdmin(admin.ModelAdmin):
    actions = ['scrap']
    list_display = ['namex','num_sections','edit']

    def scrap(self, request, queryset):
        for provider in queryset:  
            provider.scrap()          
    
    def self(self, provider):
        return unicode(provider)

    def num_sections(self, provider):
        return provider.sections.count()

    def edit(self, provider):
        return "<a href='%s'>edit</a>" % urlresolvers.reverse("admin:scrapper_provider_change", args=(provider.id,))
    edit.allow_tags = True

    def namex(self, provider):
        return "<a href='%s?%s'>%s</a>" % (urlresolvers.reverse("admin:scrapper_providersection_changelist"),
            urllib.urlencode(dict(provider__id__exact=provider.id)), unicode(provider))
    namex.allow_tags = True

class ProgramSourceInline(admin.TabularInline):
    model = ProgramSource
    fields = ('name','url',)

class ProviderSectionAdmin(admin.ModelAdmin):
    list_display = ['namex','num_programs','edit']
    actions = ['scrap','check_alive']
    list_filter = ['provider']
    inlines = [ProgramSourceInline]

    def scrap(self, request, queryset):
        for section in queryset:  
            section.scrap()          

    def check_alive(self, request, queryset):
        for section in queryset:
            for program in section.programs.all():
                for episode in program.episodes.all():
                    for media in episode.medias.iterator():
                        media.check_alive()

    def num_programs(self, section):
        return section.programs.count()

    def edit(self, section):
        return "<a href='%s'>edit</a>" % urlresolvers.reverse("admin:scrapper_providersection_change", args=(section.id,))
    edit.allow_tags = True

    def namex(self, section):
        return "<a href='%s?%s'>%s</a>" % (urlresolvers.reverse("admin:scrapper_programsource_changelist"),
            urllib.urlencode(dict(section__id__exact=section.id)), unicode(section))
    namex.allow_tags = True

class ProgramSourceAdmin(admin.ModelAdmin):
    actions = ['scrap']
    list_display = ['name','num_episodes','edit']
    list_filter = ['section']
    search_fields = ['name',]
    
    def scrap(self, request, queryset):
        for program in queryset:  
            program.scrap()          

    def num_episodes(self, program):
        return program.episodes.count()

    def edit(self, program):
        return "<a href='%s'>edit</a>" % urlresolvers.reverse("admin:scrapper_programsource_change", args=(program.id,))
    edit.allow_tags = True

class EpisodeSourceAdmin(admin.ModelAdmin):
    actions = ['scrap','check_alive']
    list_display = ['namex','num_medias']
    list_filter = ['program']
    search_fields = ['program__name']

    def scrap(self, request, queryset):
        for episode in queryset:  
            episode.scrap()          

    def num_medias(self, episode):
        return episode.medias.filter(live=True).count()

    def check_alive(self, request, queryset):
        for episode in queryset.iterator():
            for media in episode.medias.iterator():
                media.check_alive()

    def namex(self, episode):
        return unicode(episode)

admin.site.register(Scrapper)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(ProviderSection, ProviderSectionAdmin)
admin.site.register(ProgramSource, ProgramSourceAdmin)
admin.site.register(EpisodeSource, EpisodeSourceAdmin)

#admin.site.register(Serie, SerieAdmin)
