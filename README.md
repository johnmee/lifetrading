# Life Trading Exercise

John Mee 31-Jul-2019

## Data Import Task

* Your task is to design a general process to import external csv files into a database
* You will need to specify the database schema, feel free to use what you see as the most appropriate
database technology
* You will need to provide code to process files and import them to the database, feel free to use any
language that fits well with your choice of database technology
* You will need to document how you see the process running in an automated way so that files are
processed within 10 minutes of their arrival

The requirements are as follows
* New file reports are dropped into a local folder at regular times in the day
* Multiple types of reports may be dropped into this folder
* Each file should be processed, and a status recorded to the database to say they have
arrived
* For specific report types, the contents of the file should also be imported into the database
and the status updated to imported
* You are free to add any additional status values as appropriate
* The modification time of the file represents the download date/time, this should be
recorded to the database
* Each report type has a specific filename pattern, this includes the report type but also
additional information relating to that file. There will always be a trade date encoded in the
filename.
* Different report types may have different filename patterns
* Each report type has a different set of columns, all columns should be imported

Bonus requirement
* Each report may be revised during the day, the prior report should be considered out of date
and replaced with this one.

---

## Discussion

TODO

---

## Unittest

The unittest looks something like this.

    john@bigbox:~/projects/lifetrading$ python3 -m unittest lifetrading_test.py 
    2019-07-31 18:34:50,087:root:DEBUG:CsvFiles: 
    2019-07-31 18:34:50,095:alembic.runtime.migration:INFO:Context impl SQLiteImpl.
    2019-07-31 18:34:50,095:alembic.runtime.migration:INFO:Will assume non-transactional DDL.
    2019-07-31 18:34:50,100:alembic.runtime.migration:INFO:Context impl SQLiteImpl.
    2019-07-31 18:34:50,100:alembic.runtime.migration:INFO:Will assume non-transactional DDL.
    2019-07-31 18:34:50,112:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:34:50,112:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:34:50,112:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:34:50,114:root:DEBUG:[]
    2019-07-31 18:34:50,115:root:DEBUG:[]
    2019-07-31 18:34:50,120:root:DEBUG:CsvFiles: 
    2019-07-31 18:34:50,124:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:34:50,124:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:34:50,124:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:34:50,126:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:34:50,126:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:34:50,126:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:34:50,126:root:DEBUG:[]
    2019-07-31 18:34:50,127:root:DEBUG:[]
    2019-07-31 18:34:50,128:root:DEBUG:CsvFiles: TradeActivityReport-LIFETRADING-1-1.csv
    2019-07-31 18:34:50,131:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:34:50,131:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:34:50,131:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:34:50,132:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:34:50,132:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:34:50,132:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:34:50,150:root:INFO:Imported 2 rows from TradeActivityReport-LIFETRADING-1-1.csv
    2019-07-31 18:34:50,151:root:DEBUG:[OrderedDict([('id', 1), ('name', 'TradeActivityReport-LIFETRADING-1-1.csv'), ('mtime', 1564562090127623505), ('status', 'IMPORTED')])]
    2019-07-31 18:34:50,151:root:DEBUG:[OrderedDict([('id', 1), ('Column1', 'data1'), ('Column2', 'data2'), ('Column3', 'data3')]), OrderedDict([('id', 2), ('Column1', 'data4'), ('Column2', 'data5'), ('Column3', 'data6')])]
    2019-07-31 18:34:50,153:root:DEBUG:CsvFiles: TradeActivityReport-LIFETRADING-1-1.csv
    2019-07-31 18:34:50,154:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:34:50,154:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:34:50,154:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:34:50,163:root:DEBUG:[OrderedDict([('id', 1), ('name', 'TradeActivityReport-LIFETRADING-1-1.csv'), ('mtime', 1564562090127623505), ('status', 'UPDATED')])]
    2019-07-31 18:34:50,168:root:DEBUG:[OrderedDict([('id', 1), ('Column1', 'data1'), ('Column2', 'data2'), ('Column3', 'data3')]), OrderedDict([('id', 2), ('Column1', 'data4'), ('Column2', 'data5'), ('Column3', 'data6')])]
    .2019-07-31 18:34:50,174:alembic.runtime.migration:INFO:Context impl SQLiteImpl.
    2019-07-31 18:34:50,175:alembic.runtime.migration:INFO:Will assume non-transactional DDL.
    2019-07-31 18:34:50,178:alembic.runtime.migration:INFO:Context impl SQLiteImpl.
    2019-07-31 18:34:50,178:alembic.runtime.migration:INFO:Will assume non-transactional DDL.
    2019-07-31 18:34:50,181:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:34:50,181:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:34:50,182:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:34:50,183:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:34:50,183:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:34:50,183:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:34:50,184:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:34:50,184:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:34:50,184:dataset.table:DEBUG:Column exists: status
    .2019-07-31 18:34:50,188:root:DEBUG:CsvFiles: 
    2019-07-31 18:34:50,189:root:DEBUG:CsvFiles: 
    2019-07-31 18:34:50,189:root:DEBUG:CsvFiles: foo.csv
    2019-07-31 18:34:50,189:root:DEBUG:CsvFiles: bar.csv, foo.csv
    ...
    ----------------------------------------------------------------------
    Ran 5 tests in 0.108s
    
    OK


