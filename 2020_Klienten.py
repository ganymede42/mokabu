#!/usr/bin/python3
'''
find /media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten -name Rech*.docx

echo '' > 2020_Klienten.txt


docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Kratz-Ulmer Aline/Rechnung_20191213.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Kratz-Ulmer Aline/Rechnung_20200205.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Beyraktar Aras/Rechnung_200317.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Caracino Alice Maria/Rechnung_200826.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Cunte Rui/Rechnung_20200125.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Dearing Bella/Rechnung_200704.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Dearing Max/Rechnung_200704.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Dolinski Filip/Rechnung_20191220.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Dolinski Filip/Rechnung_20200131.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Dolinski Filip/Rechnung_20200320.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Dolinski Filip/Rechnung_20200612.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Drescher/Rechnung_200420.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Driksell Anastasia/Rechnung_200515.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Driksell Anastasia/Rechnung_200612.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Dünner Nadine/Rechnung_200309.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Faira Lourenco/Rechnung_200317.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Faira Lourenco/Rechnung_200417.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Faira Lourenco/Rechnung_200501.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Faira Lourenco/Rechnung_200612.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Ferrini Maxime/Rechnung_20190816.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Ferrini Maxime/Rechnung_20191110.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Ferrini Maxime/Rechnung_20200717.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Gysler Fabrice/Rechnung_200626.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Gysler Fabrice/Rechnung_200731_nicht verschickt.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Gysler Fabrice/Rechnung_200817.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Hermann Estella Luisa/Rechnung.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Hermann Estella Luisa/Rechnung_20200805.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Herz Joav/Rechnung_20191122.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Herz Joav/Rechnung_20200207.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Herz Joav/Rechnung_20200618.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Hägler Julian/Rechnung_20200925.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Krasniqi Valerijana/Rechnung_20200214.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Lauff Arthur/Rechnung_200911.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Lauff Arthur/Rechnung_200925.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Lötscher Céline/Rechnung_200826.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Lötscher Céline/Rechnung_200923.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Maman Myriam/Rechnung_200714.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Markus Alli/Rechnung_200623.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Murlot Janis/Rechnung_20191026.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Murlot Janis/Rechnung_mit Tarifziffer_20191026.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Murlot Janis/Rechnung_mit Tarifziffer_20191220.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Murlot Janis/Rechnung_mit Tarifziffer_20200214.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Osei Lawrence/Rechnung mit Tarifziffern_20191026.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Osei Lawrence/Rechnung mit Tarifziffern_20191220.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Osei Lawrence/Rechnung mit Tarifziffern_20200214.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Osei Lawrence/Rechnung mit Tarifziffern_20200320.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Osei Lawrence/Rechnung mit Tarifziffern_20200529.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Osei Lawrence/Rechnung mit Tarifziffern_20200529_korrigiert.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Osei Lawrence/Rechnung mit Tarifziffern_20200529_korrigiert_2.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Osei Lawrence/Rechnung mit Tarifziffern_20200626.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Osei Lawrence/Rechnung mit Tarifziffern_20200924.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Osei Lawrence/Rechnung_20191026.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Pedrett/Rechnung_20200911.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Preisig Lukas/Rechnung_200925.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Radic Baumgartner Ksenija/Rechnung_20190628.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Radic Baumgartner Ksenija/Rechnung_20190830.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Radic Baumgartner Ksenija/Rechnung_20190830_Zahlungserinnerung.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Radic Baumgartner Ksenija/Rechnung_20191025.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Radic Baumgartner Ksenija/Rechnung_20191113.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Radic Baumgartner Ksenija/Rechnung_20200205.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Radic Baumgartner Ksenija/Rechnung_20200501.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Ruggieri Canins Joan/Rechnung_200621.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Ruoss Giulia/Rechnung_200703.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Rüede Emilie/Rechnung_200314.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Saunders Lucia/Rechnung_200923.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Schuck Flavia/Rechnung_20200228.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Sheta Liam/Rechnung_20200131.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Sheta Liam/Rechnung_20200327.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Sheta Liam/Rechnung_20200407_Herr Sheta.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Sheta Liam/Rechnung_20200416.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Sheta Liam/Rechnung_20200529.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Sheta Liam/Rechnung_20200626.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Sheta Liam/Rechnung_20200925.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Slutzkin Shayna/Rechnung_200317.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Speck Charlotte/Rechnung mit Tarifziffern_20200626.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Speck Charlotte/Rechnung mit Tarifziffern_20200924.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Speck Charlotte/Rechnung_20190530 - Kopie.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Speck Charlotte/Rechnung_20190530.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Speck Charlotte/Rechnung_20191220.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Säuberli Helena/Rechnung_2000605.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Säuberli Helena/Rechnung_200306.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Viehweg Lina/Rechnung_20200717.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Webb Frances/Rechnung_200605.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Weinhardt Victoria/Rechnung_200321.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Weinhardt Victoria/Rechnung_200529.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Weinhardt Victoria/Rechnung_200703.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20200424.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20191115.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20191218.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20200131.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20200131_MW.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20200328.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20200530.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20200627.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20200731.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20200828.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Millo/Rechnung_20200926.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Nina/Rechnung_20200627.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Nina/Rechnung_20200731.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Nina/Rechnung_20200828.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Wirahediraska Nina/Rechnung_20200926.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Zentraf Theo/Rechnung_20191213.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Zentraf Theo/Rechnung_20200205.docx' >> 2020_Klienten.txt
docx2txt < '/media/zamofing_t/DataHD/Praxis/Klienten/2020_Klienten/Zollinger Alessandra/Rechnung_200308.docx' >> 2020_Klienten.txt
'''


