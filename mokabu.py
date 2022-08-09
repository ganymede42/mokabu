#!/usr/bin/env python
# *-----------------------------------------------------------------------*
# |                                                                       |
# |  Copyright (c) 2022 by Thierry Zamofing  (th.zamofing@gmail.com)      |
# |                                                                       |
# *-----------------------------------------------------------------------*
# -*- coding: utf-8 -*-
'''
Mokabu:
Burchhaltung für Krankenkassenabrechnung

bitmask for mode:
  0x01: report_invoice (all)
  0x02: report_therapy_progress (all)
  0x04: sync_invoice (test)


'''

#https://www.w3schools.com/sql/sql_join.asp
import logging
_log=logging.getLogger(__name__)

import sqlite3 as lite
import sys,os,time
import report
from TarZif import Lut

class MoKaBu:

  def __init__(self,fn='mokabu.db',lstErb=None):
    if not os.path.exists(fn):
      self.reset(fn)
    self.open(fn)
    self._lut=lut=Lut()
    lut.open(lstErb)

  def open(self,fn):
    try:
        self.db=db=lite.connect(fn)
        self.dbc=dbc=db.cursor()
        dbc.execute('SELECT SQLITE_VERSION()')
        data = dbc.fetchone()
        _log.debug("SQLite version: %s" % data)
        #One way of permanently turning on foreign_keys by default is to inject the following line into ~/.sqliterc: PRAGMA foreign_keys = ON;
        dbc.execute("PRAGMA foreign_keys = 1")
        #dbc.execute("PRAGMA foreign_keys")
        for sql in('SELECT COUNT(*) FROM Person',
                   'SELECT COUNT(*) FROM Treatment',
                   'SELECT COUNT(*) FROM Invoice',
                   'SELECT COUNT(*) FROM Account',
                   'SELECT COUNT(*) FROM EventLog',
                   'SELECT COUNT(*) FROM EventType'):
          for row in dbc.execute(sql):
            _log.debug(f'{sql} -> {row}')
    except lite.Error as e:
        _log.error("Error %s:" % e.args[0])
        sys.exit(1)

  def close(self):
    try:
        self.db.close()
    except lite.Error as e:
        _log.error("Error %s:" % e.args[0])


  def reset(self,fn):
    schema='mokabu.schema.sql'
    _log.warning(f'database {fn} does not exist. It will be build according to schema {schema}')
    try:
      db=lite.connect(fn)
      dbc=db.cursor()
      fh=open(schema,'r')
      dbc.executescript(fh.read())
    except lite.Error as e:
        _log.error(schema+" Error %s:" % e.args[0])

  def report_invoice(self, sqlFilt=None,fn='invoice.pdf',pkInvoice=None):
    #if pkInvoice is set, the filter and the filename is generated
    db=self.db
    dbc=self.dbc
    if pkInvoice:
      sqlFilt='iv.id=%d'%pkInvoice
      sqlData=dbc.execute('SELECT fstName,lstName,dtInvoice,tplInvoice FROM Person ps LEFT JOIN Invoice iv ON ps.id=iv.fkPerson WHERE iv.id=%d'%pkInvoice).fetchone()
      path='invoice'
      try:
        os.mkdir(path)
      except FileExistsError:
        pass
      try:
        tpl='_%d'%int(sqlData[3])
      except (ValueError,TypeError):
        tpl=''
      try:
        dateStruct=time.strptime(sqlData[2],'%Y-%m-%d')
        dtTxt=time.strftime('%y%m%d',dateStruct)
      except (ValueError,TypeError) as e:
        print('error in dateconvert:"%s"'%str(sqlData[2]),file=sys.stderr)
        dtTxt='xx_xx_xx'
      fn=os.path.join(path,'Rng'+str(sqlData[1])+str(sqlData[0])+dtTxt+tpl+'.pdf')

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
    repIvc=report.Invoice(fn,self._lut)

    for recRng in dbcRng.execute(sqlRng):
      _log.debug(recRng)
      sqlBeh=sqlTplBeh%recRng[0]
      dbcBeh=dbcBeh.execute(sqlBeh)
      dBeh=dbcBeh.fetchall()
      _log.debug(dBeh)
      try:
        krzLstErb= self._lut._krzLstErb
      except AttributeError:
        if recRng[9] and int(recRng[9])<8000: #PLZ is not in ZH
          krzLstErb='MK_A'
        else:
          krzLstErb='MK_Z'
      ##if app..ar
      ##  lstErb
      repIvc.build(recRng[1],krzLstErb,recRng[3:], (recRng[0],recRng[2]),dBeh)#  add(klient,tplID,datRng,behandlungen):

    repIvc.publish()
    report.default_app_open(fn);

  def report_therapy_progress(self, sqlFilt=None,fn='therapy_progress.pdf',pkPerson=None):
    db=self.db

    db=self.db
    dbc=self.dbc
    if pkPerson:
      sqlFilt='fkPerson=%d'%pkPerson
      sqlFilt='ps.id=%d'%pkPerson
      sqlData=dbc.execute('SELECT fstName,lstName FROM Person ps WHERE id=%d'%pkPerson).fetchone()
      path='therapy_progress'
      try:
        os.mkdir(path)
      except FileExistsError:
        pass
      fn=os.path.join(path,'Verlauf'+str(sqlData[1])+str(sqlData[0])+'.pdf')

    sqlTplBeh='SELECT fkPerson,lstName,fstName,dtBirth,phone,eMail,dtTreatment,tr.comment,document FROM Treatment tr LEFT JOIN Person ps ON tr.fkPerson=ps.id'
    sqlTplOrd='ORDER BY fkPerson,tr.dtTreatment'''

    if sqlFilt is None:
      sqlBeh=sqlTplBeh+' '+sqlTplOrd
    else:
      sqlBeh=sqlTplBeh+' WHERE '+sqlFilt+' '+sqlTplOrd

    repBeh=report.TherapyProgress(fn)

    fkCurPerson=-1
    for recBeh in dbc.execute(sqlBeh):
      fkPerson=recBeh[0]
      if fkPerson!=fkCurPerson:
        fkCurPerson=fkPerson
        repBeh.addClient(*recBeh[1:6])
      repBeh.addTherapyProgress(*recBeh[6:9])
    repBeh.publish()
    report.default_app_open(fn);

  def sync_invoice(self,fn='Kontoauszug_2020_10_09.csv',verbose=False):
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
    cntIgn=0
    for r in rows:
      refDat,valuta,text,belastung,gutschrift,saldo=r[:6]
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
        if verbose: print('ignore duplicate:',key)
        cntIgn+=1
        continue
      sqlData.append((dtEvent,comment,refNr,refText,amount))

    cntAdd=len(sqlData)
    dbc.executemany("INSERT INTO Account (dtEvent,comment,refNr,refText,amount) VALUES (?,?,?,?,?)", sqlData)
    db.commit()
    if verbose: print('sync_invoice: ignored:%d added:%d'%(cntIgn,cntAdd))
    return (cntIgn,cntAdd)


