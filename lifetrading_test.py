import dataset
import lifetrading
import os
import tempfile
import unittest
from unittest import mock


DB_SQLITE_MEMORY = 'sqlite:///:memory:'


def create_file(directory, filename, content='Test\n'):
    fullpath = os.path.join(directory, filename)
    fh = open(fullpath, 'w')
    fh.write(content)
    fh.close()
    return fullpath


class LifetradingTestcase(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing.
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.test_dir.cleanup()

    def test_get_csv_files(self):
        """Test the detection of CSV files in a directory."""
        # An empty directory has no csv files.
        self.assertEqual(lifetrading.get_csv_files(self.test_dir.name), [])

        # A non-csv file is not detected.
        create_file(self.test_dir.name, 'foo.txt')
        self.assertEqual(lifetrading.get_csv_files(self.test_dir.name), [])

        # One csv file is detected.
        create_file(self.test_dir.name, 'foo.csv')
        csv_files = lifetrading.get_csv_files(self.test_dir.name)
        self.assertEqual(['foo.csv'], [file.name for file in csv_files])

        # Two csv files are detected.
        create_file(self.test_dir.name, 'bar.csv')
        csv_files = lifetrading.get_csv_files(self.test_dir.name)
        self.assertSetEqual({'foo.csv', 'bar.csv'},
                            set([file.name for file in csv_files]))

    def test_filelog(self):
        """Test the recording of files in the FileLog."""
        filelog = lifetrading.FileLog(DB_SQLITE_MEMORY)
        # File not found returns an empty iterator.
        self.assertEqual([], list(filelog.find('nothere.txt')))
        self.assertEqual([], list(filelog.queued))

        # Create a file and record it.
        mock_direntry = mock.Mock()
        mock_direntry.name = 'fake.csv'
        mock_direntry.stat.return_value.st_mtime_ns = 100
        filelog.upsert(mock_direntry)
        records = filelog.find('fake.csv')
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record['name'], 'fake.csv')
        self.assertEqual(record['mtime'], 100)
        self.assertEqual(record['status'], filelog.CREATED)

        # Create a second file and ensure the two files remain distinct.
        mock_direntry.name = 'another.csv'
        mock_direntry.stat.return_value.st_mtime_ns = 200
        filelog.upsert(mock_direntry)
        records = filelog.find('another.csv')
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record['name'], 'another.csv')
        self.assertEqual(record['mtime'], 200)
        self.assertEqual(record['status'], filelog.CREATED)

        records = filelog.find('fake.csv')
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record['name'], 'fake.csv')
        self.assertEqual(record['mtime'], 100)
        self.assertEqual(record['status'], filelog.CREATED)

        # A couple of files are now queued.
        self.assertSetEqual(filelog.queued, {'fake.csv', 'another.csv'})

        # Mark one imported.
        filelog.set_imported('fake.csv')
        self.assertSetEqual(filelog.queued, {'another.csv'})

    def test_tradeactivity_match(self):
        """Test idenfication and import of TradeActivity files."""
        self.assertFalse(lifetrading.TradeActivity.match('foo.csv'))
        self.assertFalse(lifetrading.TradeActivity.match('trade-report.csv'))
        self.assertFalse(lifetrading.TradeActivity.match(
            'TradeActivityReport-.csv'))
        self.assertFalse(lifetrading.TradeActivity.match(
            'SomeOtherReport-LIFETRADING-20191004-019323.csv'))
        self.assertTrue(lifetrading.TradeActivity.match(
            'TradeActivityReport-LIFETRADING-20181004-0500561.csv'))

    def test_tradeactivity_import(self):
        """Test importing a trade activity file."""
        filename = 'TradeActivityReport-LIFETRADING-20181004-0500561.csv'
        csv_data = ('Column1,Column2,Column3\n' 
                    'data1,data2,data3\n'
                    'data4,data5,data6\n')
        test_file = create_file(self.test_dir.name, filename, csv_data)
        trade_activity = lifetrading.TradeActivity(DB_SQLITE_MEMORY)
        trade_activity.import_csv(test_file)

        result = list(trade_activity.all())
        self.assertEqual(2, len(result))
        self.assertEqual(result[0]['Column1'], 'data1')
        self.assertEqual(result[0]['Column2'], 'data2')
        self.assertEqual(result[1]['Column3'], 'data6')


class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing.
        self.test_dir = tempfile.TemporaryDirectory()
        self.db_file = 'test_db.sqlite'
        self.db_string = 'sqlite:///%s' % self.db_file

    def tearDown(self):
        self.test_dir.cleanup()
        os.remove(self.db_file)

    def test_main(self):
        db = dataset.connect(self.db_string)
        filelog_table = db['filelog']
        trade_table = db['tradeactivity']

        # Start with nothing.
        import_count = lifetrading.main(self.test_dir.name, self.db_string)
        self.assertEqual(0, import_count)
        self.assertCountEqual([], trade_table.all())
        self.assertCountEqual([], filelog_table.all())

        # Drop in a non-processing file.
        test_file = create_file(self.test_dir.name, 'nonsense.file')
        import_count = lifetrading.main(self.test_dir.name, self.db_string)
        self.assertEqual(0, import_count)
        self.assertCountEqual([], trade_table.all())
        self.assertCountEqual([], filelog_table.all())

        # Drop in a trade activity file.
        filename = 'TradeActivityReport-LIFETRADING-1-1.csv'
        csv_data = ('Column1,Column2,Column3\n' 
                    'data1,data2,data3\n'
                    'data4,data5,data6\n')
        test_file = create_file(self.test_dir.name, filename, csv_data)
        import_count = lifetrading.main(self.test_dir.name, self.db_string)
        self.assertEqual(1, import_count)
        self.assertEqual(2, len(list(trade_table.all())))
        filelog_records = list(filelog_table.find(name=filename))
        self.assertEqual(1, len(filelog_records))
        self.assertEqual(lifetrading.FileLog.IMPORTED,
                         filelog_records[0]['status'])

        # Skip imported files.
        import_count = lifetrading.main(self.test_dir.name, self.db_string)
        self.assertEqual(0, import_count)
