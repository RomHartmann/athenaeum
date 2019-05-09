import unittest

import testing.mysqld
import testing.postgresql
from sqlalchemy import create_engine

# prevent generating brand new db every time.  Speeds up tests.
PS_FACTORY = testing.postgresql.PostgresqlFactory(port=7654)
MYSQLD_FACTORY = testing.mysqld.MysqldFactory(cache_initialized_db=True, port=7531)


def tearDownModule():
    """Tear down databases after test script has run.

    https://docs.python.org/3/library/unittest.html#setupclass-and-teardownclass
    """
    # clear cached database at end of tests
    PS_FACTORY.clear_cache()
    MYSQLD_FACTORY.clear_cache()


class TestEtl(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create source postgres database, table and data
        #    We are creating a postgres database (instead of just sqlite) because `config` is json type.
        cls.postgresql = PS_FACTORY()
        cls.source_conn = create_engine(cls.postgresql.url()).connect()

        # create target db and table
        cls.mysql = MYSQLD_FACTORY()
        cls.target_conn = create_engine(cls.mysql.url()).connect()

    def setUp(self):
        self.postgresql.start()
        self.source_conn.execute("""
            CREATE TABLE foo (
                created_at TIMESTAMP(6) NOT NULL,
                id INT NOT NULL
            )
        """)

        self.mysql.start()
        self.target_conn.execute("""
            CREATE TABLE `bar` (
                Date TIMESTAMP(6) NOT NULL,
                id INT NOT NULL
            INDEX Date (Date)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
        """)

    def tearDown(self):
        self.source_conn.execute("DROP TABLE foo")
        self.target_conn.execute("DROP TABLE bar")

    @classmethod
    def tearDownClass(cls):
        cls.postgresql.stop()
        cls.mysql.stop()

    def test_something(self):
        """A simple test to check expected output"""
        resp = self.target_conn.execute("SELECT * FROM bar")
        cols = resp.keys()
        vals = resp.fetchall()
