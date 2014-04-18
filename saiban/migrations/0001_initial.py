# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Kanji'
        db.create_table(u'saiban_kanji', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('front', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='kanji', null=True, to=orm['saiban.KanjiGroup'])),
            ('on', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('kun', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('namae', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('gloss', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
        ))
        db.send_create_signal(u'saiban', ['Kanji'])

        # Adding M2M table for field radicals on 'Kanji'
        m2m_table_name = db.shorten_name(u'saiban_kanji_radicals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('kanji', models.ForeignKey(orm[u'saiban.kanji'], null=False)),
            ('radical', models.ForeignKey(orm[u'saiban.radical'], null=False))
        ))
        db.create_unique(m2m_table_name, ['kanji_id', 'radical_id'])

        # Adding M2M table for field compounds on 'Kanji'
        m2m_table_name = db.shorten_name(u'saiban_kanji_compounds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('kanji', models.ForeignKey(orm[u'saiban.kanji'], null=False)),
            ('compound', models.ForeignKey(orm[u'saiban.compound'], null=False))
        ))
        db.create_unique(m2m_table_name, ['kanji_id', 'compound_id'])

        # Adding model 'Compound'
        db.create_table(u'saiban_compound', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('front', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('gloss', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
        ))
        db.send_create_signal(u'saiban', ['Compound'])

        # Adding model 'Radical'
        db.create_table(u'saiban_radical', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('front', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('alternative', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
        ))
        db.send_create_signal(u'saiban', ['Radical'])

        # Adding model 'KanjiGroup'
        db.create_table(u'saiban_kanjigroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True)),
        ))
        db.send_create_signal(u'saiban', ['KanjiGroup'])


    def backwards(self, orm):
        # Deleting model 'Kanji'
        db.delete_table(u'saiban_kanji')

        # Removing M2M table for field radicals on 'Kanji'
        db.delete_table(db.shorten_name(u'saiban_kanji_radicals'))

        # Removing M2M table for field compounds on 'Kanji'
        db.delete_table(db.shorten_name(u'saiban_kanji_compounds'))

        # Deleting model 'Compound'
        db.delete_table(u'saiban_compound')

        # Deleting model 'Radical'
        db.delete_table(u'saiban_radical')

        # Deleting model 'KanjiGroup'
        db.delete_table(u'saiban_kanjigroup')


    models = {
        u'saiban.compound': {
            'Meta': {'object_name': 'Compound'},
            'front': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'gloss': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'saiban.kanji': {
            'Meta': {'object_name': 'Kanji'},
            'compounds': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'kanji'", 'null': 'True', 'to': u"orm['saiban.Compound']"}),
            'front': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'gloss': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'kanji'", 'null': 'True', 'to': u"orm['saiban.KanjiGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kun': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'namae': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'on': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'radicals': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'kanji'", 'null': 'True', 'to': u"orm['saiban.Radical']"})
        },
        u'saiban.kanjigroup': {
            'Meta': {'object_name': 'KanjiGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'saiban.radical': {
            'Meta': {'object_name': 'Radical'},
            'alternative': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'front': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['saiban']