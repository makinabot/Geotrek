# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Trek.date_insert'
        db.delete_column('itineraire', 'date_insert')

        # Deleting field 'Trek.date_update'
        db.delete_column('itineraire', 'date_update')

        # Deleting field 'Trek.id'
        db.delete_column('itineraire', 'id')

        # Deleting field 'Trek.geom'
        db.delete_column('itineraire', 'geom')

        # Deleting field 'Trek.deleted'
        db.delete_column('itineraire', 'deleted')

        # Deleting field 'Trek.length'
        db.delete_column('itineraire', 'length')

        # Adding field 'Trek.topology_ptr'
        db.add_column('itineraire', 'topology_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['core.Topology'], unique=True, primary_key=True),
                      keep_default=False)

        # Removing M2M table for field paths on 'Trek'
        db.delete_table('itineraire_paths')


    def backwards(self, orm):
        # Adding field 'Trek.date_insert'
        db.add_column('itineraire', 'date_insert',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 8, 16, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Trek.date_update'
        db.add_column('itineraire', 'date_update',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 8, 16, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Trek.id'
        db.add_column('itineraire', 'id',
                      self.gf('django.db.models.fields.AutoField')(default=datetime.datetime(2012, 8, 16, 0, 0), primary_key=True),
                      keep_default=False)

        # Adding field 'Trek.geom'
        db.add_column('itineraire', 'geom',
                      self.gf('django.contrib.gis.db.models.fields.LineStringField')(srid=settings.SRID, dim=3, default='', spatial_index=False),
                      keep_default=False)

        # Adding field 'Trek.deleted'
        db.add_column('itineraire', 'deleted',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Trek.length'
        db.add_column('itineraire', 'length',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Deleting field 'Trek.topology_ptr'
        db.delete_column('itineraire', 'topology_ptr_id')

        # Adding M2M table for field paths on 'Trek'
        db.create_table('itineraire_paths', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('trek', models.ForeignKey(orm['trekking.trek'], null=False)),
            ('path', models.ForeignKey(orm['core.path'], null=False))
        ))
        db.create_unique('itineraire_paths', ['trek_id', 'path_id'])


    models = {
        'authent.structure': {
            'Meta': {'object_name': 'Structure'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'core.datasource': {
            'Meta': {'object_name': 'Datasource', 'db_table': "'source_donnees'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']"})
        },
        'core.network': {
            'Meta': {'object_name': 'Network', 'db_table': "'reseau_troncon'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']"})
        },
        'core.path': {
            'Meta': {'object_name': 'Path', 'db_table': "'troncons'"},
            'ascent': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'denivelee_positive'"}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'remarques'", 'blank': 'True'}),
            'datasource': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paths'", 'null': 'True', 'to': "orm['core.Datasource']"}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {}),
            'descent': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'denivelee_negative'"}),
            'geom': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '%s' % settings.SRID, 'dim': '3', 'spatial_index': 'False'}),
            'geom_cadastre': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '%s' % settings.SRID, 'dim': '3', 'null': 'True', 'spatial_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_column': "'longueur'"}),
            'max_elevation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'altitude_maximum'"}),
            'min_elevation': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'altitude_minimum'"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'db_column': "'nom_troncon'", 'blank': 'True'}),
            'networks': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'paths'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Network']"}),
            'stake': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paths'", 'null': 'True', 'to': "orm['core.Stake']"}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']"}),
            'trail': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'paths'", 'null': 'True', 'to': "orm['core.Trail']"}),
            'usages': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'paths'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['core.Usage']"}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_column': "'troncon_valide'"})
        },
        'core.pathaggregation': {
            'Meta': {'object_name': 'PathAggregation', 'db_table': "'e_r_evenement_troncon'"},
            'end_position': ('django.db.models.fields.FloatField', [], {'db_column': "'pk_fin'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aggregations'", 'db_column': "'troncon'", 'to': "orm['core.Path']"}),
            'start_position': ('django.db.models.fields.FloatField', [], {'db_column': "'pk_debut'"}),
            'topo_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'aggregations'", 'db_column': "'evenement'", 'to': "orm['core.Topology']"})
        },
        'core.stake': {
            'Meta': {'object_name': 'Stake', 'db_table': "'enjeu'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stake': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']"})
        },
        'core.topology': {
            'Meta': {'object_name': 'Topology', 'db_table': "'e_t_evenement'"},
            'date_insert': ('django.db.models.fields.DateTimeField', [], {}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'supprime'"}),
            'geom': ('django.contrib.gis.db.models.fields.LineStringField', [], {'srid': '%s' % settings.SRID, 'dim': '3', 'spatial_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.TopologyKind']"}),
            'length': ('django.db.models.fields.FloatField', [], {'default': '0', 'db_column': "'longueur'"}),
            'offset': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'decallage'"}),
            'troncons': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Path']", 'through': "orm['core.PathAggregation']", 'symmetrical': 'False'})
        },
        'core.topologykind': {
            'Meta': {'object_name': 'TopologyKind', 'db_table': "'type_evenements'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'core.trail': {
            'Meta': {'object_name': 'Trail', 'db_table': "'sentier'"},
            'arrival': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'comments': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'departure': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']"})
        },
        'core.usage': {
            'Meta': {'object_name': 'Usage', 'db_table': "'usage'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'structure': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['authent.Structure']"}),
            'usage': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'trekking.destination': {
            'Meta': {'object_name': 'Destination', 'db_table': "'destination'"},
            'destination': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'destination_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'destination_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'destination_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pictogram': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'trekking.difficultylevel': {
            'Meta': {'object_name': 'DifficultyLevel', 'db_table': "'classement_difficulte'"},
            'difficulty': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'difficulty_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'difficulty_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'difficulty_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'trekking.poi': {
            'Meta': {'object_name': 'POI', '_ormbases': ['core.Topology']},
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'topo_object': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Topology']", 'unique': 'True', 'primary_key': 'True', 'db_column': "'evenement'"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pois'", 'to': "orm['trekking.POIType']"})
        },
        'trekking.poitype': {
            'Meta': {'object_name': 'POIType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'label_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'label_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'label_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'pictogram': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'trekking.route': {
            'Meta': {'object_name': 'Route', 'db_table': "'parcours'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'route_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'route_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'route_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'trekking.trek': {
            'Meta': {'object_name': 'Trek', 'db_table': "'itineraire'", '_ormbases': ['core.Topology']},
            'advice': ('django.db.models.fields.TextField', [], {}),
            'advice_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'advice_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'advice_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'advised_parking': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ambiance': ('django.db.models.fields.TextField', [], {}),
            'ambiance_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ambiance_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ambiance_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'arrival': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'arrival_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'arrival_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'arrival_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'ascent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'departure': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'departure_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'departure_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'departure_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'descent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_teaser': ('django.db.models.fields.TextField', [], {}),
            'description_teaser_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_teaser_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_teaser_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'treks'", 'null': 'True', 'to': "orm['trekking.Destination']"}),
            'difficulty': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'treks'", 'null': 'True', 'to': "orm['trekking.DifficultyLevel']"}),
            'disabled_infrastructure': ('django.db.models.fields.TextField', [], {}),
            'disabled_infrastructure_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disabled_infrastructure_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disabled_infrastructure_it': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {}),
            'is_park_centered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_transborder': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_elevation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'min_elevation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'networks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'treks'", 'symmetrical': 'False', 'to': "orm['trekking.TrekNetwork']"}),
            'parking_location': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '%s' % settings.SRID, 'spatial_index': 'False'}),
            'public_transport': ('django.db.models.fields.TextField', [], {}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'treks'", 'null': 'True', 'to': "orm['trekking.Route']"}),
            'topology_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Topology']", 'unique': 'True', 'primary_key': 'True'}),
            'usages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'treks'", 'symmetrical': 'False', 'to': "orm['trekking.Usage']"}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'web_links': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'treks'", 'symmetrical': 'False', 'to': "orm['trekking.WebLink']"})
        },
        'trekking.treknetwork': {
            'Meta': {'object_name': 'TrekNetwork', 'db_table': "'reseau'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'network_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'network_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'network_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'trekking.trekrelationship': {
            'Meta': {'unique_together': "(('trek_a', 'trek_b'),)", 'object_name': 'TrekRelationship', 'db_table': "'liens_itineraire'"},
            'has_common_departure': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_common_edge': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_circuit_step': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'trek_a': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trek_relationship_a'", 'to': "orm['trekking.Trek']"}),
            'trek_b': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trek_relationship_b'", 'to': "orm['trekking.Trek']"})
        },
        'trekking.usage': {
            'Meta': {'object_name': 'Usage', 'db_table': "'usages'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'usage': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'usage_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'usage_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'usage_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'trekking.weblink': {
            'Meta': {'object_name': 'WebLink', 'db_table': "'liens_web'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['trekking']