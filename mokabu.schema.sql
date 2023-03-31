-- NAMING CONVENTIONS:
-- <TableName>                table starts with upper case and is camel case
-- <fieldName>                field name starts with lower case and is camel case
-- <id>                       primary key field is 'id'
-- fk<TableName>              foreign key field is 'fk<TableName>' and reffers to field id of table <TableName>
-- Cpk<TableName>             primary key constraint
-- Cfk<TableName>_<fieldName> foreign key constraint
-- Idx<TableName>             index on primary key
-- Idx<TableName>_<fieldName> index on a field (mostly foreign key)

-- CONSTRAINT Cpk<TblName> PRIMARY KEY (id),
-- CONSTRAINT Cfk<TblName>_fk<TblRef> FOREIGN KEY (fk<TblRef>) REFERENCES <TblRef>(id)
-- CREATE UNIQUE INDEX Idx<TblName> ON <TblName>(id);
-- CREATE INDEX Idx<TblName>_fk<TblRef> ON <TblName> (fk<TblRef>);

--- condendes fileld list:
--- Person:
---   id,ivcPrefix,ivcLstName,ivcFstName,ivcAddress,ivcAddress1,ivcAddress2,zipCode,city,lstName,
---   fstName,phone,phone1,phone2,dtBirth,eMail,eMail1,eMail2,ahvNr,comment,
--- Invoice:
---   id,fkPerson,tplInvoice,dtInvoice,comment,
--- Treatment:
---    id,fkInvoice,fkPerson,dtTreatment,duration,costPerHour,comment,tarZif,document,


PRAGMA foreign_keys = 0;
DROP TABLE  IF EXISTS Person;
DROP TABLE IF EXISTS Treatment;
DROP TABLE  IF EXISTS Invoice;
DROP TABLE  IF EXISTS Account;
DROP TABLE  IF EXISTS EventLog;
DROP TABLE  IF EXISTS EventType;

PRAGMA foreign_keys = 1;


-- TABLE Person definition

CREATE TABLE Person (
  id  INTEGER NOT NULL,

  cltPrefix TEXT,
  cltLstName TEXT NOT NULL,
  cltFstName TEXT NOT NULL,
  cltAddress  TEXT,
  cltZipCode INTEGER,
  cltCity  TEXT,
  cltAhvNr TEXT,
  cltDtBirth DATETIME,

  ivcPrefix TEXT,
  ivcLstName  TEXT,
  ivcFstName  TEXT,
  ivcAddress  TEXT,
  ivcZipCode INTEGER,
  ivcCity  TEXT,

  phone TEXT,
  phone1  TEXT,
  phone2  TEXT,
  eMail TEXT,
  eMail1  TEXT,
  eMail2  TEXT,
  comment TEXT,
  CONSTRAINT CpkPerson PRIMARY KEY(id)
);

-- TABLE Invoice definition

CREATE TABLE Invoice (
	id INTEGER NOT NULL,
	fkPerson INTEGER,
	fkAccount INTEGER,
	tplInvoice INTEGER, --invoice template
	dtInvoice DATETIME,
	comment TEXT,
	CONSTRAINT CpkInvoice PRIMARY KEY (id),
	CONSTRAINT CfkInvoice_fkPerson FOREIGN KEY (fkPerson) REFERENCES Person(id),
	CONSTRAINT CfkInvoice_fkAccount FOREIGN KEY (fkAccount) REFERENCES Account(id)
);
CREATE UNIQUE INDEX IdxInvoice ON Invoice (id);
CREATE INDEX IdxInvoice_fkPerson ON Invoice (fkPerson);
CREATE INDEX IdxInvoice_fkAccount ON Invoice (fkAccount);


-- TABLE Account definition

CREATE TABLE Account (
	id INTEGER NOT NULL,
	dtEvent DATETIME, --date of money transfer
	amount NUMERIC,
	refNr NUMERIC,
	refText TEXT,
	comment TEXT,
	CONSTRAINT CpkAccount PRIMARY KEY (id)
);
CREATE UNIQUE INDEX IdxAccount ON Account (id);


-- TABLE Treatment definition

CREATE TABLE Treatment (
	id INTEGER NOT NULL,
	fkInvoice INTEGER,
	fkPerson INTEGER,
	dtTreatment TEXT,
	duration INTEGER DEFAULT 60,
	costPerHour NUMERIC DEFAULT 180,
	comment TEXT,
	tarZif TEXT,
	document TEXT,
	CONSTRAINT CpkTreatment PRIMARY KEY (id),
	CONSTRAINT CfkTreatment_fkInvoice FOREIGN KEY (fkInvoice) REFERENCES Invoice(id)
	CONSTRAINT CfkTreatment_fkPerson FOREIGN KEY (fkPerson) REFERENCES Person(id)
);
CREATE UNIQUE INDEX IdxTreatment ON Treatment (id);
CREATE INDEX IdxTreatment_fkInvoice ON Treatment (fkInvoice);
CREATE INDEX IdxTreatment_fkPerson ON Treatment (fkPerson);


-- TABLE EventLog definition

CREATE TABLE EventLog (
	id INTEGER NOT NULL,
	dtEvt DATETIME,
	fkEventType INTEGER,
	fkObj INTEGER,
	comment TEXT,
	CONSTRAINT CpkEventLog PRIMARY KEY (id),
	CONSTRAINT CfkEventLog_fkEventType FOREIGN KEY (fkEventType) REFERENCES EventType(id)
);
CREATE UNIQUE INDEX IdxEventLog ON EventLog (id);
CREATE INDEX IdxEventLog_fkEventType ON EventLog (fkEventType);


-- TABLE EventType definition

CREATE TABLE EventType (
	id INTEGER NOT NULL,
	tblName TEXT,
	comment TEXT,
	CONSTRAINT CpkEventType PRIMARY KEY (id)
);
CREATE UNIQUE INDEX IdxEventType ON EventType(id);

INSERT INTO EventType (id,tblName,comment) VALUES
(100,'Invoice','Rechnung erstellt'),
(101,'Invoice','Rechnung bezahlt'),
(102,'Invoice','1. Mahnung erstellt'),
(103,'Invoice','2. Mahnung erstellt');

PRAGMA application_id=1; --- set application_id (initial=0)

VACUUM;
