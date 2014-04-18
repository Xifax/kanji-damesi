# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Kanji.namae'
        db.delete_column(u'saiban_kanji', 'namae')

        # Adding field 'Kanji.nanori'
        db.add_column(u'saiban_kanji', 'nanori',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Kanji.jlpt'
        db.add_column(u'saiban_kanji', 'jlpt',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Kanji.grade'
        db.add_column(u'saiban_kanji', 'grade',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Kanji.strokes'
        db.add_column(u'saiban_kanji', 'strokes',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Kanji.namae'
        db.add_column(u'saiban_kanji', 'namae',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Kanji.nanori'
        db.delete_column(u'saiban_kanji', 'nanori')

        # Deleting field 'Kanji.jlpt'
        db.delete_column(u'saiban_kanji', 'jlpt')

        # Deleting field 'Kanji.grade'
        db.delete_column(u'saiban_kanji', 'grade')

        # Deleting field 'Kanji.strokes'
        db.delete_column(u'saiban_kanji', 'strokes')


    models = {
        u'saiban.compound': {
            'Meta': {'object_name': 'Compound'},
            'front': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'gloss': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reading': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'saiban.kanji': {
            'Meta': {'object_name': 'Kanji'},
            'compounds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'kanji'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['saiban.Compound']"}),
            'front': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'gloss': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'grade': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'kanji'", 'null': 'True', 'to': u"orm['saiban.KanjiGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jlpt': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kun': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nanori': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'on': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'alternative': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'front': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['saiban']