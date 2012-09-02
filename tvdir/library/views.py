# Create your views here.
from django.views.generic import ListView, DetailView
from library.models import Channel, Program

class ChannelListView(ListView):
    model = Channel
    context_object_name = 'channels'

class ChannelDetailView(DetailView):
    model = Channel
    context_object_name = 'channel'

    def get_context_data(self, **kwargs):
        context = super(ChannelDetailView, self).get_context_data(**kwargs)
        programs = {}
        for program in set(context['channel'].programs.filter(episodes__isnull=False).all()):
            if program.genre not in programs: programs[program.genre] = []
            programs[program.genre].append(program)
        context['programs'] = programs
        return context    

class ProgramDetailView(DetailView):
    model = Program
    context_object_name = 'program'

    def get_context_data(self, **kwargs):
        context = super(ProgramDetailView, self).get_context_data(**kwargs)
        episodes = {}
        for episode in context['program'].episodes.all():
            season = episode.season or 1
            if season not in episodes: episodes[season] = []
            episodes[season].append(episode)
        context['episodes'] = episodes
        return context 
