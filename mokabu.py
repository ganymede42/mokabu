#!/usr/bin/python3
# -*- coding: utf-8 -*-

#https://www.w3schools.com/sql/sql_join.asp
import sqlite3 as lite
import sys

class MoKaBu:

  def __init__(self,fn='mokabu.db'):
    self.open(fn)

  def open(self,fn):
    try:
        self.db=db=lite.connect(fn)
        self.dbc=dbc=db.cursor()
        dbc.execute('SELECT SQLITE_VERSION()')
        data = dbc.fetchone()
        print("SQLite version: %s" % data)
        #One way of permanently turning on foreign_keys by default is to inject the following line into ~/.sqliterc: PRAGMA foreign_keys = ON;
        dbc.execute("PRAGMA foreign_keys = 1")
        #dbc.execute("PRAGMA foreign_keys")
    except lite.Error as e:
        print("Error %s:" % e.args[0])
        sys.exit(1)

  def close(self):
    try:
        self.db.close()
    except lite.Error as e:
        print("Error %s:" % e.args[0])


  def reset(self):
    try:
      schema='mokabu.schema'
      dbc=self.dbc
      fh=open(schema,'r')
      dbc.executescript(fh.read())
    except lite.Error as e:
        print("1Error %s:" % e.args[0])

  def populate(self):
    dbc=self.dbc
    try:
      #dbc.execute("insert into tblPerson values (NULL,'Anrede','Nachname','Vorname','Adresse',1111,'Ort',1234,5678,'eMail','Bemerkung')")
      #dbc.execute("insert into tblPerson values ('IDPerson','Anrede','Nachname','Vorname','Adresse','PLZ','Ort','Telefon','Mobile','eMail','Bemerkung')")

      dataLst=((None,'Anrede','Nachname','Vorname','Adresse',1111,'Ort','0794269945','0654269945','eMail','Bemerkung'),
               (None,'Herr','Zamofing','Thierry','Weihermattstrasse 11a',5242,'Birr','0763399148',None,'th.zamofing@gmail.com','Bemerkung'),
               (None,'Frau','Kast','Monika','Albisstrasse 12',8000,'Zürich','0785561234',None,'eMail','Bemerkung'),
               (None,'Herr','Meier','Roger','Fluhweg 10',5430,'Wettingen','0763395416','0654269945','eMail','Bemerkung'))
      #for data in dataLst:
      #  dbc.execute("INSERT INTO tblPerson VALUES "+str(data).replace('None','NULL'))

      dbc.executemany("INSERT INTO tblPerson VALUES (?,?,?,?,?,?,?,?,?,?,?)",dataLst)
      #dataLst=(('Anrede','Nachname','Vorname','Adresse',1111,'Ort',1234,5678,'eMail','Bemerkung'),
      #         ('Herr','Zamofing','Thierry','Weihermattstrasse 11a','0763399148','Birr',1234,5678,'eMail','Bemerkung'),
      #         ('Frau','Kast','Monika','Albisstrasse 12',8000,'Zürich',1234,5678,'eMail','Bemerkung'),
      #         ('Herr','Meier','Roger','Fluhweg 10',5430,'Wettingen','0763399148',5678,'eMail','Bemerkung'))
      #dbc.executemany("INSERT INTO tblPerson(Anrede,Nachname,Vorname,Adresse,PLZ,Ort,Telefon,Mobile,eMail,Bemerkung) VALUES (?,?,?,?,?,?,?,?,?,?)",dataLst)


      populate='populate.sql'
      dbc=self.dbc
      fh=open(populate,'r')
      dbc.executescript(fh.read())


      self.db.commit()
      for row in dbc.execute('SELECT * FROM tblPerson'):
        print(row)
      for row in dbc.execute('SELECT * FROM tblBehandlung'):
        print(row)
      for row in dbc.execute("SELECT datetime(Datum,'unixepoch'),* FROM tblBehandlung"):
        print(row)
      for row in dbc.execute("SELECT tblBehandlung.*, tblPerson.* FROM tblBehandlung INNER JOIN tblPerson ON tblBehandlung.RFPerson=tblPerson.IDPerson;"):
        print(row)


    except lite.Error as e:
        print("Error %s:" % e.args[0])




mkb=MoKaBu('mokabu.db')
#mkb.open()
mkb.reset()
mkb.populate()
mkb.close()

