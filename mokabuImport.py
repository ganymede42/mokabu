#!/usr/bin/python3
'''
retrieves all usefull data out of the existing bills

find /media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten -name Rech*.docx
echo '' > 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Kratz-Ulmer Aline/Rechnung_20191213.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Kratz-Ulmer Aline/Rechnung_20200205.docx' >> 2020_Klienten.txt
...
'''

import os,sys,re,time
import subprocess as spc
from  pathlib import Path as plPath
import sqlite3 as lite

def getline(fh,errStr='getline:%s:error'):
  l=fh.readline()
  if l=='':
    raise IOError(errStr%fh.name)
  return l[:-1]

def dateconvert(dateStr,errStr='dateconvert'):
  #https://www.sqlitetutorial.net/sqlite-date/
  #time.time() # epoch time (Seconds since 1.1.1970)
  #time.gmtime() struct of current time
  #time.mktime(time.gmtime()) #convert struct to epoch time
  #time.strptime("30 Nov 00", "%d %b %y")  convert string to struct
  for fmt in ("%d.%m.%y","%d.%m.%Y"):
    try:
      dateStruct=time.strptime(dateStr,fmt)
    except ValueError:
      continue
    break
  try:
    #dateEpoch=int(time.mktime(dateStruct)) # conver struct to second since 1.1.1970
    dateEpoch=time.strftime('%Y-%m-%d',dateStruct)
    #dateEpoch=int(time.strftime('%Y%m%d',dateStruct))
  except UnboundLocalError as e:
    raise UserWarning(str(dateStr))
  return dateEpoch



def insert_verlauf(rec,dateStr,title,eintrag,fh):
  if dateStr is not None:
    try:
      date=dateconvert(dateStr,str(rec))
    except UserWarning as e:
      print('insert_verlauf(1)'+fh.name+':error in dateconvert:"%s"'%str(dateStr),file=sys.stderr)
      date=0
    t=1;dt=date
    while dt in rec:
      print('insert_verlauf(1): warning dupkicate key:',fh.name,dateStr,dt,file=sys.stderr)
      dt=date + ' 00:%.2d'%t;t+=1

    eintrag='\n'.join(eintrag)
    eintrag=eintrag.strip()
    #eintrag.replace('\n','<br/>\n')
    title=title.strip()

    rec[dt]=(title,eintrag)