if __name__=='__main__':
  import argparse
  epilog=__doc__ #+'\nExamples:'+''.join(map(lambda s:cmd+s, exampleCmd))+'\n'
  parser=argparse.ArgumentParser(epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-m', '--mode', type=lambda x: int(x,0), help='mode (see bitmasks) default=0x%(default)x', default=0x0)
  parser.add_argument("--database", help="database file", default='mokabu.db')
  parser.add_argument("-l", "--loglevel", type=int, help="50:Critical 4:Error 3:Warning 2:Info 1:DEBUG default=%(default)u", default=2)
  parser.add_argument('--lstErb', help='Kürzel Leistungserbringer', default=None)
  args = parser.parse_args()
  _log.debug(args)
  #logging.basicConfig(level=logging.DEBUG, format='%(name)s%(levelname)s:%(module)s:%(lineno)d:%(funcName)s:%(message)s ')
  logging.basicConfig(level=args.loglevel*10, format='%(levelname)s:%(module)s:%(lineno)d:%(funcName)s:%(message)s ')


  mkb=MoKaBu(args.database,args.lstErb)
  if args.mode&1:
    mkb.report_invoice();exit(0)
  if args.mode&2:
    mkb.report_therapy_progress();exit(0)
  if args.mode&4:
    mkb.sync_invoice('Kontoauszug_15.11.2020 11_07_49.csv');exit(0)


  import qtgui
  dbg=0#16#0xf8
  qtgui.MainApp(mkb,dbg)

  mkb.close()

