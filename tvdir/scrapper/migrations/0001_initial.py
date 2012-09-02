# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Scrapper'
        db.create_table('scrapper_scrapper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('klass', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('scrapper', ['Scrapper'])

        # Adding model 'Provider'
        db.create_table('scrapper_provider', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('scrapper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scrapper.Scrapper'])),
            ('last_scrapped', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('copyright', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('scrapper', ['Provider'])

        # Adding model 'ProviderSection'
        db.create_table('scrapper_providersection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections', to=orm['scrapper.Provider'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=4096)),
            ('last_scrapped', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sources', null=True, to=orm['library.Channel'])),
            ('genre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Genre'], null=True, blank=True)),
        ))
        db.send_create_signal('scrapper', ['ProviderSection'])

        # Adding model 'ProgramSource'
        db.create_table('scrapper_programsource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='programs', to=orm['scrapper.ProviderSection'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=4096)),
            ('last_scrapped', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sources', null=True, to=orm['library.Program'])),
        ))
        db.send_create_signal('scrapper', ['ProgramSource'])

        # Adding model 'EpisodeSource'
        db.create_table('scrapper_episodesource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(related_name='episodes', to=orm['scrapper.ProgramSource'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=4096)),
            ('last_scrapped', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sources', null=True, to=orm['library.Episode'])),
        ))
        db.send_create_signal('scrapper', ['EpisodeSource'])

        # Adding model 'EpisodeMedia'
        db.create_table('scrapper_episodemedia', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(related_name='medias', to=orm['scrapper.EpisodeSource'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('mimetype', self.gf('django.db.models.fields.CharField')(default='mp4', max_length=50)),
            ('fps', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('subtitles', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('live', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('transport', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=2048)),
        ))
        db.send_create_signal('scrapper', ['EpisodeMedia'])


    def backwards(self, orm):
        # Deleting model 'Scrapper'
        db.delete_table('scrapper_scrapper')

        # Deleting model 'Provider'
        db.delete_table('scrapper_provider')

        # Deleting model 'ProviderSection'
        db.delete_table('scrapper_providersection')

        # Deleting model 'ProgramSource'
        db.delete_table('scrapper_programsource')

        # Deleting model 'EpisodeSource'
        db.delete_table('scrapper_episodesource')

        # Deleting model 'EpisodeMedia'
        db.delete_table('scrapper_episodemedia')


    models = {
        'library.channel': {
            'Meta': {'object_name': 'Channel'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'library.episode': {
            'Meta': {'object_name': 'Episode'},
            'air': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': "orm['library.Program']"}),
            'season': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'library.genre': {
            'Meta': {'object_name': 'Genre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'library.person': {
            'Meta': {'object_name': 'Person'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'library.program': {
            'Meta': {'object_name': 'Program'},
            'actors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'acted'", 'blank': 'True', 'to': "orm['library.Person']"}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'programs'", 'null': 'True', 'to': "orm['library.Channel']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'director': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'directed'", 'null': 'True', 'to': "orm['library.Person']"}),
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Genre']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'scrapper.episodemedia': {
            'Meta': {'object_name': 'EpisodeMedia'},
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'medias'", 'to': "orm['scrapper.EpisodeSource']"}),
            'fps': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'default': "'mp4'", 'max_length': '50'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'subtitles': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'transport': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048'}),
            'width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'scrapper.episodesource': {
            'Meta': {'object_name': 'EpisodeSource'},
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sources'", 'null': 'True', 'to': "orm['library.Episode']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scrapped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'episodes'", 'to': "orm['scrapper.ProgramSource']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '4096'})
        },
        'scrapper.programsource': {
            'Meta': {'object_name': 'ProgramSource'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scrapped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'program': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sources'", 'null': 'True', 'to': "orm['library.Program']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'programs'", 'to': "orm['scrapper.ProviderSection']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '4096'})
        },
        'scrapper.provider': {
            'Meta': {'object_name': 'Provider'},
            'copyright': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scrapped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'scrapper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scrapper.Scrapper']"}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'scrapper.providersection': {
            'Meta': {'object_name': 'ProviderSection'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sources'", 'null': 'True', 'to': "orm['library.Channel']"}),
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Genre']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scrapped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': "orm['scrapper.Provider']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '4096'})
        },
        'scrapper.scrapper': {
            'Meta': {'object_name': 'Scrapper'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'klass': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['scrapper']