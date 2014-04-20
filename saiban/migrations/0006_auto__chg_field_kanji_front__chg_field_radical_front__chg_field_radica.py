# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Kanji.front'
        db.alter_column(u'saiban_kanji', 'front', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10))

        # Changing field 'Radical.front'
        db.alter_column(u'saiban_radical', 'front', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10))

        # Changing field 'Radical.alternative'
        db.alter_column(u'saiban_radical', 'alternative', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

    def backwards(self, orm):

        # Changing field 'Kanji.front'
        db.alter_column(u'saiban_kanji', 'front', self.gf('django.db.models.fields.CharField')(max_length=1, unique=True))

        # Changing field 'Radical.front'
        db.alter_column(u'saiban_radical', 'front', self.gf('django.db.models.fields.CharField')(max_length=1, unique=True))

        # Changing field 'Radical.alternative'
        db.alter_column(u'saiban_radical', 'alternative', self.gf('django.db.models.fields.CharField')(max_length=1, null=True))

    models = {
        u'saiban.compound': {
            'Meta': {'object_name': 'Compound'},
            'front': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'gloss': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reading': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'saiban.kanji': {
            'Meta': {'object_name': 'Kanji'},
            'compounds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'kanji'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['saiban.Compound']"}),
            'front': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'gloss': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'kanji'", 'null': 'True', 'to': u"orm['saiban.KanjiGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jlpt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kun': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nanori': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'on': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'processed': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'radicals': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'kanji'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['saiban.Radical']"}),
            'strokes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'saiban.kanjigroup': {
            'Meta': {'object_name': 'KanjiGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'saiban.radical': {
            'Meta': {'object_name': 'Radical'},
            'alternative': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'front': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['saiban']