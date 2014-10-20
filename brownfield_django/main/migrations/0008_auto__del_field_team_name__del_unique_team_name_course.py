# flake8: noqa
# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Team', fields ['name', 'course']
        db.delete_unique(u'main_team', ['name', 'course_id'])

        # Deleting field 'Team.name'
        db.delete_column(u'main_team', 'name')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Team.name'
        raise RuntimeError("Cannot reverse this migration. 'Team.name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Team.name'
        db.add_column(u'main_team', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)

        # Adding unique constraint on 'Team', fields ['name', 'course']
        db.create_unique(u'main_team', ['name', 'course_id'])


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
        u'main.course': {
            'Meta': {'object_name': 'Course'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enableNarrative': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'taught_by'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'startingBudget': ('django.db.models.fields.PositiveIntegerField', [], {'default': '60000'})
        },
        u'main.document': {
            'Meta': {'object_name': 'Document'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['main.Course']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'main.history': {
            'Meta': {'object_name': 'History'},
            'cost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Team']"})
        },
        u'main.performedtest': {
            'Meta': {'object_name': 'PerformedTest'},
            'X': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paramString': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'testNumber': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'y': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'z': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'main.team': {
            'Meta': {'object_name': 'Team'},
            'budget': ('django.db.models.fields.PositiveIntegerField', [], {'default': '65000'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Course']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'signed_contract': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team_entity': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'team'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'main.userprofile': {
            'Meta': {'ordering': "['user']", 'object_name': 'UserProfile'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['main.Course']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['main.Team']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'main.visit': {
            'Meta': {'object_name': 'Visit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']