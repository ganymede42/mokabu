#!/usr/bin/python3
'''
retrieves all usefull data out of the existing bills

find /media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten -name Rech*.docx
echo '' > 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Kratz-Ulmer Aline/Rechnung_20191213.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Kratz-Ulmer Aline/Rechnung_20200205.docx' >> 2020_Klienten.txt
...
'''

import os,sys,re
import subprocess as spc
from  pathlib import Path as plPath
import sqlite3 as lite

def getline(fh,errStr='getline'):
  l=fh.readline()
  if l=='':
    raise IOError(errStr+': error in '+fh.name)
  return l[:-1]

def insert_verlauf(rec,date,title,eintrag):
  if date is not None:
    if date in rec:
      print('insert_verlauf(1): Dupkicate key:',date,file=sys.stderr)
    else:
      #eintrag='\n'.join(eintrag)
      #eintrag='<br/>'.join(eintrag)

      eintrag='\n'.join(eintrag)
      eintrag=eintrag.strip()
      eintrag.replace('\n','<br/>\n')
      title=title.strip()

      rec[date]=(title,eintrag)


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
    print('reading files '+srcPath+'/*Rech*.doc*')
    for path in plPath(srcPath).rglob('*Rech*.doc*'):
      if path.name.startswith('.~lock'):
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
    print('reading files '+srcPath+'/*Verl*.doc*')
    os.makedirs(dstPath,exist_ok=True)
    for path in plPath(srcPath).rglob('*Verl*.doc*'):
      if path.name.startswith('.~lock'):
        continue #ignore
      fnSrc=path.as_posix()
      if path.parts[-2]!=path.stem.replace('_Verlauf',''):
        print('Filename warning:'+path.parts[-2]+' <-> '+path.stem, file=sys.stderr)

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
    self.db=db=list() #database
    self.lutKlient2Path=lutKlient2Path=dict() #database klienten to path
    #fnLst=('/tmp/mokabu/invoice/Hermann_Estella_Luisa_Rechnung_20200805.txt', #missing geb:
  #     I                           '/tmp/mokabu/invoice/Preisig_Lukas_Rechnung_200925.txt') #missing geb:
    #for fn in fnLst:
    for path in sorted(plPath(srcPath).glob('*Rech*.txt')):
      fn=path.as_posix()
      if fn.find('Zahlungserinnerung')>=0 or \
         fn.find('Osei_Lawrence#Rechnung_mit_Tarifziffern_20191026.txt')>=0  or \
         fn.find('Osei_Lawrence#Rechnung_mit_Tarifziffern_20200924.txtt')>=0:
        print('parse_invoices(1): ignored:'+fn,file=sys.stderr)
        continue
      fh=open(fn,'r')
      try:
        rec=ImportData.read_klient(fh)
        db.append(rec)
        keyKlient='\t'.join(rec[1][:3])
        keyPath=path.stem.split('#',1)[0]
        lutKlient2Path[keyKlient]=keyPath
        print(fn,keyPath,keyKlient,file=self.log)
      except IOError as e:
        print(e, file=sys.stderr)
      fh.close()

  @staticmethod
  def read_klient(fh):
    while True:
      l=getline(fh,'read_klient(1)')
      if l.find('monika.kast-perry@psychologie.ch')>=0:
        break

    rchAdr=list()
    while True:
      l=getline(fh,'read_klient(2)')
      if l.startswith('Zürich,'):
        try:
          rchDat=l.split(', ',1)[1]
        except BaseException as e:
          print(e, file=sys.stderr)
          rchDat=None
        break
      if len(l)>0:
        rchAdr.append(l)

    while True:
      l=getline(fh,'read_klient(3)')
      if l.find('geb:')>=0:
        klient,geb=l.split('geb:')
        geb=geb.strip()
        if geb.find('AHV-Nr.')>=0:
          geb,AHVNr=geb.split('AHV-Nr.')
          geb=geb.split(', ',1)[0]
        else:
          AHVNr=None

        klient=klient.strip(', ')
        klient=klient.lstrip('Therapie für ')
        klNa,klVo=klient.rsplit(' ',1)
        break

    beh=list()
    while True:
      l=getline(fh,'read_klient(4)')
      if l.startswith('Ich bitte Sie,'):
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
      print(e,'Error in PLZ_Ort:',PLZ_Ort, file=sys.stderr)
      PLZ=None
      Ort=PLZ_Ort

    #return (rchAdr,(klNa,klVo,geb),beh)
    return ((Anrede,Name,Vorname,Adresse,Adresse1,Adresse2,PLZ,Ort),(klNa,klVo,geb,AHVNr),rchDat,beh)

  @staticmethod
  def split_behandlung(behRaw):
    beh=list()
    #tarif preis pro 60 min
    #zeit in minuten
    #datum,tarif,zeit,Bemerkung,tarZif
    if tuple(map(lambda x : x.strip(' :'),behRaw[0].split('\t')))==('Daten', 'Minuten / Ansatz pro h', 'Kosten', 'Total') or \
       tuple(map(lambda x:x.strip(' :'),behRaw[0].split('\t')))==('Daten','Minuten / Ansatz','Kosten','Total'):
        #print('format 1')
        for r in behRaw[1:]:
          if r=='\t': continue
          rs=r.split('\t')
          try:
            z,t=rs[1].split('/')[-2:]
          except ValueError:
            raise ValueError(r)
          else:
            z=z.replace('min','').strip(' .')
            t=t.replace('SFr','').strip(' .')
          beh.append((rs[0],float(t),float(z),None,None))

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
          d=r[0]
          b=r[1]
          z=r[2].replace('min','')
          t=60*float(r[3].replace('CHF','').strip())/float(z)
          beh.append((d,t,float(z),b,None))

    elif tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Minuten','Betrag') or \
        tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Zeit in Min','Kosten') or \
        tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Zeit in Min','Betrag') or \
        tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Zeit','Kosten'):
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
          d=r[0]
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
          d=r[0]
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
    self.dbTrt=dbTrt=dict()
    for path in sorted(plPath(srcPath).glob('*.txt')):
      fn=path.as_posix()
      fh=open(fn,'r')
      try:
        rec=ImportData.read_verlauf(fh)
        print(fn,rec.keys(),file=self.log)
        key=path.stem.split('#')[0]
        if key in dbTrt:
          print('duplicated keys:',key, file=sys.stderr)
          print(dbTrt[key].keys() & rec.keys())
          dbTrt[key].update(rec)
        else:
          dbTrt[key]=rec
        #print(rec[0],rec[1])
      except IOError as e:
        print(e, file=sys.stderr)
      fh.close()

  @staticmethod
  def read_verlauf(fh):
    rec=dict()
    date=title=None;eintrag=[]
    for l in fh.readlines():
      m=re.match('\d*\.\d*\.\d*',l)
      if m:
        insert_verlauf(rec,date,title,eintrag)
        try:
          date,title=l.split(maxsplit=1)
        except ValueError as e:
          print('read_verlauf(2)',e, file=sys.stderr)
        eintrag=[]
      else:
        try:
          eintrag.append(l.strip())
        except UnboundLocalError as e:
          print('read_verlauf(2)',fh.name,e,file=sys.stderr)
          print(l.strip())

    insert_verlauf(rec,date,title,eintrag)
    return rec

  def rawdb2relational(self):
    print('--- rawdb2relational ---')
    db=self.db
    self.lutKlient2pk=lutKlient2pk=dict() #database klienten
    self.dbKlient=dbKlient=list() #database klienten
    self.dbRch=dbRch=list() #database Rechnungen
    self.dbBeh=dbBeh=list() #database Behandlungen
    lutKlient2Path=self.lutKlient2Path
    dbTrt=self.dbTrt

    idNewKlient=1
    idBeh=1
    idRch=1
    for (rchAddr,client,rchDat,behRaw) in db:
      keyKlient='\t'.join(client[:3])
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
      behLst=ImportData.split_behandlung(behRaw)
      print(keyKlient, tuple(map(lambda x: x[0],behLst)),file=self.log)
      try:
        trtDict=dbTrt[lutKlient2Path[keyKlient]]
      except KeyError:
        print('rawdb2relational(1) No akteneingtrag at all',keyKlient,file=sys.stderr)
        trtDict={}

      for beh in behLst:
        try:
          #trt=trtDict[rec[0]]
          trt=trtDict.pop(beh[0])
        except KeyError:
          print('rawdb2relational(2) No akteneingtrag',beh[0],keyKlient,file=sys.stderr)
          bem=verl=None
        else:
          bem=trt[0].strip()
          verl=trt[1]
        rec=[idBeh,idRch,pkKlient,];rec.extend(beh)
        if rec[-2] is None:
          rec[-2]=bem
        else:
          print('rawdb2relational(3) dupl Bemerkung:|',beh[0],file=sys.stderr)#+rec[-2]+'|',bem+'|',file=sys.stderr)
        rec.append(verl)
        dbBeh.append(tuple(rec))
        idBeh+=1
      idRch+=1

    print('--- unlinked treatment entries (not in any invoice)--- ')
    lutPath2pk=dict()
    for k,v in lutKlient2Path.items():
      vv=lutKlient2pk[k]
      lutPath2pk[v]=vv

    for k,behDict in dbTrt.items():
      if len(behDict)>0:
        print(k,':',behDict.keys())
        for kDat,trt in behDict.items():
          pkKlient=lutPath2pk.get(k)
          if pkKlient is None:
            print('unknown key:',k)
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
    #fh.write('INSERT INTO tblPerson (IDPerson,Anrede,Nachname,Vorname,Adresse,PLZ,Ort,Mobile,Telefon,eMail,Bemerkung) VALUES')
    fh.write('INSERT INTO tblPerson (pkPerson,RngAnrede,RngNachname,RngVorname,RngAdresse,RngAdresse1,RngAdresse2,PLZ,Ort,Nachname,Vorname,datGeb,AHVNr) VALUES\n')
    fh.write('('+'),\n('.join((map(lambda rec:','.join(map(lambda s:'NULL' if s is None else repr(s),rec)),dbKlient)))+');\n\n\n')
    #fh.write(',\n'.join(map(str,dbKlient)))

    fh.write('INSERT INTO tblRechnung (pkRechnung,fkPerson,datRechnung) VALUES\n')
    fh.write('('+'),\n('.join((map(lambda rec:','.join(map(lambda s:'NULL' if s is None else repr(s),rec)),dbRch)))+');\n\n\n')
    #fh.write(',\n'.join(map(str,dbRch)))

    fh.write('INSERT INTO tblBehandlung (pkBehandlung,fkRechnung,fkPerson,datBehandlung,Stundenansatz,Dauer,Bemerkung,TarZif,AktenEintrag) VALUES\n')
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
        'INSERT INTO tblPerson (pkPerson,RngAnrede,RngNachname,RngVorname,RngAdresse,RngAdresse1,RngAdresse2,PLZ,Ort,Nachname,Vorname,datGeb,AHVNr) VALUES\n'\
        '(?,?,?,?,?,?,?,?,?,?,?,?,?)',dbKlient)

      dbc.executemany(
        'INSERT INTO tblRechnung (pkRechnung,fkPerson,datRechnung) VALUES\n'\
        '(?,?,?)',dbRch)

      dbc.executemany(
        'INSERT INTO tblBehandlung (pkBehandlung,fkRechnung,fkPerson,datBehandlung,Stundenansatz,Dauer,Bemerkung,TarZif,AktenEintrag) VALUES\n'\
        '(?,?,?,?,?,?,?,?,?)',dbBeh)

      for sql in ('SELECT COUNT(*) FROM tblPerson',
                  'SELECT COUNT(*) FROM tblBehandlung',
                  'SELECT COUNT(*) FROM tblRechnung'):
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



