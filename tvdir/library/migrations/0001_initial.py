# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('library_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('library', ['Person'])

        # Adding model 'Genre'
        db.create_table('library_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('library', ['Genre'])

        # Adding model 'Channel'
        db.create_table('library_channel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True, blank=True)),
        ))
        db.send_create_signal('library', ['Channel'])

        # Adding model 'Program'
        db.create_table('library_program', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Channel'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('genre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Genre'], null=True, blank=True)),
            ('director', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='directed', null=True, to=orm['library.Person'])),
        ))
        db.send_create_signal('library', ['Program'])

        # Adding M2M table for field actors on 'Program'
        db.create_table('library_program_actors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('program', models.ForeignKey(orm['library.program'], null=False)),
            ('person', models.ForeignKey(orm['library.person'], null=False))
        ))
        db.create_unique('library_program_actors', ['program_id', 'person_id'])

        # Adding model 'Episode'
        db.create_table('library_episode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('program', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Program'])),
            ('season', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('air', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('library', ['Episode'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table('library_person')

        # Deleting model 'Genre'
        db.delete_table('library_genre')

        # Deleting model 'Channel'
        db.delete_table('library_channel')

        # Deleting model 'Program'
        db.delete_table('library_program')

        # Removing M2M table for field actors on 'Program'
        db.delete_table('library_program_actors')

        # Deleting model 'Episode'
        db.delete_table('library_episode')


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
            'program': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Program']"}),
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
            'actors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'acted'", 'symmetrical': 'False', 'to': "orm['library.Person']"}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Channel']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'director': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'directed'", 'null': 'True', 'to': "orm['library.Person']"}),
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Genre']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['library']