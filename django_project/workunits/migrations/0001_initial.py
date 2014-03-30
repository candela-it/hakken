# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WorkUnit'
        db.create_table(u'workunits_workunit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('x', self.gf('django.db.models.fields.IntegerField')()),
            ('y', self.gf('django.db.models.fields.IntegerField')()),
            ('z', self.gf('django.db.models.fields.IntegerField')()),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('locked', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'workunits', ['WorkUnit'])

        # Adding model 'Solution'
        db.create_table(u'workunits_solution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workunit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workunits.WorkUnit'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Answer'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'workunits', ['Solution'])


    def backwards(self, orm):
        # Deleting model 'WorkUnit'
        db.delete_table(u'workunits_workunit')

        # Deleting model 'Solution'
        db.delete_table(u'workunits_solution')


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
        u'projects.answer': {
            'Meta': {'object_name': 'Answer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'projects.answerorder': {
            'Meta': {'object_name': 'AnswerOrder'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Answer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Iteration']"}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'projects.iteration': {
            'Meta': {'object_name': 'Iteration'},
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['projects.Answer']", 'through': u"orm['projects.AnswerOrder']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'projects.iterationstep': {
            'Meta': {'object_name': 'IterationStep'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Iteration']"}),
            'iteration_step': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Workflow']"})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'area_of_interest': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_zoom': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'deleted'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Workflow']"})
        },
        u'projects.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iteration': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['projects.Iteration']", 'through': u"orm['projects.IterationStep']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'workunits.solution': {
            'Meta': {'object_name': 'Solution'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Answer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'workunit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workunits.WorkUnit']"})
        },
        u'workunits.workunit': {
            'Meta': {'object_name': 'WorkUnit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'x': ('django.db.models.fields.IntegerField', [], {}),
            'y': ('django.db.models.fields.IntegerField', [], {}),
            'z': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['workunits']