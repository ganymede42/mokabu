-- https://www.sqlite.org/lang_altertable.html   section 7, steps 1-12
-- https://www.techonthenet.com/sqlite/index.php
-- migrates shema of application_id=0 to application_id=1

-- SELECT type, sql FROM sqlite_master WHERE tbl_name='Person';

PRAGMA foreign_keys = 0;
CREATE TABLE PersonNew (
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

INSERT INTO PersonNew (id, cltPrefix, cltLstName, cltFstName, cltAddress,                                                               cltZipCode, cltCity, cltAhvNr, cltDtBirth, ivcPrefix, ivcLstName, ivcFstName, ivcAddress,                                                               ivcZipCode, ivcCity, phone, phone1, phone2, eMail, eMail1, eMail2, comment)
  SELECT               id, '',        lstName,    fstName,    ivcAddress||COALESCE('|'||ivcAddress1,'')||COALESCE('|'||ivcAddress2,''), zipCode,    city,    ahvNr,    dtBirth,    ivcPrefix, ivcLstName, ivcFstName, ivcAddress||COALESCE('|'||ivcAddress1,'')||COALESCE('|'||ivcAddress2,''), zipCode,    city,    phone, phone1, phone2, eMail, eMail1, eMail2, comment FROM Person;

DROP TABLE Person;

ALTER TABLE PersonNew RENAME TO Person;

CREATE UNIQUE INDEX IdxPerson ON Person (id);

PRAGMA application_id;
PRAGMA application_id=1; --- set new application_id (initial=0)

PRAGMA foreign_key_check;

PRAGMA foreign_keys = 1;

VACUUM;
