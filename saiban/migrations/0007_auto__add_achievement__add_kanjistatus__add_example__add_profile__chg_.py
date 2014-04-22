# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Achievement'
        db.create_table(u'saiban_achievement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1000)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, null=True, blank=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'saiban', ['Achievement'])

        # Adding model 'KanjiStatus'
        db.create_table(u'saiban_kanjistatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('kanji', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='status', null=True, to=orm['saiban.Kanji'])),
            ('level', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=3, decimal_places=2, blank=True)),
            ('seen', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
            ('next_practice', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('easy_factor', self.gf('django.db.models.fields.FloatField')(default=2.5)),
        ))
        db.send_create_signal(u'saiban', ['KanjiStatus'])

        # Adding model 'Example'
        db.create_table(u'saiban_example', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('front', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1000)),
            ('reading', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('gloss', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal(u'saiban', ['Example'])

        # Adding model 'Profile'
        db.create_table(u'saiban_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('streak', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'saiban', ['Profile'])

        # Adding M2M table for field achievements on 'Profile'
        m2m_table_name = db.shorten_name(u'saiban_profile_achievements')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'saiban.profile'], null=False)),
            ('achievement', models.ForeignKey(orm[u'saiban.achievement'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'achievement_id'])

        # Adding M2M table for field examples on 'Compound'
        m2m_table_name = db.shorten_name(u'saiban_compound_examples')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('compound', models.ForeignKey(orm[u'saiban.compound'], null=False)),
            ('example', models.ForeignKey(orm[u'saiban.example'], null=False))
        ))
        db.create_unique(m2m_table_name, ['compound_id', 'example_id'])


        # Changing field 'KanjiGroup.level'
        db.alter_column(u'saiban_kanjigroup', 'level', self.gf('django.db.models.fields.PositiveIntegerField')())

    def backwards(self, orm):
        # Deleting model 'Achievement'
        db.delete_table(u'saiban_achievement')

        # Deleting model 'KanjiStatus'
        db.delete_table(u'saiban_kanjistatus')

        # Deleting model 'Example'
        db.delete_table(u'saiban_example')

        # Deleting model 'Profile'
        db.delete_table(u'saiban_profile')

        # Removing M2M table for field achievements on 'Profile'
        db.delete_table(db.shorten_name(u'saiban_profile_achievements'))

        # Removing M2M table for field examples on 'Compound'
        db.delete_table(db.shorten_name(u'saiban_compound_examples'))


        # Changing field 'KanjiGroup.level'
        db.alter_column(u'saiban_kanjigroup', 'level', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'saiban.achievement': {
            'Meta': {'object_name': 'Achievement'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1000'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'})
        },
        u'saiban.compound': {
            'Meta': {'object_name': 'Compound'},
            'examples': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'compons'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['saiban.Example']"}),
            'front': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'gloss': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reading': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'saiban.example': {
            'Meta': {'object_name': 'Example'},
            'front': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1000'}),
            'gloss': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reading': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'})
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
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'saiban.kanjistatus': {
            'Meta': {'ordering': "['next_practice']", 'object_name': 'KanjiStatus'},
            'easy_factor': ('django.db.models.fields.FloatField', [], {'default': '2.5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kanji': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'status'", 'null': 'True', 'to': u"orm['saiban.Kanji']"}),
            'level': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'next_practice': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'seen': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'saiban.profile': {
            'Meta': {'object_name': 'Profile'},
            'achievements': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'profiles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['saiban.Achievement']"}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'streak': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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