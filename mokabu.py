#!/usr/bin/python3
# -*- coding: utf-8 -*-

#https://www.w3schools.com/sql/sql_join.asp
import sqlite3 as lite
import sys
import report

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
        print(schema+" Error %s:" % e.args[0])

  def populate(self):
    dbc=self.dbc
    try:
      #populate='populate.sql'
      populate='2020_Klienten.sql'
      dbc=self.dbc
      fh=open(populate,'r')
      dbc.executescript(fh.read())
      self.db.commit()
    except lite.Error as e:
      print(populate+" Error %s:"%e.args[0])

    try:
      for row in dbc.execute('SELECT * FROM tblPerson'):
        print(row)
      for row in dbc.execute('SELECT * FROM tblBehandlung'):
        print(row)
      for row in dbc.execute("SELECT datetime(datBehandlung,'unixepoch'),* FROM tblBehandlung"):
        print(row)
      print('xxx')
      for row in dbc.execute("SELECT tblBehandlung.*, tblPerson.* FROM tblBehandlung LEFT JOIN tblPerson ON tblBehandlung.fkPerson=tblPerson.pkPerson;"):
        print(row)
    except lite.Error as e:
        print("SQL tests Error %s:" % e.args[0])

  def report_invoice(self):
    db=self.db
    dbcRng=self.dbc
    dbcBeh=db.cursor()
    sqlRng='''SELECT tr.pkRechnung,tr.datRechnung,RngAnrede,RngNachname,RngVorname,RngAdresse,RngAdresse1,RngAdresse2,PLZ,Ort,Nachname,Vorname,datGeb,AHVNr
    FROM tblRechnung tr LEFT JOIN tblPerson tp on tr.fkPerson=tp.pkPerson
    ORDER BY tr.pkRechnung'''

    sqlTplBeh='''SELECT datBehandlung,Stundenansatz,Dauer,Bemerkung,TarZif FROM tblBehandlung tb
    WHERE tb.fkRechnung=%s
    ORDER BY tb.datBehandlung'''

#    sql='''SELECT tp.* ,tr.pkRechnung,tr.datRechnung,tb.Dauer,tb.Stundenansatz,
#tb.Dauer*tb.Stundenansatz/60 AS tot
#FROM tblBehandlung tb LEFT JOIN tblRechnung tr ON tb.fkRechnung=tr.pkRechnung LEFT JOIN tblPerson tp on tb.fkPerson =tp.pkPerson
#ORDER BY tr.pkRechnung, tb.datBehandlung'''

    repIvc=report.Invoice()
    repIvc.init()

    for recRng in dbcRng.execute(sqlRng):
      print(recRng)
      sqlBeh=sqlTplBeh%recRng[0]
      dbcBeh=dbcBeh.execute(sqlBeh)
      dBeh=dbcBeh.fetchall()
      print(dBeh)
      repIvc.add(recRng[2:],recRng[1],dBeh)

    repIvc.finalize()



mkb=MoKaBu('mokabu.db')
#mkb.open()
mkb.reset()
mkb.populate()
mkb.report_invoice()
mkb.close()

