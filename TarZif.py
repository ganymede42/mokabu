#https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.psychologie.ch%2Fsites%2Fdefault%2Ffiles%2F2022-06%2F20220602_psytarif_einfuehrungsversion_tarifstruktur_de.xlsx&wdOrigin=BROWSELINK
import logging
_log=logging.getLogger(__name__)

lutLstErb={
  'MK_A': {
    'vorname': 'Monika',
    'name': 'Kast Perry',
    'email': 'monika.kast-perry@psychologie.ch',
    'telM': '+41 76 335 72 79',
    'adr': 'Weihermattstrasse 11a',
    'plz':'5242',
    'ort': 'Birr',
    'qrFmt':'SPC\n0200\n1\nCH6000781622418862000\nS\nPraxis Weiterkommen Monika Kast Perry\nWeihermattstrasse 11a\n\n5242\nBirr\nCH\n\n\n\n\n\n\n\n%.2f\nCHF\n\n\n\n\n\n\n\nNON\n\n%s\nEPD',
    'GLN':7601007566037,
    'UID':'CHE327073453',
    'ZSR':'I989819',
  },
  'MK_Z':{
    'vorname': 'Monika',
    'name': 'Kast Perry',
    'email': 'monika.kast-perry@psychologie.ch',
    'telM': '+41 76 335 72 79',
    'adr': 'Riedthofstrasse 100',
    'plz':'8105',
    'ort': 'Regensdorf',
    'qrFmt':'SPC\n0200\n1\nCH6000781622418862000\nS\nPraxis Weiterkommen Monika Kast Perry\nWeihermattstrasse 11a\n\n5242\nBirr\nCH\n\n\n\n\n\n\n\n%.2f\nCHF\n\n\n\n\n\n\n\nNON\n\n%s\nEPD',
    'GLN':7601007566037,
    'UID': 'CHE327073453',
    'ZSR':'D749131',
  },
  'TA_R':{
    'vorname': 'Tanja',
    'name': 'Rom',
    'email': 'tanja.rom@gmail.com',
    'telM': '+41 76 563 72 72',
    'adr': 'Häringstrasse 20',
    'plz':'8001',
    'ort': 'Zürich',
    'qrFmt':'SPC\n0200\n1\nCH0600700112700738038\nS\nTanja Rom\nHäringstrasse 20\n\n8001\nZürich\nCH\n\n\n\n\n\n\n\n%.2f\nCHF\n\n\n\n\n\n\n\nNON\n\n%s\nEPD',
    'GLN':7601003944099,
    'UID': 'CHE320888520',
    'ZSR':'S633931',
  },
  'CA_M':{
    'vorname': 'Caroline',
    'name': 'Maroni',
    'email': 'caroline.maroni@fsp-hin.ch',
    'telM': '+41 78 660 74 30',
    'adr': 'Dufourstrase 130',
    'plz':'8008',
    'ort': 'Zürich',
    'qrFmt':'SPC\n0200\n1\nCH1680808004966166240\nS\nCaroline Maroni\nDufourstrase 130\n\n8008\nZürich\nCH\n\n\n\n\n\n\n\n%.2f\nCHF\n\n\n\n\n\n\n\nNON\n\n%s\nEPD',
    'GLN':7601003944099,
    'UID': 'CHE462837078',
    'ZSR':'Y871331',
  }
}

