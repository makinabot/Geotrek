from django.test import TestCase
from django.conf import settings
from django.contrib.gis.geos import LineString
from django.db import connections, DEFAULT_DB_ALIAS, IntegrityError
from django.utils.translation import ugettext_lazy as _

from geotrek.common.tests import CommonTest

from geotrek.common.utils import dbnow
from geotrek.authent.factories import UserFactory, PathManagerFactory, StructureFactory
from geotrek.authent.models import Structure, default_structure
from geotrek.core.factories import (PathFactory, StakeFactory, TrailFactory, ComfortFactory)
from geotrek.core.models import Path


class ViewsTest(CommonTest):
    model = Path
    modelfactory = PathFactory
    userfactory = PathManagerFactory

    def get_bad_data(self):
        return {'geom': '{"geom": "LINESTRING (0.0 0.0, 1.0 1.0)"}'}, _("Linestring invalid snapping.")

    def get_good_data(self):
        return {
            'name': '',
            'structure': default_structure().pk,
            'stake': '',
            'comfort': ComfortFactory.create().pk,
            'trail': '',
            'comments': '',
            'departure': '',
            'arrival': '',
            'datasource': '',
            'valid': 'on',
            'geom': '{"geom": "LINESTRING (99.0 89.0, 100.0 88.0)", "snap": [null, null]}',
        }

    def _post_add_form(self):
        # Avoid overlap, delete all !
        for p in Path.objects.all():
            p.delete()
        super(ViewsTest, self)._post_add_form()

    def test_structurerelated_filter(self):
        def test_structure(structure, stake):
            user = self.userfactory(password='booh')
            p = user.profile
            p.structure = structure
            p.save()
            success = self.client.login(username=user.username, password='booh')
            self.assertTrue(success)
            response = self.client.get(Path.get_add_url())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('form' in response.context)
            form = response.context['form']
            self.assertTrue('stake' in form.fields)
            stakefield = form.fields['stake']
            self.assertTrue((stake.pk, unicode(stake)) in stakefield.choices)
            self.client.logout()
        # Test for two structures
        s1 = StructureFactory.create()
        s2 = StructureFactory.create()
        st1 = StakeFactory.create(structure=s1)
        StakeFactory.create(structure=s1)
        st2 = StakeFactory.create(structure=s2)
        StakeFactory.create(structure=s2)
        test_structure(s1, st1)
        test_structure(s2, st2)


# FIXME: this test has random results (as reported by Hudson)
#class StakeTest(TestCase):
#    def test_comparison(self):
#        low = StakeFactory.create()
#        high = StakeFactory.create()
#        # In case SERIAL field was reinitialized
#        if high.pk < low.pk:
#            tmp = high
#            high = low
#            low = tmp
#            self.assertTrue(low.pk < high.pk)
#        self.assertTrue(low < high)
#        self.assertTrue(low <= high)
#        self.assertFalse(low > high)
#        self.assertFalse(low >= high)
#        self.assertFalse(low == high)


