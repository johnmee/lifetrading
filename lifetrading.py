#!/usr/bin/python3
"""Monitor a directory and import csv files to a database when they arrive.

For usage:
    ./lifetrading.py --help

Detects new/updated csv files in the path and import them into the database.
"""
import argparse
import csv
import logging
import os
import sys
import time

import dataset


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')


class FileLog:
    """A database of files in a directory.

    Keeps a record of every relevant file that was found in the directory.
    """
    # Status choices.
    CREATED = 'CREATED'
    UPDATED = 'UPDATED'
    IMPORTED = 'IMPORTED'

    def __init__(self, dbstring):
        """Connect to the database.

        Args:
            dbstring (str): A database url that dataset understands.
        """
        self.db = dataset.connect(dbstring)
        self._table = None

    @property
    def table(self):
        """The database table.

        Returns:
            dataset.Table: Table of file records.
        """
        return self._table or self._create_table()

    def _create_table(self):
        """Create the filelog database table.

        Returns:
            dataset.Table: Table of file records.
        """
        table = self.db.create_table('filelog')
        table.create_column('name', self.db.types.string)
        table.create_column('mtime', self.db.types.bigint)
        table.create_column('status', self.db.types.string)
        table.create_index(['name', 'mtime', 'status'])
        self._table = table
        return table

    @property
    def queued(self):
        """Set of filenames that are waiting to be imported.

        Returns:
             set of str: set of filenames.
        """
        # TODO: Include UPDATED files in the resultset.
        return set(file['name'] for file in
                   self.table.find(status=FileLog.CREATED, order_by=['mtime']))

    def find(self, filename):
        """Find records in the database associated with a filename.

        Args:
            filename (str): The name of the file to search for.

        Returns:
             list of OrderedDict: the relevant rows from the database.
        """
        return list(self.table.find(name=filename))

    def upsert(self, direntry):
        """Add, or update, a file record in the database.

        Args:
            os.Direntry: the directory entry of the file.

        Returns:
            int: the row id of the record.
        """
        mtime = direntry.stat().st_mtime_ns
        if len(self.find(direntry.name)) == 0:
            data = dict(name=direntry.name, mtime=mtime, status=FileLog.CREATED)
            row_id = self.table.insert(data)
        else:
            data = dict(name=direntry.name, mtime=mtime, status=FileLog.UPDATED)
            row_id = self.table.update(data, ['name'])
        return row_id

    def set_imported(self, filename):
        """Change status of the file to IMPORTED.

        Args:
            filename (str): Name of the file to change status.
        """
        data = dict(name=filename, status=FileLog.IMPORTED)
        self.table.update(data, ['name'])


class TradeActivity:
    """Database of trade activity.

    Keeps a record of every trade that has occured.
    """
    def __init__(self, dbstring):
        """Connect and create the database table.

        Args:
            dbstring (str): the database connection URL.
        """
        self.db = dataset.connect(dbstring)
        self.table = self.db['tradeactivity']

    def import_csv(self, filename):
        """Import Trade Activity from the file.

        Loads every row of the file into the database.

        Args:
            filename (str): the name of the file to import.

        Returns:
            int: The number of rows imported.
        """
        with open(filename) as infile:
            reader = csv.DictReader(infile)
            rows = list(reader)
            self.table.insert_many(rows)
        return len(rows)

    def all(self):
        """Returns every row in the table."""
        return self.table.all()

    @staticmethod
    def match(filename):
        """True if the filename matches a trade activity csv.

        Example:
            TradeActivityReport-LIFETRADING-20181004-0500561.csv

        Returns:
            bool: True when the filename matches a trade activity report.
        """
        try:
            root, ext = os.path.splitext(filename)
            (report_type, account, trade_date, gen_time) = root.split('-')
        except ValueError:
            return False
        return report_type == 'TradeActivityReport' and ext == '.csv'


def get_csv_files(path):
    """Get all the CSV files in the path.

    Args:
        path (str or path-like object): The directory to examine.

    Returns:
         list of DirEntry: All the csv files in the path.
    """
    csv_files = []
    try:
        for direntry in os.scandir(path):
            if direntry.is_file and direntry.name.endswith('.csv'):
                csv_files.append(direntry)
    except FileNotFoundError:
        pass
    logging.debug('CsvFiles: %s', ', '.join([file.name for file in csv_files]))
    return csv_files


def main(path, dbstring):
    """Import the files in path to the database.

    Args:
          path (str or path-like object): The directory to import files from.
          dbstring (str): Database URL of database to use.

    Returns:
          int: a count of the files imported.
    """
    # Fetch all the csv files and update the filelog database.
    csv_files = get_csv_files(path)
    filelog = FileLog(dbstring)
    for entry in csv_files:
        filelog.upsert(entry)

    # Import all the unimported files.
    num_files_processed = 0
    trade_activity = TradeActivity(dbstring)
    for filename in filelog.queued:
        if TradeActivity.match(filename):
            rowcount = trade_activity.import_csv(os.path.join(path, filename))
            filelog.set_imported(filename)
            logging.info('Imported %s rows from %s', rowcount, filename)
            num_files_processed += 1

    logging.debug(list(filelog.table.all()))
    logging.debug(list(trade_activity.table.all()))
    return num_files_processed


if __name__ == '__main__':
    """Execution from the commandline.
    
    An endless loop which must be interrupted by Keyboard:
        1. Import new/updated files.
        2. If no files were processed, take a nap.
    """
    parser = argparse.ArgumentParser(
        description='Data Import task for lifetrading.com.au')
    parser.add_argument('db_string', help='Database connection string.')
    parser.add_argument('download_path',
                        help='Path to the download directory.')
    parser.add_argument('poll_seconds', type=int,
                        help='Number of seconds to sleep when nothing to do.')
    args = parser.parse_args()

    logging.info('Starting: Path "%s" DB "%s" Poll %s',
                 args.download_path, args.db_string, args.poll_seconds)
    try:
        while True:
            filecount = main(args.download_path, args.db_string)
            if filecount == 0:
                time.sleep(args.poll_seconds)
    except KeyboardInterrupt:
        logging.info('Stopping: Keyboard Interrupt')
