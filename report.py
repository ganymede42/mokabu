#!/usr/bin/python3
import time
#import reportlab as rl
import reportlab.lib as rll
import reportlab.platypus as rlp
import reportlab.lib.units as rlu
import reportlab.lib.styles as rls
import reportlab.platypus as rlp
import reportlab.lib.enums as rle
import reportlab.lib.pagesizes as rlps

#from reportlab.lib.enums import TA_JUSTIFY
#from reportlab.lib.pagesizes import letter
#from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
#from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#from reportlab.lib.units import inch
class Invoice():
  def init(self,fn='invoice.pdf'):
    styles=rls.getSampleStyleSheet()
    styles.add(rls.ParagraphStyle(name='Justify', alignment=rle.TA_JUSTIFY))
    styles.add(rls.ParagraphStyle(name='Right', alignment=rle.TA_RIGHT))
    styles.add(rls.ParagraphStyle(name='Center', alignment=rle.TA_CENTER))

    doc = rlp.SimpleDocTemplate(fn,pagesize=rlps.A4,
                            rightMargin=72,leftMargin=72,
                            topMargin=22,bottomMargin=18)
    Story=[]
    im = rlp.Image("Logo_Monika.png", 8*rlu.cm, 4*rlu.cm)
    im.hAlign='RIGHT'
    Story.append(im)
    txt='''<font size="7"><b>Monika Kast Perry</b><br/>
Dr. phil., Fachpsychologin<br/>
für Kinder- & Jugendpsychologie FSP<br/>
eidg. anerkannte Psychotherapeutin.<br/>
Albisstrasse 11 · 8038 Zürich · +41 76 335 72 79<br/>
monika.kast-perry@psychologie.ch · praxis-weiterkommen.com</font>'''
    Story.append(rlp.Paragraph(txt,styles["Right"]))


    txt='''
Familie<br/>
Cunte Cristine & Fonte Miguel<br/>
Binzacherweg 20<br/>
8166 Niderweningen'''
    Story.append(rlp.Spacer(1, 36))
    Story.append(rlp.Paragraph(txt,styles["Normal"]))
    txt='''
Zürich, 25.01.2020'''
    Story.append(rlp.Spacer(1, 36))
    Story.append(rlp.Paragraph(txt,styles["Normal"]))
    txt='''Rechnung für<br/>
<br/>
<b>Cunte Rui, geb: 26.03.2013</b>'''
    Story.append(rlp.Paragraph(txt,styles["Normal"]))

    Story.append(rlp.Spacer(1, 12))
    data=[['00','01','02','03','04'],
     ['10','11','12','13','14'],
     ['20','21','22','23','24'],
     ['30','31','32','33','34']]
    t=rlp.Table(data)
    t.setStyle(rlp.TableStyle([('BACKGROUND',(1,1),(-2,-2),rll.colors.green),
                           ('TEXTCOLOR',(0,0),(1,-1),rll.colors.red)]))
    Story.append(t)

    txt='''
    Daten: 	Minuten / Ansatz pro h: 	Kosten:	Total:<br/>
17.01.2020	60 min / 180.00 SFr.	SFr. 180.00	SFr. 180.00'''
    Story.append(rlp.Spacer(1, 12))
    Story.append(rlp.Paragraph(txt,styles["Normal"]))
    txt='''Ich bitte Sie, den Betrag von SFr. 180.00 auf folgendes Konto zu überweisen:<br/>
St. Galler Kantonalbank, IBAN-Nr. CH60 0078 1622 4188 6200 0<br/>
<br/>
Monika Kast Perry<br/>
Praxis weiterkommen<br/>
Albisstrasse 11<br/>
8038 Zürich'''
    Story.append(rlp.Spacer(1, 12))
    Story.append(rlp.Paragraph(txt,styles["Normal"]))
    txt='''Herzlichen Dank und liebe Grüsse'''
    Story.append(rlp.Spacer(1, 12))
    Story.append(rlp.Paragraph(txt,styles["Normal"]))
    Story.append(rlp.Spacer(1, 12))
    im = rlp.Image("signature.png", 8*rlu.cm, 2*rlu.cm)
    im.hAlign='CENTER'
    Story.append(im)
    txt='''Monika Kast Perry'''
    Story.append(rlp.Paragraph(txt,styles["Center"]))
    txt='PS: Es kann über die Zusatzversicherung Ihrer Krankenkasse abgerechnet werden.'
    doc.build(Story)


  def add(self,row):
    pass

  def finalize(self):
    pass


if __name__ == '__main__':
  rep=Invoice()
  rep.init()
  rep.finalize()
