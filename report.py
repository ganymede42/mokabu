#!/usr/bin/python3
import time
import reportlab as rl
import reportlab.lib as rll
import reportlab.platypus as rlp
import reportlab.lib.units as rlu
import reportlab.lib.styles as rls
import reportlab.platypus as rlp
import reportlab.lib.enums as rle
import reportlab.lib.pagesizes as rlps
import reportlab.pdfgen as rlpg
import reportlab.pdfbase as rlpb
import reportlab.pdfbase.ttfonts #else not visible

#from reportlab.lib.enums import TA_JUSTIFY
#from reportlab.lib.pagesizes import letter
#from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
#from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#from reportlab.lib.units import inch
class MyDocTemplate(rlp.SimpleDocTemplate):
  def __init__(self,fn,**kw):
    rlp.SimpleDocTemplate.__init__(self,fn,**kw)

  def beforeDocument(self):
    canvas=self.canv

class Invoice():
  def init(self,fn='invoice.pdf'):
    #dimension by default 1/72 inch
    self.canvas=canvas=rlpg.canvas.Canvas(fn,pagesize=rlps.A4)
    self.styles=styles=rls.getSampleStyleSheet()
    styles.add(rls.ParagraphStyle(name='Justify', alignment=rle.TA_JUSTIFY))
    styles.add(rls.ParagraphStyle(name='Right', alignment=rle.TA_RIGHT))
    styles.add(rls.ParagraphStyle(name='Center', alignment=rle.TA_CENTER))

    pass


  def add(self,klient,datRng,behandlungen):
    canvas=self.canvas
    styles=self.styles
    sz=rlps.A4
    l=.8*rlu.cm;
    r=sz[0]-.8*rlu.cm;
    t=sz[1]-.8*rlu.cm;
    b=.8*rlu.cm
    canvas.setLineWidth(.3)
    canvas.line(l,t,r,t)
    canvas.line(l,b,r,b)
    frm=rlp.Frame(l,b,r-l,t-b,showBoundary=1)

    #canvas.setLineWidth(.3)
    #canvas.line(1*rlu.cm,760,20*rlu.cm,760)
    #canvas.line(10,747,580,747)
    #canvas.setFont('Helvetica',12)
    #canvas.drawString(30,800,'1OFFICIAL COMMUNIQUE')
    #rlpb.pdfmetrics.registerFont(rlpb.ttfonts.TTFont('Vera', 'Vera.ttf'))
    #canvas.setFont('Vera',10)
    #canvas.drawString(30,780,'2OFFICIAL COMMUNIQUE')
    #canvas.showPage() #new drawing on new page
    #canvas.drawString(30,780,'3OFFICIAL COMMUNIQUE')
    #canvas.save()

    #doc = rlp.SimpleDocTemplate(fn,pagesize=rlps.A4,
    story=[]
    im=rlp.Image("Logo_Monika.png",7*rlu.cm,2*rlu.cm)
    im.hAlign='RIGHT'
    story.append(im)
    story.append(rlp.Spacer(1,12))
    txt='''<font size="7"><b>Monika Kast Perry</b><br/>
    Dr. phil., Fachpsychologin<br/>
    für Kinder- & Jugendpsychologie FSP<br/>
    eidg. anerkannte Psychotherapeutin.<br/>
    Albisstrasse 11 · 8038 Zürich · +41 76 335 72 79<br/>
    monika.kast-perry@psychologie.ch · praxis-weiterkommen.com</font>'''
    story.append(rlp.Paragraph(txt,styles["Right"]))

    txt='''
    %s<br/>
    %s %s<br/>'''%klient[0:3]
    for i in range(3,6):
      adr=klient[i]
      if len(adr)>0:
        txt+=adr+'<br/>'
    txt+='%s %s<br/>'''%klient[6:8]

    story.append(rlp.Spacer(1,36))
    story.append(rlp.Paragraph(txt,styles["Normal"]))
    txt='Zürich, %s'%datRng
    story.append(rlp.Spacer(1,36))
    story.append(rlp.Paragraph(txt,styles["Normal"]))
    story.append(rlp.Spacer(1,36))
    txt='''Rechnung für<br/>
    <br/>
    <b>%s %s, geb: %s'''%(klient[8:11])
    if len(klient[11])>0: txt+='AHV-Nr: %s'%klient[11]
    txt+='</b>'
    story.append(rlp.Paragraph(txt,styles["Normal"]))

    story.append(rlp.Spacer(1,12))
    #data=[['00','01','02','03','04'],
    #      ['10','11','12','13','14'],
    #      ['20','21','22','23','24'],
    #      ['30','31','32','33','34']]

    #t=rlp.Table(data)
    #t.setStyle(rlp.TableStyle([('BACKGROUND',(1,1),(-2,-2),rll.colors.green),
    #                           ('TEXTCOLOR',(0,0),(1,-1),rll.colors.red)]))
    #story.append(t)

    data=[('Datum','Stundenansatz','Minuten','Bemerkung','TarifZif','Total',)]
    totSum=0.
    for datBehandlung,Stundenansatz,Dauer,Bemerkung,TarZif in behandlungen:
      tot=Stundenansatz*Dauer/60
      totSum+=tot
      data.append((datBehandlung,'%.2f'%Stundenansatz,'%d Min'%Dauer,Bemerkung,TarZif,'%.2f'%tot))
    data.append(('','','','','','%.2f'%totSum))
    #data.append(('','','','','',rlp.Paragraph('<b>%.2f</b>'%totSum,styles['Center'])))
    t=rlp.Table(data)
    t.hAlign='LEFT'
    t.setStyle(rlp.TableStyle([('LINEBELOW',(-1,-2),(-1,-1),1,rll.colors.black),
                               ('LINEBELOW',(-1,-2),(-1,-1),1,rll.colors.black)]))

    story.append(t)

    story.append(rlp.Spacer(1,12))
    txt='''Ich bitte Sie, den Betrag von SFr. %.2f innert 30 Tagen auf folgendes Konto zu überweisen:<br/>
    St. Galler Kantonalbank, IBAN-Nr. CH60 0078 1622 4188 6200 0<br/>
    <br/>
    Monika Kast Perry<br/>
    Praxis weiterkommen<br/>
    Albisstrasse 11<br/>
    8038 Zürich'''%totSum
    story.append(rlp.Spacer(1,12))
    story.append(rlp.Paragraph(txt,styles["Normal"]))
    txt='''Herzlichen Dank und liebe Grüsse'''
    story.append(rlp.Spacer(1,12))
    story.append(rlp.Paragraph(txt,styles["Normal"]))
    story.append(rlp.Spacer(1,12))
    im=rlp.Image("signature.png",8*rlu.cm,2*rlu.cm)
    im.hAlign='CENTER'
    story.append(im)
    txt='''Monika Kast Perry'''
    story.append(rlp.Paragraph(txt,styles["Center"]))
    txt='PS: Es kann über die Zusatzversicherung Ihrer Krankenkasse abgerechnet werden.'
    frm.addFromList(story,canvas)
    canvas.showPage()

  def finalize(self):
    self.canvas.save()
    pass


if __name__ == '__main__':
  rep=Invoice()
  rep.init()
  lstKlient=\
    (('Frau ', 'Saki', 'Karakurt', 'Meierwiesenstrasse 24', '', '', '8107', 'Buchs', 'Bayraktar', 'Aras', '15.02.2012', ''),
     ('Familie', 'Preisig U. &', 'C.', 'Sihlaustr. 3', '', '', '8134', 'Adliswil', 'Radic Baumgartner', 'Ksenija', '18.06.1975', ''),)
  lstDatRng=\
    (('17.03.2020'),('26.06.2020'),)
  lstBeh=\
      ((('15.05.2020', 142.0, 60.0, '', ''),('22.05.2020', 142.0, 60.0, '', ''),('29.05.2020', 142.0, 60.0, '', ''),('03.06.2020', 142.0, 60.0, '', ''),('12.06.2020', 142.0, 60.0, '', '')),
       (('19.06.2020', 180.0, 60.0, '', ''),('31.07.2020', 180.0, 60.0, '', ''),('31.07.2020', 180.0, 60.0, '', ''),('06.08.2020', 180.0, 60.0, '', '')))

  for i in range(2):
    rep.add(lstKlient[i],lstDatRng[i],lstBeh[i])
  rep.finalize()