rawTxt='''\
PA	"Therapieleistungen in Anwesenheit des Patienten (gemäss Art. 11b Abs. 1 lit. a KLV)"	Regulär angeordnete Psychotherapie. Anordnung von maximal 15 Therapiesitzungen durch Ärzte oder Ärztinnen der Grundversorgung sowie der psychiatrischen und psychosomatischen Versorgung. Für die Weiterführung der Psychotherapie nach kumuliert 30 Sitzungen ist vor Einreichung des Berichts mit einem Vorschlag zur Fortsetzung der Therapie eine Fallbeurteilung durch Fachärzte oder Fachärztinnen mit den Weiterbildungstiteln Psychiatrie und Psychotherapie oder Kinder- und Jugendpsychiatrie und -psychotherapie erforderlich.
PA010	Diagnostik und Therapie mit einem Patienten in Anwesenheit, pro 1 Min.	"Beinhaltet psychologische und psychotherapeutische Diagnostik und Psychotherapie (Begrüssung, Therapie, Verabschiedung). Es gilt ausschliesslich das persönliche, zeitgleiche Gespräch. Abrechenbar ist die Sitzungsdauer mit dem Patienten. Testdiagnostische Leistungen während der Therapie müssen unter der Position PA220 erfasst werden. Testdiagnostische Leistungen bis zu einer Durchführungszeit von 20 Min. werden mit dieser Tarifposition verrechnet. Die Testauswertung wird in der Vor- und Nachbereitung abgerechnet. "
PA011	Diagnostik und Therapie mit einem Patienten in Anwesenheit, fernmündlich, pro 1 Min.	Beinhaltet psychologische und psychotherapeutische Diagnostik und Psychotherapie (Begrüssung, Therapie, Verabschiedung). Es gilt ausschliesslich das fernmündliche, zeitgleiche Gespräch. Abrechenbar ist die Sitzungsdauer mit dem Patienten. Testdiagnostische Leistungen bis zu einer Durchführungszeit von 20 Min. werden mit dieser Tarifposition verrechnet. Die Testauswertung wird in der Vor- und Nachbereitung abgerechnet.
PA020	Diagnostik und Therapie mit einem Paar in Anwesenheit der Patienten, pro 1 Min.	Ein Paar besteht aus zwei zusammengehörenden oder eng verbundenen Menschen. Beinhaltet psychologische und psychotherapeutische Diagnostik und Psychotherapie (Begrüssung, Therapie, Verabschiedung). Es gilt ausschliesslich das persönliche, zeitgleiche Gespräch. Divisormethode - abrechenbar anteilsmässig durch die Anzahl teilnehmender Personen.
PA021	Diagnostik und Therapie mit einem Paar in Anwesenheit der Patienten, fernmündlich, pro 1 Min. 	Ein Paar besteht aus zwei zusammengehörenden oder eng verbundenen Menschen. Beinhaltet psychologische und psychotherapeutische Diagnostik und Psychotherapie (Begrüssung, Therapie, Verabschiedung). Es gilt ausschliesslich das fernmündliche, zeitgleiche Gespräch. Divisormethode - abrechenbar anteilsmässig durch die Anzahl teilnehmender Personen.
PA030	Diagnostik und Therapie mit einer Familie in Anwesenheit des Patienten, pro 1 Min. 	Eine Familie besteht aus mindestens zwei Personen. Beinhaltet psychologische und psychotherapeutische Diagnostik und Psychotherapie (Begrüssung, Therapie, Verabschiedung). Es gilt ausschliesslich das persönliche, zeitgleiche Gespräch. Abrechenbar ist die Sitzungsdauer gegenüber dem Indexpatienten.
PA031	Diagnostik und Therapie mit einer Familie in Anwesenheit des Patienten, fernmündlich, pro 1 Min. 	Eine Familie besteht aus mindestens zwei Personen. Beinhaltet psychologische und psychotherapeutische Diagnostik und Psychotherapie (Begrüssung, Therapie, Verabschiedung). Es gilt ausschliesslich das fernmündliche, zeitgleiche Gespräch. Abrechenbar ist die Sitzungsdauer gegenüber dem Indexpatienten.
PA040	Diagnostik und Therapie mit einer Gruppe in Anwesenheit des Patienten, pro 1 Min. 	Beinhaltet psychologische und psychotherapeutische Diagnostik und Psychotherapie (Begrüssung, Therapie, Verabschiedung). Es gilt ausschliesslich das persönliche, zeitgleiche Gespräch. Gruppen ab drei Personen. Divisormethode - abrechenbar anteilsmässig durch die Anzahl teilnehmender Personen. Durch maximal zwei Psychotherapeuten gleichzeitig abrechenbar. Der zweite Psychotherapeut ist vom fallführenden Psychotherapeuten über die Zuschlagsposition PA042 abzurechnen.
PA041	Diagnostik und Therapie mit einer Gruppe in Anwesenheit der Patienten, fernmündlich, pro 1. Min.	Beinhaltet psychologische und psychotherapeutische Diagnostik und Psychotherapie (Begrüssung, Therapie, Verabschiedung). Es gilt ausschliesslich das fernmündliche, zeitgleiche Gespräch. Gruppen ab drei Personen. Divisormethode - abrechenbar anteilsmässig durch die Anzahl teilnehmender Personen. Durch maximal zwei Psychotherapeuten gleichzeitig abrechenbar. Der zweite Psychotherapeut ist vom fallführenden Psychotherapeuten über die Zuschlagsposition PA042 abzurechnen.
PA042	+ Diagnostik und Therapie mit einer Gruppe in Anwesenheit der Patienten, Co-Therapeut, pro 1. Min., 	Beinhaltet neben der psychologische Diagnostik und/oder Therapie auch Begrüssung, Verabschiedung, Begleitung zu und Übergabe (inklusive Anordnungen) an Hilfspersonal betreffend Administration. Divisormethode - abrechenbar anteilsmässig durch die Anzahl teilnehmender Personen.
PA110	Krisenintervention während der angeordneten Psychotherapie in Anwesenheit des Patienten, pro 1 Min.	"Beinhaltet psychologische und psychotherapeutische Diagnostik und Krisenintervention (Begrüssung, Therapie, Verabschiedung) mit einem Patienten. Es gilt ausschliesslich das persönliche, zeitgleiche Gespräch. Abrechenbar ist die Sitzungsdauer mit dem Patienten. Dient der Behandlung eines unvorhersehbaren psychischen Krisenzustandes im Verlauf der angeordneten Psychotherapie, welcher in Zusammenhang mit einem emotionalen Ereignis oder mit einer Veränderung der Lebensumstände aufgetreten ist. Dieser Krisenzustand wird vom Betroffenen und/oder seinem Umfeld als bedrohlich und/oder überwältigend wahrgenommen und kann von ihm und/oder seinem Umfeld ohne professionelle Hilfe nicht bewältigt werden. Beinhaltet auch Begrüssung, Verabschiedung, Übergabe, Begleitung. Gilt nicht für einen Krisenzustand in einer laufenden Sitzung. "
PA111	Krisenintervention während der angeordneten Psychotherapie in Anwesenheit des Patienten, fernmündlich, pro 1 Min	"Beinhaltet psychologische und psychotherapeutische Diagnostik und Krisenintervention (Begrüssung, Therapie, Verabschiedung) mit einem Patienten. Es gilt ausschliesslich das fernmündliche, zeitgleiche Gespräch. Abrechenbar ist die Sitzungsdauer mit dem Patienten. Dient der Behandlung eines unvorhersehbaren psychischen Krisenzustandes im Verlauf der angeordneten Psychotherapie, welcher in Zusammenhang mit einem emotionalen Ereignis oder mit einer Veränderung der Lebensumstände aufgetreten ist. Dieser Krisenzustand wird vom Betroffenen und/oder seinem Umfeld als bedrohlich und/oder überwältigend wahrgenommen und kann von ihm und/oder seinem Umfeld ohne professionelle Hilfe nicht bewältigt werden. Beinhaltet auch Begrüssung, Verabschiedung, Übergabe, Begleitung. Gilt nicht für einen Krisenzustand in einer laufenden Sitzung. "
PA220	Testdiagnostische Leistungen in Anwesenheit des Patienten, pro 1 Min. 	"Gilt für validierte und standardisierte psychodiagnostische Testverfahren, die der Diagnostik und der Psychotherapie dienen.Abrechenbar ist die Zeit in Anwesenheit des Patienten, in der sich der Psychotherapeut mit dem Patienten befasst. Erfolgt entweder auf Anordnung durch einen Arzt mit Anordnungsberechtigung oder im Verlauf einer ordentlich angeordneten Psychotherapie, wenn eine diagnostische Testabklärung erfolgen muss. Testdiagnostische Leitungen mit einer Durchführungszeit von 20 Min. und weniger werden in den Positionen PA010 und PA011 abgerechnet. "
PA230	Expositionstherapie mit einem Patienten in Anwesenheit, pro 1 Min.	Beinhaltet Expositionstherapien oder Traumaexposition innerhalb oder ausserhalb des Behandlungsraumes. Es gilt ausschliesslich das persönliche, zeitgleiche Gespräch. Abrechenbar ist die Sitzungsdauer mit dem Patienten.
PB	"Therapieleistungen in Anwesenheit des Patienten (gemäss Art. 11b Abs. 1 lit. b KLV)"	Einmalige Anordnung durch alle Ärzte und Ärztinnen von maximal 10 Sitzungen für Leistungen zur Krisenintervention oder Kurztherapien für Patienten und Patientinnen mit schweren neu diagnostizierten Erkrankungen oder einer lebensbedrohlichen Situation. Bei Weiterführung der Psychotherapie, hat diese mit einer regulären Anordnung zu erfolgen.
PB010	Diagnostik und Therapie mit einem Patienten bei Anordnung Krisenintervention/Kurztherapie mit einem Patienten in Anwesenheit, pro 1 Min.	"Durch einen Arzt mit Anordnungsberechtigung angeordnete Krisenintervention oder Kurztherapie bei schweren Erkrankungen bei Neudiagnosen oder lebensbedrohlicher Situation (gemäss Art. 11b lit. b KLV).Beinhaltet psychologische und psychotherapeutische Diagnostik und Krisenintervention (Begrüssung, Therapie, Verabschiedung). Es gilt ausschliesslich das persönliche, zeitgleiche Gespräch. Abrechenbar ist die Sitzungsdauer mit dem Patienten."
PB011	Diagnostik und Therapie mit einem Patienten bei Anordnung Krisenintervention/Kurztherapie mit einem Patienten in Anwesenheit, fernmündlich, pro 1 Min.	"Durch einen Arzt mit Anordnungsberechtigung angeordnete Krisenintervention oder Kurztherapie bei schweren Erkrankungen bei Neudiagnosen oder lebensbedrohlicher Situation (gemäss Art. 11b lit. b KLV).Beinhaltet psychologische und psychotherapeutische Diagnostik und Krisenintervention (Begrüssung, Therapie, Verabschiedung). Es gilt ausschliesslich das fernmündliche, zeitgleiche Gespräch. Abrechenbar ist die Sitzungsdauer mit dem Patienten."
PE	Leistungen in Abwesenheit des Patienten (gelten für Therapieleistungen gemäss Art. 11b Abs.1 lit. a und lit. b KLV)
PE010	Vor- und Nachbereitung der Therapiesitzung, pro 1 Min. 	Beinhaltet auf die Therapie bezogene Vor- und Nachbereitung (Akteneinsicht eigener Einträge, Akteneinträge, Bereitstellen von Therapiematerial, Vorbereitung des Raums). Für Paar- und Gruppentherapien kommt die Divisormethode zu Anwendung - abrechenbar anteilsmässig durch die Anzahl teilnehmender Personen.
PE030	Schriftliche Therapieplanung in Abwesenheit des Patienten, pro 1 Min.	"Therapieplanung, Auswertung von Video- und Tonmaterial, Erstellen eines Genogramms und anderer in der Therapie erstellten Tools, Verhaltenstherapieplanung, schriftliche Auswertung von in Therapiesitzungen erstelltem Material. Das Ergebnis der Planung und/oder Auswertung ist schriftlich festzuhalten. Die schriftliche Therapieplanung ist nicht abrechenbar für die übliche Vor- und Nachbereitung einer Therapiesitzung."
PE020	Auswertungen, Interpretationen und Bericht testdiagnostischer Leistungen in Abwesenheit des Patienten, pro 1 Min.	Dokumentierte Auswertung und Interpretation psychodiagnostischer Verfahren. Die Interpretation ist schriftlich festzuhalten. Einschliesslich Bericht. Kann nur im Zusammenhang mit der Position PA220 abgerechnet werden. Die Auswertung, die Interpretation und der Bericht kann an mehreren Tagen erfolgen.
PE040	Aktenstudium von Fremdakten in Abwesenheit des Patienten, bei Patienten ab 18 Jahren, pro 1 Min.	Studium von Fremdakten in Abwesenheit des Patienten. Als Aktenstudium gilt das patientenbezogene Studium von Fremdakten (Lesen und Beurteilen ausführlicher fremder Akten und Akten des anordnenden Arztes, inkl. Studium dort zitierter Literaturstellen). Eine Verrechnung der Leistung in Abwesenheit des Patienten zur Einsicht in eigenes Dossier ist nicht zulässig.
PE045	Aktenstudium von Fremdakten in Abwesenheit des Patienten, bei Patienten unter 18 Jahren, pro 1 Min.	Studium von Fremdakten in Abwesenheit des Patienten. Als Aktenstudium gilt das patientenbezogene Studium von Fremdakten (Lesen und Beurteilen ausführlicher fremder Akten und Akten des anordnenden Arztes, inkl. Studium dort zitierter Literaturstellen). Eine Verrechnung der Leistung in Abwesenheit des Patienten zur Einsicht in eigenes Dossier ist nicht zulässig.
PK	Koordinationsleitungen in Abwesenheit (gelten für Therapieleistungen gemäss Art. 11b Abs.1 lit. a und lit. b KLV)
PK010	Informationsaustausch und Koordination mit Ärzten und Psychologen in Abwesenheit des Patienten, bei Patienten ab 18 Jahren, pro 1 Min.	"Gilt für den patientenbezogenen Informationsaustausch wie Besprechung und Beratung zwischen den in die psychotherapeutische Behandlung des Patienten involvierte Ärzte/Psychologen und dem ausführenden psychologischen Psychotherapeuten, in Abwesenheit des Patienten.Gilt nicht für regelmässige Rapporte im Spital und Organisationen der psychologischen Psychotherapie."
PK015	Informationsaustausch und Koordination mit Ärzten und Psychologen in Abwesenheit des Patienten, bei Patienten unter 18 Jahren, pro 1 Min.	"Gilt für den patientenbezogenen Informationsaustausch wie Besprechung und Beratung zwischen den in die psychotherapeutische Behandlung des Patienten involvierte Ärzte/Psychologen und dem ausführenden psychologischen Psychotherapeuten, in Abwesenheit des Patienten.  Gilt nicht für regelmässige Rapporte im Spital und Organisationen der psychologischen Psychotherapie."
PK020	Koordination und Abklärung mit Dritten in Abwesenheit des Patienten, bei Patienten ab18 Jahren, pro 1 Min. 	Vom Psychotherapeuten geführte therapiebezogene Koordination und Abklärungen mit anderen Anspruchsgruppen (Angehörige, Sozialarbeiter, Bezugspersonen, Heilpädagogen, Arbeitgeber, Schule), die massgebend für den Patienten und dessen Therapie sind. Auskünfte, Abklärungen, Erkundigungen und Beratungen von für die Therapie des Patienten relevanten Personen. Gilt nicht für regelmässige Rapporte im Spital und Organisation der psychologischen Psychotherapie.
PK025	Koordination und Abklärung mit Dritten in Abwesenheit des Patienten bei Patienten unter 18 Jahren, pro 1 Min. 	Vom Psychotherapeuten geführte therapiebezogene Koordination und Abklärungen mit anderen Anspruchsgruppen (Sozialarbeiter, Bezugspersonen, Heilpädagogen, Arbeitgeber, Eltern, Angehörige, Schule), die massgebend für den Patienten und dessen Therapie sind. Auskünfte, Abklärungen, Erkundigungen und Beratungen von für die Therapie des Patienten relevanten Personen. Gilt nicht für regelmässige Rapporte im Spital und Organisation der psychologischen Psychotherapie.
PL	Berichte und Überweisungen in Abwesenheit (gelten für Therapieleistungen gemäss Art. 11b Abs.1 lit. a und lit. b KLV)	Die vom Psychotherapeuten verfassten Berichte, Schreiben (Schriftverkehr zwischen Arzt und psychologischem Psychotherapeut, vom Versicherer verlangte Berichte usw.) müssen medizinisch und/oder administrativ notwendig sein. Allfällige Fristen sind einzuhalten. Diese Dokumente müssen grundsätzlich maschinell oder elektronisch erzeugt werden, d.h. keine handschriftlich verfassten Berichte. Die Vergütung eines Berichtes beinhaltet auch das erstmalige Anfertigen allfälliger Kopien desselben sowie die Zustellung dieser Kopien auf Verlangen des Versicherers.
PL010	Psychotherapeutischer Bericht an den anordnenden und/oder fallbeurteilenden Arzt, bei Patienten ab 18 Jahren, pro 1 Min. 	"Psychotherapeutischer Bericht oder Bericht zur Verlängerung der Psychotherapie an den anordnenden Arzt und/oder an den fallbeurteilenden Arzt, inkl. allfälliger Kopien. Der Bericht ist dem Versicherer resp. dem Vertrauensarzt des Versicherers auf Verlangen zuzustellen. Dabei gelten die Bestimmungen des Datenschutzes. Die erstmalige Zustellung des Berichts auf Verlangen des Versicherers erfolgt kostenlos. "
PL015	Psychotherapeutischer Bericht an den anordnenden und/oder fallbeurteilenden Arzt, bei Patienten unter 18 Jahre, pro 1 Min. 	"Psychotherapeutischer Bericht oder Bericht zur Verlängerung der Psychotherapie an den anordnenden Arzt und/oder an den fallbeurteilenden Arzt, inkl. allfälliger Kopien. Der Bericht ist dem Versicherer resp. dem Vertrauensarzt des Versicherers auf Verlangen zuzustellen. Dabei gelten die Bestimmungen des Datenschutzes. Die erstmalige Zustellung des Berichts auf Verlangen des Versicherers erfolgt kostenlos. "
PL020	Psychotherapeutischer Bericht, bei Patienten ab 18 Jahren, pro 1 Min. 	"Psychotherapeutischer Bericht für den Schriftverkehr unter Dritten (Kliniken, ambulante Institutionen, Ärzte, Psychologen u.a.) betreffend Befund, Diagnose, Therapien, Prognose über den Heilungsverlauf und weitere Massnahmen den Patient betreffend. Gilt für das Verfassen von Berichten, sofern nicht anderweitig entschädigt. Gilt nicht für interne Verlaufsberichte und Schriftverkehr innerhalb des Spitals und Organisation der psychologischen Psychotherapie."
PL025	Psychotherapeutischer Bericht, bei Patienten unter 18 Jahre, pro 1 Min.	"Psychotherapeutischer Bericht für den Schriftverkehr unter Dritten (Kliniken, ambulante Institutionen, Ärzte, Psychologen u.a.) betreffend Befund, Diagnose, Therapien, Prognose über den Heilungsverlauf und weitere Massnahmen den Patient betreffend. Gilt für das Verfassen von Berichten, sofern nicht anderweitig entschädigt. Gilt nicht für interne Verlaufsberichte und Schriftverkehr innerhalb des Spitals und Organisation der psychologischen Psychotherapie. "
PN	Notfall (gelten für Therapieleistungen gemäss Art. 11b Abs.1 lit. a und lit. b KLV)
PN010	Administrativer Notfallaufwand, im Zeitraum 07:00-19:00 Uhr wochentags	"Gilt für Behandlung wochentags im Zeitraum 07:00-19:00 Uhr, die wegen eines Notfalls verlangt und durchgeführt werden müssen - psychotherapeutisch notwendig sind und vom Patienten, Angehörigen oder Dritten als notwendig erachtet werden. Dabei kann es sich um eine plötzlich entstandene Krise, eine Selbst- oder eine Fremdgefährdung oder eine Dekompensation des Patienten handeln. Der Psychotherapeut befasst sich unverzüglich nach Kenntnisnahme des Notfalls mit dem Patienten. Es wird ein direkter und unmittelbarer Therapeut-Patient-Kontakt vorausgesetzt, unabhängig von der Örtlichkeit. Die Konsultation kann auch fernmündlich erfolgen. Die Leistung beginnt mit der Kenntnisnahme des Notfalls und endet mit dem Abschluss der administrativen Tätigkeiten (Kontaktaufnahme mit abzusagenden Patienten, Organisation des Betriebs). Die Behandlung von ordentlich angemeldeten Patienten gilt nicht als Notfall, auch wenn sie in diesem Zeitraum erfolgt. Die Behandlung von nicht angemeldeten Patienten gilt nicht generell als Notfall und berechtigt nicht generell zur Verrechnung des Notfallzuschlags."
PN020	Notfallzuschlag 20%, Freitag 19:00 Uhr bis Montag 07:00 Uhr, wochentags 19:00 Uhr bis 07:00 Uhr und an gesetzlichen Feiertagen, prozentual	"Zuschlag zu Therapie oder Diagnostik im Notfall an Wochenenden (Freitag 19:00 Uhr bis Montag 07:00 Uhr) und Feiertagen sowie 19:00 bis 07:00 Uhr. Gilt für Behandlung, psychotherapeutisch notwendig und vom Patienten, Angehörigen oder Dritten als notwendig erachtet. Dabei kann es sich um eine plötzlich entstandene Krise, eine Selbst- oder eine Fremdgefährdung oder eine Dekompensation des Patienten handeln. Der Psychotherapeut befasst sich unverzüglich nach Kenntnisnahme des Notfalls mit dem Patienten. Es wird ein direkter und unmittelbarer Therapeut-Patient-Kontakt vorausgesetzt, unabhängig von der Örtlichkeit. Die Konsultation kann auch fernmündlich erfolgen. Die Behandlung von ordentlich angemeldeten Patienten gilt nicht als Notfall, auch wenn sie in diesem Zeitraum erfolgen. Behandlung von nicht angemeldeten Patienten gilt nicht generell als Notfall und berechtigt nicht generell zur Verrechnung des Notfallzuschlags."
PW	Weg und Material (gelten für Therapieleistungen gemäss Art. 11b Abs.1 lit. a und lit. b KLV)
PW010	Wegentschädigung beim Patientenkontakt ausserhalb der Behandlungsräume, pro 1 Min. 	Effektive Wegzeit (An- und Rückreise). Bei einem vergeblichen Aufsuchen kann die Wegzeit abgerechnet werden, sofern eine nachweisbare therapeutische Indikation zur Abwesenheit des Patienten führte. Beim Aufsuchen von mehreren Patienten in der gleichen Tour kann nur der Ortswechsel abgerechnet werden. Wegzeiten dürfen nur abgerechnet werden, wenn die Situation, das Befinden und/oder das Störungsbild des Patienten die Behandlung ausserhalb der Behandlungsräumlichkeiten erfordert. Durch Psychologische Psychotherapeuten oder Organisationen der psychologischen Psychotherapeuten, die ausschliesslich aufsuchend tätig sind, nicht abrechenbar.
PW020	Für die Therapie und Diagnostik benötigtes zusätzliches Testmaterial, CHF	Verbrauchsmaterial ist separat zu erfassen, sofern der Einkaufspreis pro Einzelstück grösser Fr. 20.-. Für die Therapie und Diagnostik benötigtes, für den Patienten spezifisch eingekauftes Testmaterial zum einmaligen Gebrauch - Beispielsweise Testbögen, Onlinetestungen und -auswertungen.\
'''

class Lut:
  def __init__(self):
    pass

  def open(self, krzLstErb=None):
    self._lutTarZif=lut=dict()
    self._lutLstErb=lutLstErb
    if krzLstErb is not None:
      self._krzLstErb=krzLstErb

    for ln in rawTxt.split('\n'):
      el=ln.split('\t')
      if not el[0]:
        _log.warning(f'ignore{el}')
        continue
      lut[el[0]]=(2.58,)+tuple(el[1:])

  def tar_zif(self,tz):
    return self._lutTarZif[tz]

  def lst_erb(self,lstErb):
    return self._lutLstErb[lstErb]

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(module)s:%(lineno)d:%(funcName)s:%(message)s ')
  tz=Lut()
  pass
