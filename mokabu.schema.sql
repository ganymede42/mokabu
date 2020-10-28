PRAGMA foreign_keys = 0;
DROP TABLE IF EXISTS tblBehandlung;
DROP TABLE  IF EXISTS tblRechnung;
DROP TABLE  IF EXISTS tblPerson;
PRAGMA foreign_keys = 1;

-- tblPerson definition

CREATE TABLE tblPerson (
	pkPerson INTEGER NOT NULL,
	RngAnrede TEXT,
	RngNachname TEXT,
	RngVorname TEXT,
	RngAdresse TEXT,
	RngAdresse1 TEXT,
	RngAdresse2 TEXT,
	PLZ INTEGER DEFAULT 0,
	Ort TEXT,
	Nachname TEXT,
	Vorname TEXT,
	Tel TEXT,
	Tel1 TEXT,
	Tel2 TEXT,
	datGeb TEXT,
	eMail TEXT,
	eMail1 TEXT,
	eMail2 TEXT,
	AHVNr TEXT,
	Bemerkung TEXT,
	CONSTRAINT PKtblPerson PRIMARY KEY (pkPerson)
);

CREATE UNIQUE INDEX IDXtblPerson ON tblPerson (pkPerson);


-- tblRechnung definition

CREATE TABLE tblRechnung (
	pkRechnung INTEGER NOT NULL,
	fkPerson INTEGER,
	tplInvoice INTEGER, --invoice template
	datRechnung TEXT,
	datGedruckt TEXT,
	datBezahlt TEXT,
	Bemerkung TEXT,
	CONSTRAINT PKtblRechnung PRIMARY KEY (pkRechnung),
	CONSTRAINT FKtblPersonfkPerson FOREIGN KEY (fkPerson) REFERENCES tblPerson(pkPerson)
);
CREATE UNIQUE INDEX IDXtblRechnung ON tblRechnung (pkRechnung);
CREATE INDEX IDXtblRechnungfkPerson ON tblRechnung (fkPerson);


-- tblBehandlung definition

CREATE TABLE tblBehandlung (
	pkBehandlung INTEGER NOT NULL,
	fkRechnung INTEGER,
	fkPerson INTEGER,
	datBehandlung TEXT,
	Dauer INTEGER DEFAULT 60,
	Stundenansatz NUMERIC DEFAULT 180,
	Bemerkung TEXT,
	TarZif TEXT,
	AktenEintrag TEXT,
	CONSTRAINT PKtblBehandlung PRIMARY KEY (pkBehandlung),
	CONSTRAINT FKtblBehandlungfkRechnung FOREIGN KEY (fkRechnung) REFERENCES tblRechnung(pkRechnung)
	CONSTRAINT FKtblBehandlungfkPerson FOREIGN KEY (fkPerson) REFERENCES tblPerson(pkPerson)
);

CREATE UNIQUE INDEX IDXtblBehandlung ON tblBehandlung (pkBehandlung);
CREATE INDEX IDXtblBehandlungfkRechnung ON tblBehandlung (fkRechnung);
CREATE INDEX IDXtblBehandlungfkPerson ON tblBehandlung (fkPerson);

VACUUM;