class PathTest(TestCase):
    def test_paths_bystructure(self):
        user = UserFactory()
        p1 = PathFactory()
        p2 = PathFactory(structure=Structure.objects.create(name="other"))

        self.assertEqual(user.profile.structure, p1.structure)
        self.assertNotEqual(user.profile.structure, p2.structure)

        self.assertEqual(len(Structure.objects.all()), 2)
        self.assertEqual(len(Path.objects.all()), 2)

        self.assertEqual(Path.in_structure.for_user(user)[0], Path.for_user(user)[0])
        self.assertTrue(p1 in Path.in_structure.for_user(user))
        self.assertFalse(p2 in Path.in_structure.for_user(user))

        # Change user structure on-the-fly
        profile = user.profile
        profile.structure = p2.structure
        profile.save()

        self.assertEqual(user.profile.structure.name, "other")
        self.assertFalse(p1 in Path.in_structure.for_user(user))
        self.assertTrue(p2 in Path.in_structure.for_user(user))

    def test_dates(self):
        t1 = dbnow()
        p = PathFactory()
        t2 = dbnow()
        self.assertTrue(t1 < p.date_insert < t2,
                        msg='Date interval failed: %s < %s < %s' % (
                            t1, p.date_insert, t2
                        ))

        p.name = "Foo"
        p.save()
        t3 = dbnow()
        self.assertTrue(t2 < p.date_update < t3,
                        msg='Date interval failed: %s < %s < %s' % (
                            t2, p.date_update, t3
                       ))

    def test_elevation(self):
        # Create a simple fake DEM
        conn = connections[DEFAULT_DB_ALIAS]
        cur = conn.cursor()
        cur.execute('CREATE TABLE mnt (rid serial primary key, rast raster)')
        cur.execute('INSERT INTO mnt (rast) VALUES (ST_MakeEmptyRaster(3, 3, 0, 3, 1, -1, 0, 0, %s))', [settings.SRID])
        cur.execute('UPDATE mnt SET rast = ST_AddBand(rast, \'16BSI\')')
        for x in range(1, 4):
            for y in range(1, 4):
                cur.execute('UPDATE mnt SET rast = ST_SetValue(rast, %s, %s, %s::float)', [x, y, x+y])
        conn.commit_unless_managed()

        # Create a geometry and check elevation-based indicators
        p = Path(geom=LineString((1.5,1.5,0), (2.5,1.5,0), (1.5,2.5,0)))
        self.assertEqual(p.ascent, 0)
        self.assertEqual(p.descent, 0)
        self.assertEqual(p.min_elevation, 0)
        self.assertEqual(p.max_elevation, 0)
        p.save()
        self.assertEqual(p.ascent, 1)
        self.assertEqual(p.descent, -2)
        self.assertEqual(p.min_elevation, 3)
        self.assertEqual(p.max_elevation, 5)

        # Check elevation profile
        profile = p.get_elevation_profile()
        self.assertEqual(len(profile), 3)
        self.assertEqual(profile[0][0], 0.0)
        self.assertEqual(profile[0][1], 4)
        self.assertTrue(1.4 < profile[1][0] < 1.5)
        self.assertEqual(profile[1][1], 5)
        self.assertTrue(3.8 < profile[2][0] < 3.9)
        self.assertEqual(profile[2][1], 3)

    def test_length(self):
        p = PathFactory.build()
        self.assertEqual(p.length, 0)
        p.save()
        self.assertNotEqual(p.length, 0)

    def test_delete_cascade(self):
        from geotrek.trekking.models import Trek
        from geotrek.trekking.factories import TrekFactory

        p1 = PathFactory.create()
        p2 = PathFactory.create()
        t = TrekFactory.create(no_path=True)
        t.add_path(p1)
        t.add_path(p2)

        # Everything should be all right before delete
        self.assertTrue(t.published)
        self.assertFalse(t.deleted)
        self.assertEqual(t.aggregations.count(), 2)

        # When a path is deleted
        p1.delete()
        t = Trek.objects.get(pk=t.pk)
        self.assertFalse(t.published)
        self.assertFalse(t.deleted)
        self.assertEqual(t.aggregations.count(), 1)

        # Reset published status
        t.published = True
        t.save()

        # When all paths are deleted
        p2.delete()
        t = Trek.objects.get(pk=t.pk)
        self.assertFalse(t.published)
        self.assertTrue(t.deleted)
        self.assertEqual(t.aggregations.count(), 0)

    def test_valid_geometry(self):
        connection = connections[DEFAULT_DB_ALIAS]

        # Create path with self-intersection
        p = PathFactory.build(geom=LineString((0,0,0),(2,0,0),(1,1,0),(1,-1,0)))
        self.assertRaises(IntegrityError, p.save)
        # FIXME: Why a regular transaction.rollback does not work???
        connection.close() # Clear DB exception at psycopg level

        # Fix self-intersection
        p.geom = LineString((0,0,0),(2,0,0),(1,1,0))
        p.save()

        # Update with self-intersection
        p.geom = LineString((0,0,0),(2,0,0),(1,1,0),(1,-1,0))
        self.assertRaises(IntegrityError, p.save)
        connection.close() # Clear DB exception at psycopg level

    def test_overlap_geometry(self):
        PathFactory.create(geom=LineString((0,0,0),(60,0,0)))
        p = PathFactory.create(geom=LineString((40,0,0),(50,0,0)))
        self.assertTrue(p.is_overlap())
        # Overlaping twice
        p = PathFactory.create(geom=LineString((20,1,0),(20,0,0),(25,0,0),(25,1,0),
                                              (30,1,0),(30,0,0),(35,0,0),(35,1,0)))
        self.assertTrue(p.is_overlap())

        # But crossing is ok
        p = PathFactory.create(geom=LineString((6,1,0),(6,3,0)))
        self.assertFalse(p.is_overlap())
        # Touching is ok too
        p = PathFactory.create(geom=LineString((5,1,0),(5,0,0)))
        self.assertFalse(p.is_overlap())
        # Touching twice is ok too
        p = PathFactory.create(geom=LineString((2.5,0,0),(3,1,0),(3.5,0,0)))
        self.assertFalse(p.is_overlap())

        """
        I gave up with the idea of checking "almost overlaping" (and touching)...
        """
        # Almost overlaping fails also
        #PathFactory.create(geom=LineString((0,0,0),(60,0,0)))
        #p = PathFactory.build(geom=LineString((20,0.5,0),(30,0.5,0)))
        #self.assertRaises(IntegrityError, p.save)
        #connection.close()
        # Almost touching is also ok
        #PathFactory.create(geom=LineString((4,1,0),(4,0.5,0)))
        # Almost touching twice is also ok
        #PathFactory.create(geom=LineString((0.5,1,0),(1,1,0),(1.5,1,0)))


class TrailTest(TestCase):

    def test_geom(self):
        t = TrailFactory.create()
        self.assertTrue(t.geom is None)
        p = PathFactory.create()
        t.paths.add(p)
        self.assertFalse(t.geom is None)
