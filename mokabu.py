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
        for sql in('SELECT COUNT(*) FROM Person',
                   'SELECT COUNT(*) FROM Treatment',
                   'SELECT COUNT(*) FROM Invoice',
                   'SELECT COUNT(*) FROM Account',
                   'SELECT COUNT(*) FROM EventLog',
                   'SELECT COUNT(*) FROM EventType'):
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

  def report_invoice(self, sqlFilt=None,fn='invoice.pdf'):
    db=self.db
    dbcRng=self.dbc
    dbcBeh=db.cursor()
    sqlTplRng='''SELECT iv.id,tplInvoice,dtInvoice,ivcPrefix,ivcLstName,ivcFstName,ivcAddress,ivcAddress1,ivcAddress2,zipCode,city,lstName,fstName,dtBirth,ahvNr
    FROM Invoice iv LEFT JOIN Person ps on iv.fkPerson=ps.id'''
    sqlTplOrd='ORDER BY iv.id'''

    if sqlFilt is None:
      sqlRng=sqlTplRng+' '+sqlTplOrd
    else:
      sqlRng=sqlTplRng+' WHERE '+sqlFilt+' '+sqlTplOrd

    sqlTplBeh='''SELECT dtTreatment,costPerHour,duration,comment,tarZif FROM Treatment tr
    WHERE tr.fkInvoice=%s
    ORDER BY tr.dtTreatment'''
    repIvc=report.Invoice(fn)

    for recRng in dbcRng.execute(sqlRng):
      print(recRng)
      sqlBeh=sqlTplBeh%recRng[0]
      dbcBeh=dbcBeh.execute(sqlBeh)
      dBeh=dbcBeh.fetchall()
      print(dBeh)
      repIvc.add(recRng[3:],recRng[1],recRng[2],dBeh)#  add(klient,tplID,datRng,behandlungen):

    repIvc.publish()
    report.default_app_open(fn);

  def report_therapy_progress(self, sqlFilt=None,fn='therapy_progress.pdf'):
    db=self.db
    dbcRng=self.dbc
    dbcBeh=db.cursor()

    sqlTplBeh='SELECT fkPerson,lstName,fstName,dtBirth,phone,eMail,dtTreatment,tr.comment,document FROM Treatment tr LEFT JOIN Person ps ON tr.fkPerson=ps.id'
    sqlTplOrd='ORDER BY fkPerson,tr.dtTreatment'''

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

  def sync_invoice(self,fn='Kontoauszug_2020_10_09.csv'):
    import csv,re,time
    db=self.db
    dbc=self.dbc
    dbc.execute("SELECT dtEvent,comment,refNr,refText,amount FROM Account")
    #dbc.execute("SELECT dtEvent+refNr+comment+refText,amount FROM Account")
    account=dbc.fetchall()
    account=set(account)

    fh = open(fn)
    rows = csv.reader(fh,delimiter=';')
    sqlData=[]
    header=rows.__next__()
    #['\ufeffDatum', 'Valuta', 'Buchungstext', 'Belastung', 'Gutschrift', 'Saldo']
    for refDat,valuta,text,belastung,gutschrift,saldo in rows:
      if gutschrift!='':
        amount=float(gutschrift.replace("'",''))
      else:
        amount=-float(belastung.replace("'",''))
      dtEvent=refDat
      dtEvent=time.strptime(dtEvent,'%d.%m.%Y')
      dtEvent=time.strftime('%Y-%m-%d',dtEvent)
      #re.match('(.*?)([/\s]+Ref\.*-Nr\.*\s*)(\d*)(\s*)(.*)',text).groups()
      m=re.match('\s+(.*?)[/\s]+Ref\.*-Nr\.*\s*(\d*)\s*(.*)',text)
      if m:
        comment,refNr,refText=m.groups()
        refText=refText.strip()
        refNr=int(refNr)
      else:
        comment=text.strip()
        refNr=refText=None
      #key=dtEvent+str(refNr)+comment+refText
      key=(dtEvent,comment,refNr,refText,amount)
      if key in account:
        print('ignore duplicate:',key)
        continue
      sqlData.append((dtEvent,comment,refNr,refText,amount))

    dbc.executemany("INSERT INTO Account (dtEvent,comment,refNr,refText,amount) VALUES (?,?,?,?,?)", sqlData)
    db.commit()
    #db.close()
    #try:
    #except lite.Error as e:
    #  print(schema+" Error %s:" % e.args[0])



if __name__=='__main__':

  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('-m', '--mode', type=int, help='mode bits', default=0x0)
  args = parser.parse_args()
  print(args)
  mkb=MoKaBu('mokabu.db')
  #mkb.open()
  #mkb.reset()
  #mkb.populate()
  if args.mode&1:
    mkb.report_invoice();exit(0)
  if args.mode&2:
    mkb.report_therapy_progress();exit(0)
  if args.mode&4:
    mkb.sync_invoice();exit(0)


  import qtgui
  dbg=1#+2+4
  qtgui.MainApp(mkb,dbg)

  mkb.close()

