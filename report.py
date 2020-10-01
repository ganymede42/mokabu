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
    styN=styles['Normal']
    styR=styles['Right']
    styC=styles["Center"]
    styJ=styles["Justify"]
    sz=rlps.A4
    brd=(1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm)#l,r,t,b
    l=brd[0];r=sz[0]-brd[1];t=sz[1]-brd[2];b=brd[3]
    canvas.setLineWidth(.3)
    canvas.line(l,t,r,t)
    canvas.line(l,b,r,b)
    brd=(1.4*rlu.cm,1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm)#l,r,t,b

    frm=rlp.Frame(brd[0],brd[3],sz[0]-brd[0]-brd[1],sz[1]-brd[2]-brd[3],showBoundary=0)

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
    story.append(rlp.Paragraph(txt,styR))

    txt='''
    %s<br/>
    %s %s<br/>'''%klient[0:3]
    for i in range(3,6):
      adr=klient[i]
      if len(adr)>0:
        txt+=adr+'<br/>'
    txt+='%s %s<br/>'''%klient[6:8]

    story.append(rlp.Spacer(1,36))
    story.append(rlp.Paragraph(txt,styN))
    txt='Zürich, %s'%datRng
    story.append(rlp.Spacer(1,36))
    story.append(rlp.Paragraph(txt,styN))
    story.append(rlp.Spacer(1,36))
    txt='''Rechnung für<br/>
    <br/>
    <b>%s %s, geb: %s'''%(klient[8:11])
    if len(klient[11])>0: txt+=' AHV-Nr: %s'%klient[11]
    txt+='</b>'
    story.append(rlp.Paragraph(txt,styN))

    story.append(rlp.Spacer(1,12))
    data=[('Datum','Stundenansatz','Minuten','Bemerkung','TarifZif','Total',)]
    totSum=0.
    for datBehandlung,Stundenansatz,Dauer,Bemerkung,TarZif in behandlungen:
      tot=Stundenansatz*Dauer/60
      totSum+=tot
      #pBemerkung=
      pBemerkung=rlp.Paragraph('<font size="8">'+Bemerkung+'</font>',styN)
      data.append((datBehandlung,'%.2f'%Stundenansatz,'%d Min'%Dauer,pBemerkung,TarZif,'%.2f'%tot))
    #pTotSum='%.2f'%totSum
    pTotSum=rlp.Paragraph('<b>%.2f</b>'%totSum,styR)
    data.append(('','','','','',pTotSum))

    t=rlp.Table(data,colWidths=(60,80,60,130,50,60,))
    t.hAlign='LEFT'
    t.setStyle(rlp.TableStyle([#('INNERGRID',(0,0),(-1,-1),0.25,rll.colors.black),
                               #('BOX',(0,0),(-1,-1),0.25,rll.colors.black),
                               ('ALIGN',(0,0),(0,0),'CENTER'),
                               ('ALIGN',(1,0),(2,-1),'RIGHT'),
                               ('ALIGN',(5,0),(5,-1),'RIGHT'),
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
    story.append(rlp.Paragraph(txt,styN))
    txt='''Herzlichen Dank und liebe Grüsse'''
    story.append(rlp.Spacer(100,12))
    story.append(rlp.Paragraph(txt,styN))
    story.append(rlp.Spacer(1,12))
    im=rlp.Image("signature.png",8*rlu.cm,8*262/1024*rlu.cm) #1024x262, 735x139
    im.hAlign='CENTER'
    story.append(im)
    story.append(rlp.Spacer(1,12))
    txt='''Monika Kast Perry'''
    story.append(rlp.Paragraph(txt,styC))
    txt='PS: Es kann über die Zusatzversicherung Ihrer Krankenkasse abgerechnet werden.'
    frm.addFromList(story,canvas)
    canvas.showPage()

  def playground(self):
    lorIps='Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et'
    canvas=self.canvas
    styles=self.styles
    styN=styles['Normal']
    styC=styles["Center"]
    styJ=styles["Justify"]
    sz=rlps.A4
    brd=(1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm)#l,r,t,b
    l=brd[0];r=sz[0]-brd[1];t=sz[1]-brd[2];b=brd[3]
    canvas.setLineWidth(.3)
    canvas.line(l,t,r,t)
    canvas.line(l,b,r,b)
    brd=(1.4*rlu.cm,1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm)#l,r,t,b

    styT=rls.ParagraphStyle(name='Test',fontSize=6,leading=8,backColor='yellow',alignment=rle.TA_CENTER)
    styT=rls.ParagraphStyle(name='Test',fontSize=6,leading=8,backColor='yellow',leftIndent=50,endDots='_.,',spaceBefore=20,alignment=rle.TA_LEFT)
    #styles.add(rls.ParagraphStyle(name='Center', alignment=rle.TA_CENTER))

    story=[]
    story.append(rlp.Paragraph(lorIps,styN))
    story.append(rlp.Paragraph(lorIps,styC))
    story.append(rlp.Paragraph(lorIps,styJ))

    frm=rlp.Frame(brd[0],brd[3],sz[0]-brd[0]-brd[1],sz[1]-brd[2]-brd[3],showBoundary=1)
    frm.addFromList(story,canvas)

    story=[]
    story.append(rlp.Paragraph(lorIps,styT))
    story.append(rlp.Paragraph('ABCD',styJ))
    story.append(rlp.Paragraph('ABCD',styT))
    story.append(rlp.Paragraph('ABCD',styJ))
    r=list(range(10))
    data=list();
    for i in range(5):
      data.append(r)
    t=rlp.Table(data)
    t.hAlign='LEFT'
    t.setStyle(rlp.TableStyle([('LINEBELOW',(-1,-2),(-1,-1),1,rll.colors.black),
                               ('LINEBELOW',(-1,-2),(-1,-1),1,rll.colors.black)]))
    story.append(t)
    story.append(rlp.Paragraph('ABCD',styJ))
    cw=tuple(range(15,40,2));cw=cw[:10]
    t=rlp.Table(data,colWidths=cw)
    t.hAlign='LEFT'
    t.setStyle(rlp.TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                           ('TEXTCOLOR',(1,1),(-2,-2),rll.colors.red),
                           ('VALIGN',(0,0),(0,-1),'TOP'),
                           ('TEXTCOLOR',(0,0),(0,-1),rll.colors.blue),
                           ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                           ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                           ('TEXTCOLOR',(0,-1),(-1,-1),rll.colors.green),
                           ('INNERGRID',(0,0),(-1,-1),0.25,rll.colors.black),
                           ('BOX',(0,0),(-1,-1),0.25,rll.colors.black),
                           ]))
    story.append(t)
    story.append(rlp.Paragraph('ABCD',styJ))
    story.append(rlp.Paragraph('ABCD',styJ))
    story.append(rlp.Paragraph('ABCD',styJ))
    brd=(4*rlu.cm,7*rlu.cm,12*rlu.cm,2*rlu.cm)#l,r,t,b
    frm=rlp.Frame(brd[0],brd[3],sz[0]-brd[0]-brd[1],sz[1]-brd[2]-brd[3],showBoundary=1)
    frm.addFromList(story,canvas)
    canvas.showPage()
    pass


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
  rep.playground()
  rep.finalize()