fh=open('2020_Klienten.txt','r')
db=list() #database

def read_klient():
  while True:
    l=fh.readline()
    if l=='': return None
    if l.find('monika.kast-perry@psychologie.ch')>=0:
      break

  rchAdr=list()
  while True:
    l=fh.readline()[:-1]
    if l.startswith('Zürich,'):
      try:
        rchDat=l.split(', ',1)[1]
      except BaseException as e:
        print(e)
        rchDat=''
      break
    if len(l)>0:
      rchAdr.append(l)

  while True:
    l=fh.readline()[:-1]
    if l.find('geb:')>=0:
      klient,geb=l.split('geb:')
      geb=geb.strip()
      if geb.find('AHV-Nr.')>=0:
        geb,AHVNr=geb.split('AHV-Nr.')
        geb=geb.split(', ',1)[0]
      else:
        AHVNr=''

      klient=klient.strip(', ')
      klNa,klVo=klient.rsplit(' ',1)
      break

  beh=list()
  while True:
    l=fh.readline()[:-1]
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
      Vorname=''

    Adresse=rchAdr[-2]
    PLZ_Ort=rchAdr[-1]
    Addrzusatz=rchAdr[2:-2]
    Adresse1=Adresse2=''
    try:
      Adresse1=Addrzusatz[0]
    except IndexError as e:
      pass
    try:
      Adresse2=Addrzusatz[1]
    except IndexError as e:
      pass


  try:
      PLZ,Ort=PLZ_Ort.split()
  except ValueError as e:
    print(e,'Error in PLZ_Ort:',PLZ_Ort)
    PLZ=''
    Ort=PLZ_Ort

  #return (rchAdr,(klNa,klVo,geb),beh)
  return ((Anrede,Name,Vorname,Adresse,Adresse1,Adresse2,PLZ,Ort),(klNa,klVo,geb,AHVNr),rchDat,beh)

while True:
  try:
    rec=read_klient()
    if rec is None: break
    db.append(rec)
    print(rec[0],rec[1])

  except IOError as e:
    print(e)
#print(db)

lutKlient=dict() #database klienten
dbKlient=list() #database klienten
dbRch=list() #database Behandlungen
dbBeh=list() #database Behandlungen

