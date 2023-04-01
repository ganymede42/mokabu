kleines Handbuch
================
```
!!! Warnung Software ist in einem Alpha-Teststadium !!!
Direkter link des letzen status:
https://github.com/ganymede42/mokabu/archive/refs/heads/master.zip
```

Personen verwalten,Akteneinträge,Rechnungen, Verlauf drucken
------------------------------------------------------------
```
Menu Edit->Person
-----------------
Im Feld <Suche>, kann der Anfang der Person eingegeben werden, und so einfach ausgewählt werden

!Beim Verändern der Daten muss <Save> gedrückt werden, sonst gehen die Änderungen gleich verloren!
!Das Format des Datums muss yyyy-mm-dd sein. also z.B. 1970-11-25

Button Treatment -> öffnet die Behandlungen der aktuellen Person
Button Invoice   -> öffnet die Rechnungen der aktuellen Person
Button Report Treatment -> gesammter Therapieverlauf der aktuellen Person -> therapy_progress.pdf


Die Art wie eine Rechnung ausgedruckt wird, kann mit tplInvoice veränder werden.
Es ist ein 'Bitfeld und ist eine Summe folgender Zahlen:

0: Normal
+1: 1. Mahnung
+2: 2. Mahnung

 0 : nichts spezielles
+1 : Zahlungserinnerung
+2 : 2. Mahnung

+8 : QR-Code

+16*0: Normal
+16*1: IV mit Tarifziffer
+16*2: Offizielles Format mit Tarifziffer etc. für Monika Kast
+16*3: Offizielles Format mit Tarifziffer etc. (allgemein)

z.B. 
  8+16=12 -> IV-Rechnung mit QR-Code
  8+32=40 -> Offizielles Format mit Tarifziffer etc. für Monika Kast mit QR-Code
  8+48=56 -> Offizielles Format mit Tarifziffer etc. (allgemein) mit QR-Code

default is 0x28(=40) for Monika and 0x38(=56) as default
```

Erstellen neuer Rechnungen
--------------------------
```
Menu Edit->New Assisted Invoices
Erstellen neuer Rechnungen. Es werden alle noch nicht verrechneten Behandlungen angezeigt.
Doppelclick auf einem Eintrag erstellt für alle 'offenen' Behandlungen dieser Person eine neue Rechnung.
```

Bezahlung überprüfen
--------------------
```
Menu Edit->Sync Invoice->Account
Gleicht das Bankkonto mit den erstellten Rechnungen ab. Clicken in linker und rechter Tabelle. Doppelclick verknüpft/entkoppelt die zwei angewählten Einträge. Grün markiert sind die gelinkten Einträge.

Als Datenquelle der rechten Tabelle dient ein CSV-File der Bank.
Zur Zeit kann es noch nicht per Userinterface erneuert werden.
die Funktionalität ist aber vorbeteitet.
mkb.sync_invoice() ./mokabu.py -m4
-> dies liest das File Kontoauszug_2020_10_09.csv ein. Dabei sollten alte Einträge nicht verändert werden sonder nur ergänzt.
```

Gesammtberichte
---------------
```
Über Menu Report->Invoices/Therapy Progress können Dokumente aller Rechnungen und Akteneinträge erzeugt werden.
```


!!! Wichtig !!!
---------------
```
- Die nicht erwähnten Menupunkte sollten !NICHT! werwendet werden. Sie sind für die Entwicklung und Tests gedacht, und können die Datenbank beschädigen!
```

TODO:
-----
```
- bei 'InvoiceAcountSync': Popup menu und öffnen dazugehörenden records in child windows öffnen. Besseres handling
- logging von Datenbank Aktionen
- Bessere GUI Darstellung und resizing Verhalten der Formulare
```

Bugs:
-----
```
```


DONE IN THIS COMMIT
-----
```
- Report Rechnung: 'Bemerkungsfeld' standartmässig auch drauf
- combobox unten in Treatment entfernen
- NOT NULL gewisser Einträge in der Datenbank:
  Person->(anrede,lstName,fstName) Invoice->(dtInvoice) Treatment->(dtTreatment,comment)
  -> use sqlitebrowser for this.

- Bein 'assisted invoice' und einzelne Invoice Generierung wird die Rechnung unter invoice/Rng<NameVornameDatum>.pdf gespeichert.
- Löschen von Rechnungen -> die dazugehörenden Behandlungen müssen 'entkoppelt werden' (fkInvoice=NULL)
- Entfernen von Behandlungen aus Rechnungen
- Hinzufügen von Behandlungen in Rechnungen
- Einfügen von Behandlungen in Rechnungen (nicht nur auto-assistant)
- Tabelle der nicht verrechneten Behandlungen (Invoice mit id=-1)
- Button (checkbox) um Behandlung zu 'nicht verrechnet' hinzufügn/entfernen
```

Deploy
------
```
rm /tmp/mokabu.zip; zip /tmp/mokabu.zip *.py  mokabu.db
unzip -l /tmp/mokabu.zip

cd C:\Users\monik\Documents\Praxis\Mokabu\
git fetch github_https master
git reset github_https/master --hard
```

SCRATCH
-------
```
remove file complitly from history:
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch path_to_file" HEAD
git subtree split

git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch  mokabu.db cleanupKlienten2020.txt populate.sql" HEAD

git filter-branch --prune-empty --index-filter "git rm --cached --ignore-unmatch $(git ls-files | git ls-files | grep -v -e mokabu.db -e cleanupKlienten2020.txt -e populate.sql)"

git filter-repo  --invert-paths --path cleanupKlienten2020.txt mokabu.db populate.sql

mkdir /tmp/Mokabu
git -C /tmp/Mokabu init
git filter-repo --path cleanupKlienten2020.txt --path mokabu.db --path populate.sql --invert-paths --source ~/Documents/prj/Mokabu --target /tmp/Mokabu
git -C /tmp/Mokabu replace -d `git -C /tmp/Mokabu replace`

mkdir /tmp/Mokabu/data
git -C /tmp/Mokabu/data init
git filter-repo --path cleanupKlienten2020.txt --path mokabu.db --path populate.sql --replace-refs delete-no-add --source ~/Documents/prj/Mokabu --target /tmp/Mokabu/data
git -C /tmp/Mokabu/data replace -d `git -C /tmp/Mokabu/data replace`
```

Strukturumbau (31.3.23)
-----------------------
```

lstName

ivcAddress -> ivcAddress||COALESCE('|'||ivcAddress1,'')||COALESCE('|'||ivcAddress2,''),
ivcZipCode -> zipCode
ivcCity -> city
cltLstName -> lstName
cltFstName -> fstName
cltAhvNr -> ahvNr
cltDtBirth -> dtBirth

sed -r -i \
  -e 's/\bzipCode\b/ivcZipCode/g' \
  -e 's/\bcity\b/ivcCity/g' \
  -e 's/\blstName\b/cltLstName/g' \
  -e 's/\bfstName\b/cltFstName/g' \
  -e 's/\bahvNr\b/cltAhvNr/g' \
  -e 's/\bdtBirth\b/cltDtBirth/g' \
   *.py