class ImportData:

  def __init__(self):
    fn='/tmp/mokabu/import.log'
    print(' logging to file: '+fn)
    os.makedirs(plPath(fn).parent.as_posix(),exist_ok=True)
    self.log=open(fn,'w')

  @staticmethod
  def docx2txt_invoices(srcPath,dstPath):
    print('--- docx2txt_invoices ---')
    os.makedirs(dstPath,exist_ok=True)
    print('reading files '+srcPath+'/*Rechnung*.doc*')
    for path in plPath(srcPath).rglob('*Rechnung*.doc*'):
      if path.name.startswith('.~lock') or path.name.startswith('~$') or\
        path.name.find('Zahlungserinnerung')>=0:
        print('docx2txt_invoices(1): ignored:'+path.as_posix(),file=sys.stderr)
        continue  #ignore

      fnSrc=path.as_posix()
      fnDst=plPath(dstPath).joinpath(path.parts[-2]+'#'+path.stem+'.txt' ).as_posix()
      fnDst=fnDst.replace(' ','_')
      #print('docx2txt',fnSrc,fnDst)
      #print(fnDst)
      res=spc.Popen(('docx2txt',fnSrc,fnDst)).wait()
    pass

  @staticmethod
  def docx2txt_treatments(srcPath,dstPath):
    print('--- docx2txt_treatments ---')
    print('reading files '+srcPath+'/*Verlauf*.doc*')
    os.makedirs(dstPath,exist_ok=True)
    for path in plPath(srcPath).rglob('*Verlauf*.doc*'):
      if path.name.startswith('.~lock') or path.name.startswith('~$'):
        print('docx2txt_invoices(1): ignored:'+path.name,file=sys.stderr)
        continue #ignore
      fnSrc=path.as_posix()
      if path.parts[-2]!=path.stem.replace('_Verlauf',''):
        print('docx2txt_treatments(2): Filename warning:'+path.parts[-2]+' <-> '+path.stem, file=sys.stderr)

      fnDst=plPath(dstPath).joinpath(path.parts[-2]+'#'+path.stem+'.txt').as_posix()
      fnDst=fnDst.replace(' ','_')
      #print('docx2txt',fnSrc,fnDst)
      #print(fnDst)

      if fnSrc.endswith('docx'):
        res=spc.Popen(('docx2txt',fnSrc,fnDst)).wait()
      else:
        p=spc.Popen(('catdoc',fnSrc),stdout=spc.PIPE)
        res=p.wait()
        fh=open(fnDst,'wb')
        fh.write( p.stdout.read())
        fh.close()
    pass

  def parse_invoices(self,srcPath):
    print('--- parse_invoices ---')
    self.dbRawIvc=dbRawIvc=list() #invoice raw database
    self.lutKlient2Path=lutKlient2Path=dict() #database klienten to path
    #fnLst=('/tmp/mokabu/invoice/Hermann_Estella_Luisa_Rechnung_20200805.txt', #missing geb:
  #     I                           '/tmp/mokabu/invoice/Preisig_Lukas_Rechnung_200925.txt') #missing geb:
    #for fn in fnLst:
    for path in sorted(plPath(srcPath).glob('*Rech*.txt')):
      fn=path.as_posix()
      fh=open(fn,'r')
      try:
        rec=ImportData.read_klient(fh)
        dbRawIvc.append(rec)

        keyKlient=ImportData.gen_klient_key(rec[1][:3])
        keyPath=path.stem.split('#',1)[0]
        try:
          keyPathOld=lutKlient2Path[keyKlient]
        except KeyError:
          lutKlient2Path[keyKlient]=keyPath
        else:
          if keyPathOld!=keyPath:
            print("parse_invoices(1): Duplicate Keys: Error client:'%s' paths:'%s', '%s'"%(keyKlient,keyPathOld,keyPath),file=sys.stderr)
        print(fn,keyPath,keyKlient,file=self.log)
      except IOError as e:
        print(e, file=sys.stderr)
      fh.close()

  @staticmethod
  def gen_klient_key(rec):
    na,vo,geb=rec
    if geb is None:
      gebStr='None'
    else:
      #gebStr=time.strftime('%d.%m.%Y',time.gmtime(geb))
      gebStr=str(geb)
    return na+'#'+vo+'#'+gebStr

  @staticmethod
  def read_klient(fh):
    while True:
      l=getline(fh,'read_klient(1):%s:error_ "monika.kast-perry@psychologie.ch" not found')
      if l.find('monika.kast-perry@psychologie.ch')>=0:
        break

    rchAdr=list()
    while True:
      l=getline(fh,'read_klient(2):%s:error_ "Zürich," not found')
      if l.startswith('Zürich,'):
        try:
          rchDatStr=l.split(', ',1)[1]
        except BaseException as e:
          print(e, file=sys.stderr)
          rchDatStr=None
        break
      if len(l)>0:
        rchAdr.append(l)

    while True:
      l=getline(fh,'read_klient(3):%s:error_ "geb:" not found')
      if l.find('geb:')>=0:
        klient,gebDatStr=l.split('geb:')
        gebDatStr=gebDatStr.strip()
        if gebDatStr.find('AHV-Nr.')>=0:
          gebDatStr,AHVNr=gebDatStr.split('AHV-Nr.')
          gebDatStr=gebDatStr.split(', ',1)[0]
        else:
          AHVNr=None

        klient=klient.strip(', ')
        klient=klient.lstrip('Therapie für ')
        klNa,klVo=klient.rsplit(' ',1)
        if klNa=='Nachname':
          print('read_klient(4)'+fh.name+':error suspicious name:',(klNa,klVo),file=sys.stderr)
        break

    beh=list()
    while True:
      l=getline(fh,'read_klient(5):%s:error_ "Ich bitte Sie," not found')
      if l.startswith('Ich bitte Sie,') or l.startswith('Bitte überweisen Sie'):
        break
      if len(l)>0:
        beh.append(l)

      #Anrede,Name_Vorname,Strasse,PLZ_Ort=rchAdr
      Anrede=rchAdr[0]
      Name_Vorname=rchAdr[1]
      try:
        Name,Vorname=Name_Vorname.rsplit(maxsplit=1)
      except ValueError:
        Name=Name_Vorname
        Vorname=None

      Adresse=rchAdr[-2]
      PLZ_Ort=rchAdr[-1]
      Addrzusatz=rchAdr[2:-2]
      Adresse1=Adresse2=None
      try:
        Adresse1=Addrzusatz[0]
      except IndexError as e:
        pass
      try:
        Adresse2=Addrzusatz[1]
      except IndexError as e:
        pass


    try:
        PLZ,Ort=PLZ_Ort.split(maxsplit=1)
    except ValueError as e:
      print('read_klient(6)'+fh.name+':error in PLZ_Ort:',PLZ_Ort,e,file=sys.stderr)
      PLZ=None
      Ort=PLZ_Ort

    #return (rchAdr,(klNa,klVo,geb),beh)
    try:
      gebDat=dateconvert(gebDatStr)
    except UserWarning as e:
      print('read_klient(7)'+fh.name+':error in dateconvert:"%s"'%str(gebDatStr),file=sys.stderr)
      gebDat=None
    try:
      rchDat=dateconvert(rchDatStr)
    except UserWarning as e:
      print('read_klient(7)'+fh.name+':error in dateconvert:"%s"'%str(rchDatStr),file=sys.stderr)
      rchDat=None

    return ((Anrede,Name,Vorname,Adresse,Adresse1,Adresse2,PLZ,Ort),(klNa,klVo,gebDat,AHVNr),rchDat,beh)


  @staticmethod
  def split_behandlung(behRaw):
    beh=list()
    #tarif preis pro 60 min
    #zeit in minuten
    #datum,tarif,zeit,Bemerkung,tarZif
    tpl=tuple(map(lambda x:x.strip(' :'),behRaw[0].strip().split('\t')))
    if tpl==('Daten','Minuten / Ansatz pro h','Kosten','Total') or\
       tpl==('Daten','Minuten / Ansatz pro 1h','Kosten','Total') or\
       tpl==('Daten','Minuten / Ansatz','Kosten','Total'):
        #print('format 1')
        for r in behRaw[1:]:
          if r.strip()=='': continue
          rs=r.split('\t')
          try:
            z,t=rs[1].split('/')[-2:]
          except ValueError:
            raise ValueError(r)
          else:
            z=z.replace('min','').strip(' .')
            t=t.replace('SFr','').strip(' .')
            d=dateconvert(rs[0])
          beh.append((d,float(t),float(z),None,None))

    elif tuple(map(lambda x:x.strip(' :'),behRaw[0:4]))==('Datum','Inhalt','Minuten','Betrag') or \
         tuple(map(lambda x:x.strip(' :'),behRaw[0:4]))==('Datum','Inhalt','Zeit','Kosten') or \
         tuple(map(lambda x:x.strip(' :'),behRaw[0:4]))==('Datum','Inhalt','Zeit','Betrag'):
        #print('format 2')
        n=(len(behRaw)-4-3)//4
        if (len(behRaw)!=n*4+4+3):
          n=(len(behRaw)-4)//4
          print('(1)wrong counts!',len(behRaw), file=sys.stderr)
          #print('wrong counts!',len(behRaw),behRaw,file=sys.stderr)
        if behRaw[-2].find('Total')<0:
          print('(2)missing Total!',file=sys.stderr)#,behRaw[-4:], file=sys.stderr)
        for i in range(n):
          r=behRaw[4+4*i:8+4*i]
          #datum,tarif,zeit,Bemerkung,tarZif
          d=dateconvert(r[0])
          b=r[1]
          z=r[2].replace('min','')
          t=60*float(r[3].replace('CHF','').strip())/float(z)
          beh.append((d,t,float(z),b,None))

    elif tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Minuten','Betrag') or \
        tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Zeit in Min','Kosten') or \
        tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Zeit in Min','Betrag') or \
        tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Zeit','Kosten') or\
        tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Zeit in min','Kosten') :
        #print('format 3')
        n=(len(behRaw)-6-5)//6
        if len(behRaw)!=n*6+6+5:
          n=(len(behRaw)-6)//6
          print('(3)wrong counts!',len(behRaw), file=sys.stderr)
          #assert(len(behRaw)==n*6+6+5)
        if behRaw[-2].find('Total')<0:
          print('(4)missing Total!',file=sys.stderr)#,behRaw[-6:], file=sys.stderr)
          #assert(behRaw[-2].find('Total')>=0)
        for i in range(n):
          r=behRaw[6+6*i:12+6*i]
          #datum,tarif,zeit,Bemerkung,tarZif
          d=dateconvert(r[0])
          b=r[3]
          z=r[4].replace('min','').replace('Zeilen','').strip()
          t=60*float(r[5].replace('CHF','').strip())/float(z)
          beh.append((d,t,float(z),b,r[2]))

    elif tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Ansatz 35.50 Fr. pro 15 min/ Anzahl','Kosten'):
        #print('format 4')
        n=(len(behRaw)-6-5)//6
        if len(behRaw)!=n*6+6+5:
          n=(len(behRaw)-6)//6
          print('(5)wrong counts!',len(behRaw), file=sys.stderr)
          #assert(len(behRaw)==n*6+6+5)
        if behRaw[-2].find('Total')<0:
          print('(6)missing Total!',file=sys.stderr)#,behRaw[-6:], file=sys.stderr)
          #assert(behRaw[-2].find('Total')>=0)
        for i in range(n):
          r=behRaw[6+6*i:12+6*i]
          #datum,tarif,zeit,Bemerkung,tarZif
          d=dateconvert(r[0])
          b=r[3]
          z=float(r[4].strip())*15
          t=60*float(r[5].replace('CHF','').replace('Fr.','').strip())/float(z)
          beh.append((d,t,float(z),b,r[2]))
    else:
      print(behRaw[:6], file=sys.stderr)
      raise ValueError('Unknown Format')

    return beh

  def parse_treatments(self,srcPath):
    print('--- parse_treatments ---')
    self.dbRawTrt=dbRawTrt=dict()
    for path in sorted(plPath(srcPath).glob('*.txt')):
      fn=path.as_posix()
      fh=open(fn,'r')
      try:
        rec=ImportData.read_verlauf(fh)
        print(fn,rec.keys(),file=self.log)
        key=path.stem.split('#')[0]
        if key in dbRawTrt:
          print('duplicated keys:',key, file=sys.stderr)
          print(dbRawTrt[key].keys() & rec.keys())
          dbRawTrt[key].update(rec)
        else:
          dbRawTrt[key]=rec
        #print(rec[0],rec[1])
      except IOError as e:
        print(e, file=sys.stderr)
      fh.close()

  @staticmethod
  def read_verlauf(fh):
    rec=dict()
    dateStr=title=None;eintrag=[]
    for l in fh.readlines():
      m=re.match('\d*\.\d*\.\d*',l)
      if m:
        insert_verlauf(rec,dateStr,title,eintrag,fh)
        try:
          dateStr,title=l.split(maxsplit=1)
        except ValueError as e:
          print('read_verlauf(1):',fh.name,e, file=sys.stderr)
        eintrag=[]
      else:
        try:
          eintrag.append(l.strip())
        except UnboundLocalError as e:
          print('read_verlauf(2):',fh.name,e,file=sys.stderr)
          print(l.strip())

    insert_verlauf(rec,dateStr,title,eintrag,fh)
    return rec

  def rawdb2relational(self):
    print('--- rawdb2relational ---')
    dbRawIvc=self.dbRawIvc
    dbRawTrt=self.dbRawTrt
    self.lutKlient2pk=lutKlient2pk=dict() #database klienten
    self.dbKlient=dbKlient=list() #database klienten
    self.dbRch=dbRch=list() #database Rechnungen
    self.dbBeh=dbBeh=list() #database Behandlungen
    lutKlient2Path=self.lutKlient2Path

    idNewKlient=1
    idBeh=1
    idRch=1
    for (rchAddr,client,rchDat,behRaw) in dbRawIvc:
      keyKlient=ImportData.gen_klient_key(client[:3])
      try:
        pkKlient=lutKlient2pk[keyKlient]
      except KeyError:
        pkKlient=idNewKlient
        lutKlient2pk[keyKlient]=pkKlient
        dbKlient.append((pkKlient,)+rchAddr+client)
        idNewKlient+=1
      #print(keyKlient,pkKlient)
      dbRch.append((idRch,pkKlient,rchDat))

      #### analyze behandlung
      try:
        behLst=ImportData.split_behandlung(behRaw)
      except UserWarning as e:
        print('rawdb2relational(1):error in dateconvert:"',e,client,behRaw,file=sys.stderr)

      print(keyKlient, tuple(map(lambda x: x[0],behLst)),file=self.log)
      try:
        trtDict=dbRawTrt[lutKlient2Path[keyKlient]]
      except KeyError:
        print('rawdb2relational(1) No akteneingtrag at all',keyKlient,file=sys.stderr)
        trtDict={}

      for beh in behLst:
        try:
          #trt=trtDict[rec[0]]
          trt=trtDict.pop(beh[0])
        except KeyError:
          #print('rawdb2relational(2):warning: no akteneingtrag',keyKlient,beh[0],time.strftime('%d.%m.%Y',time.gmtime(beh[0])),file=sys.stderr)
          print('rawdb2relational(2):warning: no akteneingtrag',keyKlient,beh[0],file=sys.stderr)
          bem=verl=None
        else:
          bem=trt[0].strip()
          verl=trt[1]
        rec=[idBeh,idRch,pkKlient,];rec.extend(beh)
        if bem is not None:
          #if rec[-2] is not None:
          #  print('rawdb2relational(3):info: dupl Bemerkung:',keyKlient,(rec[-2],bem),file=sys.stderr)  #+rec[-2]+'|',bem+'|',file=sys.stderr)
          rec[-2]=bem
        rec.append(verl)
        dbBeh.append(tuple(rec))
        idBeh+=1
      idRch+=1

    print('--- unlinked treatment entries (not in any invoice)--- ')
    lutPath2pk=dict()
    for k,v in lutKlient2Path.items():
      vv=lutKlient2pk[k]
      lutPath2pk[v]=vv

    for k,behDict in dbRawTrt.items():
      if len(behDict)>0:
        print(k,':',behDict.keys())
        for kDat,trt in behDict.items():
          pkKlient=lutPath2pk.get(k)
          if pkKlient is None:
            print('rawdb2relational(4) unknown key:',k,file=sys.stderr)

          bem=trt[0].strip()
          verl=trt[1]
          dbBeh.append((idBeh,None,pkKlient,kDat,None,None,bem,None,verl))
          idBeh+=1

  def write_sql(self,fnSql='2020_Klienten.sql'):
    print('--- write_sql ---')
    dbKlient=self.dbKlient
    dbRch=self.dbRch
    dbBeh=self.dbBeh

    fh=open(fnSql,'w')

    fh.write('INSERT INTO Person (id,ivcAnrede,ivcLstName,ivcFstName,ivcAddress,ivcAddress1,ivcAddress2,zipCode,city,lstName,fstName,dtBirth,ahvNr) VALUES\n')
    fh.write('('+'),\n('.join((map(lambda rec:','.join(map(lambda s:'NULL' if s is None else repr(s),rec)),dbKlient)))+');\n\n\n')
    #fh.write(',\n'.join(map(str,dbKlient)))

    fh.write('INSERT INTO Invoice (id,fkPerson,dtInvoice) VALUES\n')
    fh.write('('+'),\n('.join((map(lambda rec:','.join(map(lambda s:'NULL' if s is None else repr(s),rec)),dbRch)))+');\n\n\n')
    #fh.write(',\n'.join(map(str,dbRch)))

    fh.write('INSERT INTO Treatment (id,fkInvoice,fkPerson,dtTreatment,costPerHour,duration,comment,tarZif,document) VALUES\n')
    fh.write('('+'),\n('.join((map(lambda rec:','.join(map(lambda s:'NULL' if s is None else repr(s),rec)),dbBeh)))+');\n\n\n')
    fh.close()
    print('write_sql file %s done.'%fnSql)

  def exec_sql(self,fnSchema='mokabu.schema.sql',fnDatabase='mokabu.db'):
    print('--- exec_sql ---')
    dbKlient=self.dbKlient
    dbRch=self.dbRch
    dbBeh=self.dbBeh
    try:
      db=lite.connect(fnDatabase)
      dbc=db.cursor()
      dbc.execute('SELECT SQLITE_VERSION()')
      data = dbc.fetchone()
      print("SQLite version: %s" % data)
      dbc.execute("PRAGMA foreign_keys = 1")
    except lite.Error as e:
      print("exec_sql(1), Error %s:" % e.args[0],e,file=sys.stderr)
      return

    try:
      fh=open(fnSchema,'r')
      dbc.executescript(fh.read())
    except lite.Error as e:
      print("exec_sql(2),"+fnSchema+" Error %s:"%e.args[0],e,file=sys.stderr)
      return

    try:
      dbc.executemany(
        'INSERT INTO Person (id,ivcPrefix,ivcLstName,ivcFstName,ivcAddress,ivcAddress1,ivcAddress2,zipCode,city,lstName,fstName,dtBirth,ahvNr) VALUES\n'\
        '(?,?,?,?,?,?,?,?,?,?,?,?,?)',dbKlient)

      dbc.executemany(
        'INSERT INTO Invoice (id,fkPerson,dtInvoice) VALUES\n'\
        '(?,?,?)',dbRch)

      dbc.executemany(
        'INSERT INTO Treatment (id,fkInvoice,fkPerson,dtTreatment,costPerHour,duration,comment,tarZif,document) VALUES\n'\
        '(?,?,?,?,?,?,?,?,?)',dbBeh)

      for sql in ('SELECT COUNT(*) FROM Person',
                  'SELECT COUNT(*) FROM Invoice',
                  'SELECT COUNT(*) FROM Treatment'):
        print(sql+' -> ',end='')
        for row in dbc.execute(sql):
          print(row)
      db.commit()
      db.close()

    except lite.Error as e:
      print("exec_sql(3), Error %s:"%e.args[0],e,file=sys.stderr)
      return
    print('exec_sql done.')


if __name__=='__main__':


  import os,sys,argparse #since python 2.7
  def GetParser(required=True):
    exampleCmd='--host=PPMACZT84 --elem g io m1 c1 m2'
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__,
                                     epilog='Example:\n'+os.path.basename(sys.argv[0])+' '+exampleCmd+'\n ')
    parser.add_argument('--force', '-f', action='store_true', help='force doc2txt')
    parser.add_argument('-p','--srcpath', default='/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten', help='source path')
    return parser

  parser=GetParser()
  args = parser.parse_args()

  impDat=ImportData()
  path='/tmp/mokabu/invoice'
  if args.force or not os.path.exists(path):
    impDat.docx2txt_invoices(args.srcpath,path)
  path='/tmp/mokabu/treatment'
  if args.force or not os.path.exists(path):
    impDat.docx2txt_treatments(args.srcpath,path)

  impDat.parse_invoices('/tmp/mokabu/invoice')
  impDat.parse_treatments('/tmp/mokabu/treatment')
  impDat.rawdb2relational()
  impDat.write_sql()
  impDat.exec_sql()