def split_behandlung(behRaw):
  beh=list()
  #tarif preis pro 60 min
  #zeit in minuten
  #datum,tarif,zeit,Bemerkung,tarZif
  if tuple(map(lambda x : x.strip(' :'),behRaw[0].split('\t')))==('Daten', 'Minuten / Ansatz pro h', 'Kosten', 'Total') or \
     tuple(map(lambda x:x.strip(' :'),behRaw[0].split('\t')))==('Daten','Minuten / Ansatz','Kosten','Total'):
      print('format 1')
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
        beh.append((rs[0],float(t),float(z),'',''))

  elif tuple(map(lambda x:x.strip(' :'),behRaw[0:4]))==('Datum','Inhalt','Minuten','Betrag') or \
       tuple(map(lambda x:x.strip(' :'),behRaw[0:4]))==('Datum','Inhalt','Zeit','Kosten') or \
       tuple(map(lambda x:x.strip(' :'),behRaw[0:4]))==('Datum','Inhalt','Zeit','Betrag'):
      print('format 2')
      n=(len(behRaw)-4-3)//4
      if (len(behRaw)!=n*4+4+3):
        n=(len(behRaw)-4)//4
        print('wrong counts!',len(behRaw),behRaw)
      if behRaw[-2].find('Total')<0:
        print('missing Total!',behRaw[-4:])
      for i in range(n):
        r=behRaw[4+4*i:8+4*i]
        #datum,tarif,zeit,Bemerkung,tarZif
        d=r[0]
        b=r[1]
        z=r[2].replace('min','')
        t=60*float(r[3].replace('CHF','').strip())/float(z)
        beh.append((d,t,float(z),b,''))

  elif tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Minuten','Betrag') or \
      tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Zeit in Min','Kosten') or \
      tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Zeit in Min','Betrag') or \
      tuple(map(lambda x:x.strip(' :'),behRaw[0:6]))==('Datum','Tarif','Tarifziffer','Inhalt','Zeit','Kosten'):
      print('format 3')
      n=(len(behRaw)-6-5)//6
      if len(behRaw)!=n*6+6+5:
        n=(len(behRaw)-6)//6
        print('wrong counts!',len(behRaw),behRaw)
        #assert(len(behRaw)==n*6+6+5)
      if behRaw[-2].find('Total')<0:
        print('missing Total!',behRaw[-6:])
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
      print('format 4')
      n=(len(behRaw)-6-5)//6
      if len(behRaw)!=n*6+6+5:
        n=(len(behRaw)-6)//6
        print('wrong counts!',len(behRaw),behRaw)
        #assert(len(behRaw)==n*6+6+5)
      if behRaw[-2].find('Total')<0:
        print('missing Total!',behRaw[-6:])
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
    print(behRaw[:6])
    raise ValueError('Unknown Format')

  return beh

def rawdb2relational():
  idNewKlient=0
  idBeh=0
  idRch=0
  for (rchAddr,client,rchDat,beh) in db:
    keyKlient='\t'.join(client[:3])
    try:
      idKlient=lutKlient[keyKlient]
    except KeyError:
      idKlient=idNewKlient
      lutKlient[keyKlient]=idKlient
      dbKlient.append((idKlient,)+rchAddr+client)
      idNewKlient+=1
    print(keyKlient,idKlient)
    dbRch.append((idRch,idKlient,rchDat))

    #### analyze behandlung
    beh=split_behandlung(beh)
    for rec in beh:
      dbBeh.append((idRch,idKlient,)+rec)
    idRch+=1


rawdb2relational()
#print(dbBeh)
#print(lutKlient)
#print(dbKlient)
#print(dbRch)
#print(dbBeh)
fh.close()
print('read data done.')

fh=open('2020_Klienten.sql','w')
#fh.write('INSERT INTO tblPerson (IDPerson,Anrede,Nachname,Vorname,Adresse,PLZ,Ort,Mobile,Telefon,eMail,Bemerkung) VALUES')
fh.write('INSERT INTO tblPerson (pkPerson,RngAnrede,RngNachname,RngVorname,RngAdresse,RngAdresse1,RngAdresse2,PLZ,Ort,Nachname,Vorname,datGeb,AHVNr) VALUES\n')
fh.write(',\n'.join(map(str,dbKlient)))
fh.write(';\n\n\n')

fh.write('INSERT INTO tblRechnung (pkRechnung,fkPerson,datRechnung) VALUES')
fh.write(',\n'.join(map(str,dbRch)))
fh.write(';\n\n\n')

fh.write('INSERT INTO tblBehandlung (fkRechnung,fkPerson,datBehandlung,Stundenansatz,Dauer,Bemerkung,TarZif) VALUES ')
fh.write(',\n'.join(map(str,dbBeh)))
fh.write(';\n\n\n')


fh.close()

print('write sql file done.')
