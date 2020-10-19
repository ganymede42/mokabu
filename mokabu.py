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
        for sql in('SELECT COUNT(*) FROM tblPerson',
                   'SELECT COUNT(*) FROM tblBehandlung',
                   'SELECT COUNT(*) FROM tblRechnung'):
          print(sql+' -> ',end='')
          for row in dbc.execute(sql):
            print(row)
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
      schema='mokabu.schema.sql'
      dbc=self.dbc
      fh=open(schema,'r')
      dbc.executescript(fh.read())
    except lite.Error as e:
        print(schema+" Error %s:" % e.args[0])

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

    fn='invoice.pdf'
    repIvc=report.Invoice(fn)

    for recRng in dbcRng.execute(sqlRng):
      print(recRng)
      sqlBeh=sqlTplBeh%recRng[0]
      dbcBeh=dbcBeh.execute(sqlBeh)
      dBeh=dbcBeh.fetchall()
      print(dBeh)
      repIvc.add(recRng[2:],recRng[1],dBeh)

    repIvc.publish()
    report.default_app_open(fn);

  def report_therapy_progress(self, sqlFilt=None,fn='therapy_progress.pdf'):
    db=self.db
    dbcRng=self.dbc
    dbcBeh=db.cursor()
    sqlTplBeh='SELECT fkPerson,Nachname,Vorname,datGeb,Tel1,eMail,datBehandlung,tb.Bemerkung,AktenEintrag FROM tblBehandlung tb LEFT JOIN tblPerson tp ON tb.fkPerson=tp.pkPerson'
    sqlTplOrd='ORDER BY fkPerson,tb.datBehandlung'''

    if sqlFilt is None:
      sqlBeh=sqlTplBeh+' '+sqlTplOrd
    else:
      sqlBeh=sqlTplBeh+' WHERE '+sqlFilt+' '+sqlTplOrd

    repBeh=report.TherapyProgress(fn)

    fkCurPerson=-1
    for recBeh in dbcRng.execute(sqlBeh):
      fkPerson=recBeh[0]
      if fkPerson!=fkCurPerson:
        fkCurPerson=fkPerson
        repBeh.addClient(*recBeh[1:6])
      repBeh.addTherapyProgress(*recBeh[6:9])
    repBeh.publish()
    report.default_app_open(fn);




if __name__=='__main__':

  mkb=MoKaBu('mokabu.db')
  #mkb.open()
  #mkb.reset()
  #mkb.populate()
  #mkb.report_invoice()
  mkb.report_therapy_progress();exit(0)

  import qtgui
  qtgui.MainApp(mkb)

  mkb.close()

