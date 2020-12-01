kleines Handbuch
================
```
!!! Warnung Software ist in einem Alpha-Teststadium !!!
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


Die Art wie eine Rechnung ausgedruckt wird, kann mit <tplInvoice veränder werden.
Es ist ein 'Bitfeld und ist eine Summe folgender Zahlen:
 0: nichts spezielles
+1: Zahlungserinnerung
+2: 2. Mahnung
+4: Rechnung für IV
+8: QR-Code

-> 4+8=12 -> IV-Rechnung mit QR-Code
default is 4.
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
- Löschen von Rechnungen -> die dazugehörenden Behandlungen müssen 'entkoppelt werden' (fkInvoice=NULL)
- Entfernen von Behandlungen aus Rechnungen
- Hinzufügen von Behandlungen in Rechnungen
- Einfügen von Behandlungen in Rechnungen (nicht nur auto-assistant)
- Tabelle der nicht verrechneten Behandlungen (Invoice mit id=-1)
- Button (checkbox) um Behandlung zu 'nicht verrechnet' hinzufügn/entfernen
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
- Bein 'assisted invoice' und einzelne Invoice Generierung wird die Rechnung unter invoice/Rng<NameVornameDatum>.pdf gespeichert.

```
current:

class WndPerson(WndSqlBase):
  def __init__(self,title):

class WndTreatment(WndSqlBase):
  def __init__(self,sqlFilter=None,title,fkPerson=None):

class WndInvoice(WndSqlBase):
  def __init__(self,sqlFilter=None,title,fkPerson=None):


new:

class WndPerson(WndSqlBase):
  def __init__(self,title,sqlCombo=None,pkPerson=None):
  have a function populate(sqlCombo,pkPerson)
  -> pobupate combobox and selects/displays the record pkPerson
  ->if sqlCombo=None use: > SELECT id, lstName||" "||fstName FROM Person ORDER BY lstName,fstName'

class WndTreatment(WndSqlBase):
  def __init__(self,sqlCombo=None,title,fkPerson=None,pkTreatment=None):
  have a function populate(sqlCombo,pkPerson,pkTreatment)
  -> pobupate combobox and selects/displays the record pkTreatment
  ->if sqlCombo=None use: > filter combobox on fkPerson


class WndInvoice(WndSqlBase):
  def __init__(self,sqlCombo=None,title,fkPerson=None):