---

## Run test

A transcript of running it and dropping the test file into the directory looks like this:

    john@bigbox:~/projects/lifetrading$ 
    john@bigbox:~/projects/lifetrading$ ls
    lifetrading.py  lifetrading_test.py  __pycache__  README.md  requirements.txt  testfiles  venv
    john@bigbox:~/projects/lifetrading$ mkdir dropdir
    john@bigbox:~/projects/lifetrading$ ./lifetrading.py --help
    usage: lifetrading.py [-h] db_string download_path poll_seconds
    
    Data Import task for lifetrading.com.au
    
    positional arguments:
      db_string      Database connection string.
      download_path  Path to the download directory.
      poll_seconds   Number of seconds to sleep when nothing to do.
    
    optional arguments:
      -h, --help     show this help message and exit
    john@bigbox:~/projects/lifetrading$ ./lifetrading.py sqlite:///database.sqlite dropdir 30 &
    [1] 28407
    john@bigbox:~/projects/lifetrading$ 2019-07-31 18:47:47,138:root:INFO:Starting: Path "dropdir" DB "sqlite:///database.sqlite" Poll 30
    2019-07-31 18:47:47,138:root:DEBUG:CsvFiles: 
    2019-07-31 18:47:47,151:alembic.runtime.migration:INFO:Context impl SQLiteImpl.
    2019-07-31 18:47:47,151:alembic.runtime.migration:INFO:Will assume non-transactional DDL.
    2019-07-31 18:47:47,156:alembic.runtime.migration:INFO:Context impl SQLiteImpl.
    2019-07-31 18:47:47,156:alembic.runtime.migration:INFO:Will assume non-transactional DDL.
    2019-07-31 18:47:47,167:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:47:47,167:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:47:47,167:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:47:47,169:root:DEBUG:[]
    2019-07-31 18:47:47,170:root:DEBUG:[]
    
    john@bigbox:~/projects/lifetrading$ cp testfiles/TradeActivityReport-LIFETRADING-20181004-0500561.csv dropdir/
    john@bigbox:~/projects/lifetrading$ 2019-07-31 18:48:17,187:root:DEBUG:CsvFiles: TradeActivityReport-LIFETRADING-20181004-0500561.csv
    2019-07-31 18:48:17,193:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:48:17,193:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:48:17,193:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:48:17,194:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:48:17,194:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:48:17,194:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:48:17,215:root:INFO:Imported 3 rows from TradeActivityReport-LIFETRADING-20181004-0500561.csv
    2019-07-31 18:48:17,216:root:DEBUG:[OrderedDict([('id', 1), ('name', 'TradeActivityReport-LIFETRADING-20181004-0500561.csv'), ('mtime', 1564562883820384057), ('status', 'IMPORTED')])]
    2019-07-31 18:48:17,216:root:DEBUG:[OrderedDict([('id', 1), ('CounterpartyShor', 'LIFTRLTDSY'), ('TradeID', '20181003-00238'), ('TradeDate', '03-Oct-18'), ('SettlementDate', '05-Oct-18'), ('Ticker', 'CYB.AX'), ('ISIN', 'AU000000CYB7'), ('Name', 'CYBG PLC - CDI'), ('ProductShortName', 'LTASXUSDA'), ('Strategy(ExternalID)', ''), ('Qty', '-28,000'), ('Type', 'Sell-Open'), ('CCYUnderlying', 'AUD'), ('GrossPrice(Local)', '5.6136'), ('FXRate', '0.7179'), ('GrossPriceSwap', '4.0299'), ('Comms', '0.0250%'), ('MarketCharges', '0.0000%'), ('NetPriceSwap', '4.0289'), ('SwapCCY', 'USD'), ('TradedNotionalAmt', '112,807.97'), ('FundingRate', 'USD 1M LIBOR'), ('Spread', '-1.0000%'), ('Performance', 'Monthly'), ('FundingReset', 'Monthly'), ('DividendEntitlement', '100.0000%'), ('InitialMargin', '5.00'), ('ProductType', 'PS'), ('RemainingNotionalAmt', '-365,897.27'), ('Unique TransactionID', '1030240934SP-LTASXAUDACYB.AX'), ('TradeTime', '06:58:04'), ('TotalComm', '-28.209045'), ('TotalMarket', '0.000000'), ('OrderIns', 'Other'), ('InstrumentIdentifier', 'SESTXC'), ('Venue', 'XXXX')]), OrderedDict([('id', 2), ('CounterpartyShor', 'LIFTRLTDSY'), ('TradeID', '20181003-00082'), ('TradeDate', '03-Oct-18'), ('SettlementDate', '09-Oct-18'), ('Ticker', '6758.T'), ('ISIN', 'JP3435000009'), ('Name', 'SONY CORP'), ('ProductShortName', 'LTJPUSDA'), ('Strategy(ExternalID)', ''), ('Qty', '8,600'), ('Type', 'Buy-Open'), ('CCYUnderlying', 'JPY'), ('GrossPrice(Local)', '6,623.6977'), ('FXRate', '113.7760'), ('GrossPriceSwap', '58.2170'), ('Comms', '0.0250%'), ('MarketCharges', '0.0000%'), ('NetPriceSwap', '58.2316'), ('SwapCCY', 'USD'), ('TradedNotionalAmt', '500,791.39'), ('FundingRate', 'USD 1M LIBOR'), ('Spread', '0.4000%'), ('Performance', 'Monthly'), ('FundingReset', 'Monthly'), ('DividendEntitlement', '90.0000%'), ('InitialMargin', '2.50'), ('ProductType', 'PS'), ('RemainingNotionalAmt', '500,791.39'), ('Unique TransactionID', '1030240934SP-LTJPUSDA6758.T'), ('TradeTime', '06:10:02'), ('TotalComm', '125.166555'), ('TotalMarket', '0.000000'), ('OrderIns', 'Other'), ('InstrumentIdentifier', 'SESTXC'), ('Venue', 'XXXX')]), OrderedDict([('id', 3), ('CounterpartyShor', 'LIFTRLTDSY'), ('TradeID', '20181003-00083'), ('TradeDate', '03-Oct-18'), ('SettlementDate', '09-Oct-18'), ('Ticker', '7751.T'), ('ISIN', 'JP3242800005'), ('Name', 'CANON INC'), ('ProductShortName', 'LTJPUSDA'), ('Strategy(ExternalID)', ''), ('Qty', '-7,000'), ('Type', 'Sell-Open'), ('CCYUnderlying', 'JPY'), ('GrossPrice(Local)', '3,642.4657'), ('FXRate', '113.7760'), ('GrossPriceSwap', '32.0144'), ('Comms', '0.0250%'), ('MarketCharges', '0.0000%'), ('NetPriceSwap', '32.0064'), ('SwapCCY', 'USD'), ('TradedNotionalAmt', '224,044.48'), ('FundingRate', 'USD 1M LIBOR'), ('Spread', '-0.5000%'), ('Performance', 'Monthly'), ('FundingReset', 'Monthly'), ('DividendEntitlement', '100.0000%'), ('InitialMargin', '2.50'), ('ProductType', 'PS'), ('RemainingNotionalAmt', '-224,044.48'), ('Unique TransactionID', '1030240934SP-LTJPUSDA7751.T'), ('TradeTime', '06:10:02'), ('TotalComm', '-56.025128'), ('TotalMarket', '0.000000'), ('OrderIns', 'Other'), ('InstrumentIdentifier', 'SESTXC'), ('Venue', 'XXXX')])]
    2019-07-31 18:48:17,217:root:DEBUG:CsvFiles: TradeActivityReport-LIFETRADING-20181004-0500561.csv
    2019-07-31 18:48:17,218:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:48:17,218:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:48:17,218:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:48:17,229:root:DEBUG:[OrderedDict([('id', 1), ('name', 'TradeActivityReport-LIFETRADING-20181004-0500561.csv'), ('mtime', 1564562883820384057), ('status', 'UPDATED')])]
    2019-07-31 18:48:17,248:root:DEBUG:[OrderedDict([('id', 1), ('CounterpartyShor', 'LIFTRLTDSY'), ('TradeID', '20181003-00238'), ('TradeDate', '03-Oct-18'), ('SettlementDate', '05-Oct-18'), ('Ticker', 'CYB.AX'), ('ISIN', 'AU000000CYB7'), ('Name', 'CYBG PLC - CDI'), ('ProductShortName', 'LTASXUSDA'), ('Strategy(ExternalID)', ''), ('Qty', '-28,000'), ('Type', 'Sell-Open'), ('CCYUnderlying', 'AUD'), ('GrossPrice(Local)', '5.6136'), ('FXRate', '0.7179'), ('GrossPriceSwap', '4.0299'), ('Comms', '0.0250%'), ('MarketCharges', '0.0000%'), ('NetPriceSwap', '4.0289'), ('SwapCCY', 'USD'), ('TradedNotionalAmt', '112,807.97'), ('FundingRate', 'USD 1M LIBOR'), ('Spread', '-1.0000%'), ('Performance', 'Monthly'), ('FundingReset', 'Monthly'), ('DividendEntitlement', '100.0000%'), ('InitialMargin', '5.00'), ('ProductType', 'PS'), ('RemainingNotionalAmt', '-365,897.27'), ('Unique TransactionID', '1030240934SP-LTASXAUDACYB.AX'), ('TradeTime', '06:58:04'), ('TotalComm', '-28.209045'), ('TotalMarket', '0.000000'), ('OrderIns', 'Other'), ('InstrumentIdentifier', 'SESTXC'), ('Venue', 'XXXX')]), OrderedDict([('id', 2), ('CounterpartyShor', 'LIFTRLTDSY'), ('TradeID', '20181003-00082'), ('TradeDate', '03-Oct-18'), ('SettlementDate', '09-Oct-18'), ('Ticker', '6758.T'), ('ISIN', 'JP3435000009'), ('Name', 'SONY CORP'), ('ProductShortName', 'LTJPUSDA'), ('Strategy(ExternalID)', ''), ('Qty', '8,600'), ('Type', 'Buy-Open'), ('CCYUnderlying', 'JPY'), ('GrossPrice(Local)', '6,623.6977'), ('FXRate', '113.7760'), ('GrossPriceSwap', '58.2170'), ('Comms', '0.0250%'), ('MarketCharges', '0.0000%'), ('NetPriceSwap', '58.2316'), ('SwapCCY', 'USD'), ('TradedNotionalAmt', '500,791.39'), ('FundingRate', 'USD 1M LIBOR'), ('Spread', '0.4000%'), ('Performance', 'Monthly'), ('FundingReset', 'Monthly'), ('DividendEntitlement', '90.0000%'), ('InitialMargin', '2.50'), ('ProductType', 'PS'), ('RemainingNotionalAmt', '500,791.39'), ('Unique TransactionID', '1030240934SP-LTJPUSDA6758.T'), ('TradeTime', '06:10:02'), ('TotalComm', '125.166555'), ('TotalMarket', '0.000000'), ('OrderIns', 'Other'), ('InstrumentIdentifier', 'SESTXC'), ('Venue', 'XXXX')]), OrderedDict([('id', 3), ('CounterpartyShor', 'LIFTRLTDSY'), ('TradeID', '20181003-00083'), ('TradeDate', '03-Oct-18'), ('SettlementDate', '09-Oct-18'), ('Ticker', '7751.T'), ('ISIN', 'JP3242800005'), ('Name', 'CANON INC'), ('ProductShortName', 'LTJPUSDA'), ('Strategy(ExternalID)', ''), ('Qty', '-7,000'), ('Type', 'Sell-Open'), ('CCYUnderlying', 'JPY'), ('GrossPrice(Local)', '3,642.4657'), ('FXRate', '113.7760'), ('GrossPriceSwap', '32.0144'), ('Comms', '0.0250%'), ('MarketCharges', '0.0000%'), ('NetPriceSwap', '32.0064'), ('SwapCCY', 'USD'), ('TradedNotionalAmt', '224,044.48'), ('FundingRate', 'USD 1M LIBOR'), ('Spread', '-0.5000%'), ('Performance', 'Monthly'), ('FundingReset', 'Monthly'), ('DividendEntitlement', '100.0000%'), ('InitialMargin', '2.50'), ('ProductType', 'PS'), ('RemainingNotionalAmt', '-224,044.48'), ('Unique TransactionID', '1030240934SP-LTJPUSDA7751.T'), ('TradeTime', '06:10:02'), ('TotalComm', '-56.025128'), ('TotalMarket', '0.000000'), ('OrderIns', 'Other'), ('InstrumentIdentifier', 'SESTXC'), ('Venue', 'XXXX')])]
    john@bigbox:~/projects/lifetrading$ 2019-07-31 18:48:47,276:root:DEBUG:CsvFiles: TradeActivityReport-LIFETRADING-20181004-0500561.csv
    2019-07-31 18:48:47,278:dataset.table:DEBUG:Column exists: name
    2019-07-31 18:48:47,278:dataset.table:DEBUG:Column exists: mtime
    2019-07-31 18:48:47,278:dataset.table:DEBUG:Column exists: status
    2019-07-31 18:48:47,287:root:DEBUG:[OrderedDict([('id', 1), ('name', 'TradeActivityReport-LIFETRADING-20181004-0500561.csv'), ('mtime', 1564562883820384057), ('status', 'UPDATED')])]
    2019-07-31 18:48:47,292:root:DEBUG:[OrderedDict([('id', 1), ('CounterpartyShor', 'LIFTRLTDSY'), ('TradeID', '20181003-00238'), ('TradeDate', '03-Oct-18'), ('SettlementDate', '05-Oct-18'), ('Ticker', 'CYB.AX'), ('ISIN', 'AU000000CYB7'), ('Name', 'CYBG PLC - CDI'), ('ProductShortName', 'LTASXUSDA'), ('Strategy(ExternalID)', ''), ('Qty', '-28,000'), ('Type', 'Sell-Open'), ('CCYUnderlying', 'AUD'), ('GrossPrice(Local)', '5.6136'), ('FXRate', '0.7179'), ('GrossPriceSwap', '4.0299'), ('Comms', '0.0250%'), ('MarketCharges', '0.0000%'), ('NetPriceSwap', '4.0289'), ('SwapCCY', 'USD'), ('TradedNotionalAmt', '112,807.97'), ('FundingRate', 'USD 1M LIBOR'), ('Spread', '-1.0000%'), ('Performance', 'Monthly'), ('FundingReset', 'Monthly'), ('DividendEntitlement', '100.0000%'), ('InitialMargin', '5.00'), ('ProductType', 'PS'), ('RemainingNotionalAmt', '-365,897.27'), ('Unique TransactionID', '1030240934SP-LTASXAUDACYB.AX'), ('TradeTime', '06:58:04'), ('TotalComm', '-28.209045'), ('TotalMarket', '0.000000'), ('OrderIns', 'Other'), ('InstrumentIdentifier', 'SESTXC'), ('Venue', 'XXXX')]), OrderedDict([('id', 2), ('CounterpartyShor', 'LIFTRLTDSY'), ('TradeID', '20181003-00082'), ('TradeDate', '03-Oct-18'), ('SettlementDate', '09-Oct-18'), ('Ticker', '6758.T'), ('ISIN', 'JP3435000009'), ('Name', 'SONY CORP'), ('ProductShortName', 'LTJPUSDA'), ('Strategy(ExternalID)', ''), ('Qty', '8,600'), ('Type', 'Buy-Open'), ('CCYUnderlying', 'JPY'), ('GrossPrice(Local)', '6,623.6977'), ('FXRate', '113.7760'), ('GrossPriceSwap', '58.2170'), ('Comms', '0.0250%'), ('MarketCharges', '0.0000%'), ('NetPriceSwap', '58.2316'), ('SwapCCY', 'USD'), ('TradedNotionalAmt', '500,791.39'), ('FundingRate', 'USD 1M LIBOR'), ('Spread', '0.4000%'), ('Performance', 'Monthly'), ('FundingReset', 'Monthly'), ('DividendEntitlement', '90.0000%'), ('InitialMargin', '2.50'), ('ProductType', 'PS'), ('RemainingNotionalAmt', '500,791.39'), ('Unique TransactionID', '1030240934SP-LTJPUSDA6758.T'), ('TradeTime', '06:10:02'), ('TotalComm', '125.166555'), ('TotalMarket', '0.000000'), ('OrderIns', 'Other'), ('InstrumentIdentifier', 'SESTXC'), ('Venue', 'XXXX')]), OrderedDict([('id', 3), ('CounterpartyShor', 'LIFTRLTDSY'), ('TradeID', '20181003-00083'), ('TradeDate', '03-Oct-18'), ('SettlementDate', '09-Oct-18'), ('Ticker', '7751.T'), ('ISIN', 'JP3242800005'), ('Name', 'CANON INC'), ('ProductShortName', 'LTJPUSDA'), ('Strategy(ExternalID)', ''), ('Qty', '-7,000'), ('Type', 'Sell-Open'), ('CCYUnderlying', 'JPY'), ('GrossPrice(Local)', '3,642.4657'), ('FXRate', '113.7760'), ('GrossPriceSwap', '32.0144'), ('Comms', '0.0250%'), ('MarketCharges', '0.0000%'), ('NetPriceSwap', '32.0064'), ('SwapCCY', 'USD'), ('TradedNotionalAmt', '224,044.48'), ('FundingRate', 'USD 1M LIBOR'), ('Spread', '-0.5000%'), ('Performance', 'Monthly'), ('FundingReset', 'Monthly'), ('DividendEntitlement', '100.0000%'), ('InitialMargin', '2.50'), ('ProductType', 'PS'), ('RemainingNotionalAmt', '-224,044.48'), ('Unique TransactionID', '1030240934SP-LTJPUSDA7751.T'), ('TradeTime', '06:10:02'), ('TotalComm', '-56.025128'), ('TotalMarket', '0.000000'), ('OrderIns', 'Other'), ('InstrumentIdentifier', 'SESTXC'), ('Venue', 'XXXX')])]
    
    john@bigbox:~/projects/lifetrading$ ps ax | grep lifetrad
    28407 pts/0    S      0:00 /usr/bin/python3 ./lifetrading.py sqlite:///database.sqlite dropdir 30
    28467 pts/0    S+     0:00 grep --color=auto lifetrad
    john@bigbox:~/projects/lifetrading$ kill -9 28407
    john@bigbox:~/projects/lifetrading$ ls
    database.sqlite  dropdir  lifetrading.py  lifetrading_test.py  __pycache__  README.md  requirements.txt  testfiles  venv
    [1]+  Killed                  ./lifetrading.py sqlite:///database.sqlite dropdir 30
    john@bigbox:~/projects/lifetrading$ sqlite3 database.sqlite 
    SQLite version 3.27.2 2019-02-25 16:06:06
    Enter ".help" for usage hints.
    sqlite> .tables
    filelog        tradeactivity
    sqlite> .dump filelog
    PRAGMA foreign_keys=OFF;
    BEGIN TRANSACTION;
    CREATE TABLE filelog (
        id INTEGER NOT NULL, 
        name VARCHAR, mtime BIGINT, status VARCHAR, 
        PRIMARY KEY (id)
    );
    INSERT INTO filelog VALUES(1,'TradeActivityReport-LIFETRADING-20181004-0500561.csv',1564562883820384057,'UPDATED');
    CREATE INDEX ix_filelog_91b3e5b34aeef828 ON filelog (name, mtime, status);
    COMMIT;
    sqlite> .dump tradeactivity
    PRAGMA foreign_keys=OFF;
    BEGIN TRANSACTION;
    CREATE TABLE tradeactivity (
        id INTEGER NOT NULL, 
        "CounterpartyShor" TEXT, 
        "TradeID" TEXT, 
        "TradeDate" TEXT, 
        "SettlementDate" TEXT, 
        "Ticker" TEXT, 
        "ISIN" TEXT, 
        "Name" TEXT, 
        "ProductShortName" TEXT, 
        "Strategy(ExternalID)" TEXT, 
        "Qty" TEXT, 
        "Type" TEXT, 
        "CCYUnderlying" TEXT, 
        "GrossPrice(Local)" TEXT, 
        "FXRate" TEXT, 
        "GrossPriceSwap" TEXT, 
        "Comms" TEXT, 
        "MarketCharges" TEXT, 
        "NetPriceSwap" TEXT, 
        "SwapCCY" TEXT, 
        "TradedNotionalAmt" TEXT, 
        "FundingRate" TEXT, 
        "Spread" TEXT, 
        "Performance" TEXT, 
        "FundingReset" TEXT, 
        "DividendEntitlement" TEXT, 
        "InitialMargin" TEXT, 
        "ProductType" TEXT, 
        "RemainingNotionalAmt" TEXT, 
        "Unique TransactionID" TEXT, 
        "TradeTime" TEXT, 
        "TotalComm" TEXT, 
        "TotalMarket" TEXT, 
        "OrderIns" TEXT, 
        "InstrumentIdentifier" TEXT, 
        "Venue" TEXT, 
        PRIMARY KEY (id)
    );
    INSERT INTO tradeactivity VALUES(1,'LIFTRLTDSY','20181003-00238','03-Oct-18','05-Oct-18','CYB.AX','AU000000CYB7','CYBG PLC - CDI','LTASXUSDA','','-28,000','Sell-Open','AUD','5.6136','0.7179','4.0299','0.0250%','0.0000%','4.0289','USD','112,807.97','USD 1M LIBOR','-1.0000%','Monthly','Monthly','100.0000%','5.00','PS','-365,897.27','1030240934SP-LTASXAUDACYB.AX','06:58:04','-28.209045','0.000000','Other','SESTXC','XXXX');
    INSERT INTO tradeactivity VALUES(2,'LIFTRLTDSY','20181003-00082','03-Oct-18','09-Oct-18','6758.T','JP3435000009','SONY CORP','LTJPUSDA','','8,600','Buy-Open','JPY','6,623.6977','113.7760','58.2170','0.0250%','0.0000%','58.2316','USD','500,791.39','USD 1M LIBOR','0.4000%','Monthly','Monthly','90.0000%','2.50','PS','500,791.39','1030240934SP-LTJPUSDA6758.T','06:10:02','125.166555','0.000000','Other','SESTXC','XXXX');
    INSERT INTO tradeactivity VALUES(3,'LIFTRLTDSY','20181003-00083','03-Oct-18','09-Oct-18','7751.T','JP3242800005','CANON INC','LTJPUSDA','','-7,000','Sell-Open','JPY','3,642.4657','113.7760','32.0144','0.0250%','0.0000%','32.0064','USD','224,044.48','USD 1M LIBOR','-0.5000%','Monthly','Monthly','100.0000%','2.50','PS','-224,044.48','1030240934SP-LTJPUSDA7751.T','06:10:02','-56.025128','0.000000','Other','SESTXC','XXXX');
    COMMIT;
    sqlite> .quit
    john@bigbox:~/projects/lifetrading$ 


