"""
    http://djangosnippets.org/snippets/2311/
    Ensure South will update our custom SQL during a call to `migrate`.
"""
import os
import re
import logging
import traceback

from django.db import connection, transaction, models
from django.conf import settings

from south.signals import post_migrate

logger = logging.getLogger(__name__)


def run_initial_sql(sender, **kwargs):
    app_label = kwargs.get('app')
    app_dir = os.path.normpath(os.path.join(os.path.dirname(
                               models.get_app(app_label).__file__), 'sql'))
    if not os.path.exists(app_dir):
        return

    r = re.compile(r'^.*\.sql$')
    sql_files = [os.path.join(app_dir, f)
                 for f in os.listdir(app_dir)
                 if r.match(f) is not None]
    sql_files.sort()
    cursor = connection.cursor()
    for sql_file in sql_files:
        try:
            logger.info("Loading initial SQL data from '%s'" % sql_file)
            f = open(sql_file)
            sql = f.read()
            f.close()
            if not settings.TEST:
                # Remove RAISE NOTICE (/!\ only one-liners)
                sql = re.sub(r"\n.*RAISE NOTICE.*\n", "\n", sql)
                # TODO: this is the ugliest driver hack ever
                sql = sql.replace('%', '%%')
            cursor.execute(sql)
        except Exception as e:
            print sql
            logger.error("Failed to install custom SQL file '%s': %s\n" %
                         (sql_file, e))
            traceback.print_exc()
            transaction.rollback_unless_managed()
            raise
        else:
            transaction.commit_unless_managed()

post_migrate.connect(run_initial_sql, dispatch_uid="geotrek.core.sqlautoload")
