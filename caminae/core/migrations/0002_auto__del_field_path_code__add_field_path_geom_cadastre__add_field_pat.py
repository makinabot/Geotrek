# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Path.code'
        db.delete_column('troncons', 'code')

        # Adding field 'Path.geom_cadastre'
        db.add_column('troncons', 'geom_cadastre',
                      self.gf('django.contrib.gis.db.models.fields.LineStringField')(srid=2154, null=True, spatial_index=False),
                      keep_default=False)

        # Adding field 'Path.comments'
        db.add_column('troncons', 'comments',
                      self.gf('django.db.models.fields.TextField')(null=True, db_column='remarques'),
                      keep_default=False)


        # Changing field 'Path.date_update'
        db.alter_column('troncons', 'date_update', self.gf('django.db.models.fields.DateField')(auto_now=True))

        # Changing field 'Path.date_insert'
        db.alter_column('troncons', 'date_insert', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

        # Renaming column for 'Path.name' to match new field type.
        db.rename_column('troncons', 'nom', 'nom_troncon')
        # Changing field 'Path.name'
        db.alter_column('troncons', 'nom_troncon', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, db_column='nom_troncon'))

    def backwards(self, orm):
        # Adding field 'Path.code'
        db.add_column('troncons', 'code',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True),
                      keep_default=False)

        # Deleting field 'Path.geom_cadastre'
        db.delete_column('troncons', 'geom_cadastre')

        # Deleting field 'Path.comments'
        db.delete_column('troncons', 'remarques')


        # Changing field 'Path.date_update'
        db.alter_column('troncons', 'date_update', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Path.date_insert'
        db.alter_column('troncons', 'date_insert', self.gf('django.db.models.fields.DateField')())

        # Renaming column for 'Path.name' to match new field type.
        db.rename_column('troncons', 'nom_troncon', 'nom')
        # Changing field 'Path.name'
        db.alter_column('troncons', 'nom', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, db_column='nom'))

    models = {
        'core.path': {
            'Meta': {'object_name': 'Path', 'db_table': "'troncons'"},
            'ascent': ('django.db.models.fields.IntegerField', [], {'db_column': "'denivelee_positive'"}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'remarques'"}),
            'date_insert': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'descent': ('django.db.models.fields.IntegerField', [], {'db_column': "'denivelee_negative'"}),
            'geom': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '2154', 'spatial_index': 'False'}),
            'geom_cadastre': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '2154', 'null': 'True', 'spatial_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'db_column': "'longueur'"}),
            'max_elevation': ('django.db.models.fields.IntegerField', [], {'db_column': "'altitude_maximum'"}),
            'min_elevation': ('django.db.models.fields.IntegerField', [], {'db_column': "'altitude_minimum'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'nom_troncon'"}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'troncon_valide'"})
        },
        'core.pathaggregation': {
            'Meta': {'object_name': 'PathAggregation', 'db_table': "'evenements_troncons'"},
            'end_position': ('django.db.models.fields.FloatField', [], {'db_column': "'pk_fin'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Path']", 'db_column': "'troncon'"}),
            'start_position': ('django.db.models.fields.FloatField', [], {'db_column': "'pk_debut'"}),
            'topo_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.TopologyMixin']", 'db_column': "'evenement'"})
        },
        'core.topologymixin': {
            'Meta': {'object_name': 'TopologyMixin', 'db_table': "'evenements'"},
            'date_insert': ('django.db.models.fields.DateField', [], {}),
            'date_update': ('django.db.models.fields.DateField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'supprime'"}),
            'geom': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '2154', 'spatial_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'db_column': "'longueur'"}),
            'offset': ('django.db.models.fields.IntegerField', [], {'db_column': "'decallage'"}),
            'troncons': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Path']", 'through': "orm['core.PathAggregation']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['core']