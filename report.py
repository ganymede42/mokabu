#!/usr/bin/python3
import time,os,platform,re,sys
import subprocess as spc
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

def default_app_open(file):
  if platform.system() == 'Darwin':       # macOS
    spc.call(('open', file))
  elif platform.system() == 'Windows':    # Windows
    os.startfile(file)
  else:                                   # linux variants
    spc.call(('xdg-open', file))

class HeaderFooter(rlp.flowables.Flowable):
  def __init__(self,txt):
    self.txt=txt
  def wrap(self,*args):
    return (0,0)
  def draw(self):
    pass

class Couvert():
  def __init__(self,fn='couvert.pdf'):
    #dimension by default 1/72 inch
    self.canvas=canvas=rlpg.canvas.Canvas(fn,pagesize=(rlps.A4[1],rlps.A4[0]))
    self.styles=styles=rls.getSampleStyleSheet()
    styles.add(rls.ParagraphStyle(name='Justify', alignment=rle.TA_JUSTIFY))
    styles.add(rls.ParagraphStyle(name='Right', alignment=rle.TA_RIGHT))
    styles.add(rls.ParagraphStyle(name='Center', alignment=rle.TA_CENTER))

    styN=styles['Normal']
    styR=styles['Right']
    styC=styles["Center"]
    styJ=styles["Justify"]
    sz=rlps.A4
    brd=(1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm)#l,r,t,b
    l=brd[0];r=sz[0]-brd[1];t=sz[1]-brd[2];b=brd[3]
    canvas.setLineWidth(.3)
    #canvas.line(l,t,r,t)
    #canvas.line(l,b,r,b)
    brd=(1.4*rlu.cm,1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm)#l,r,t,b

    # frm=rlp.Frame(brd[0],brd[3],sz[0]-brd[0]-brd[1],sz[1]-brd[2]-brd[3],showBoundary=1)
    x1=5*rlu.cm; y1=3*rlu.cm; w1=7*rlu.cm; h1=4*rlu.cm
    y1=rlps.A4[0]-y1-h1
    frm=rlp.Frame(x1,y1,w1,h1,showBoundary=0)

    #im=rlp.Image("Logo_Monika_s.png",7*rlu.cm,2*rlu.cm)
    x=x1+w1; y=y1; w=7*rlu.cm; h=2*rlu.cm
    y=y1+1.5*rlu.cm
    canvas.drawImage("Logo_Monika_s.png",x,y,w,h)
    story=[]
    #im=rlp.Image("Logo_Monika_s.png",7*rlu.cm,2*rlu.cm)
    #im.hAlign='RIGHT'
    #story.append(im)
    #story.append(rlp.Spacer(1,12))
    txt='''<font size="8"><b>Monika Kast Perry</b><br/>
    Dr. phil., Fachpsychologin<br/>
    für Kinder- & Jugendpsychologie FSP<br/>
    eidg. anerkannte Psychotherapeutin.<br/>
    Albisstrasse 11 · 8038 Zürich · +41 76 335 72 79<br/></font>
    <font size="8">monika.kast-perry@psychologie.ch<br/>
    praxis-weiterkommen.com</font>'''
    story.append(rlp.Paragraph(txt,styR))
    frm.addFromList(story,canvas)
    canvas.showPage()
    canvas.save()


class Invoice():

  def __init__(self,fn='invoice.pdf'):
    #dimension by default 1/72 inch
    self.canvas=canvas=rlpg.canvas.Canvas(fn,pagesize=rlps.A4)
    self.styles=styles=rls.getSampleStyleSheet()
    styles.add(rls.ParagraphStyle(name='Justify', alignment=rle.TA_JUSTIFY))
    styles.add(rls.ParagraphStyle(name='Right', alignment=rle.TA_RIGHT))
    styles.add(rls.ParagraphStyle(name='Center', alignment=rle.TA_CENTER))

  def add(self,klient,tplID,datRng,behandlungen):
    #Vorlagen:
    #Mahnungen nicht IV
    #/media/zamofing_t/DataHD/Praxis/KlientenMerge/all/Viehweg Lina/Rechnung_20200717.docx
    #/media/zamofing_t/DataHD/Praxis/KlientenMerge/all/Viehweg Lina/Zahlungserinnerung_Rechnung_20200717.docx
    #/media/zamofing_t/DataHD/Praxis/KlientenMerge/all/Viehweg Lina/zweite Mahnung_Rechnung_20200717.docx
    #/media/zamofing_t/DataHD/Praxis/KlientenMerge/all/Osei Lawrence/Rechnung mit Tarifziffern_20200924.docx
    #tplID&0x3:    2 Bit
    # 0: Normal
    # 1: 1. Mahnung
    # 2: 2. Mahnung
    #(tplID>>2)&0x1:
    # 0: Normal
    # 1: IV mit Tarifziffer
    if tplID==None:tplID=0x8
    tplMahnung=tplID&0x3
    tplIV=(tplID)&0x4
    tplQR=(tplID)&0x8

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
    #canvas.line(l,t,r,t)
    #canvas.line(l,b,r,b)
    brd=(1.4*rlu.cm,1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm)#l,r,t,b

    frm=rlp.Frame(brd[0],brd[3],sz[0]-brd[0]-brd[1],sz[1]-brd[2]-brd[3],showBoundary=0)

    story=[]
    im=rlp.Image("Logo_Monika_s.png",7*rlu.cm,2*rlu.cm)
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
    story.append(rlp.Spacer(1,-24))
    txt='''
    %s<br/>
    %s %s<br/>'''%tuple(map(lambda x: x if x else '',klient[0:3]))
    for i in range(3,6):
      adr=klient[i]
      if adr: # not None and not empty
        txt+=adr+'<br/>'
    txt+='%s %s<br/>'''%tuple(map(lambda x: x if x else '',klient[6:8]))
    story.append(rlp.Paragraph(txt,styN))
    story.append(rlp.Spacer(1,24+24))
    txt='Zürich, %s'%dateconvert(datRng)
    story.append(rlp.Paragraph(txt,styN))
    story.append(rlp.Spacer(1,12))

    if tplMahnung==1:
      txt='<b>Zahlungserinnerung</b><br/>Es dürfte Ihrer Aufmerksamkeit entgangen sein, dass die nachstehend aufgeführten Rechnungsposten noch offen sind. Ich bitte Sie, die fälligen Rechnungsbeträge innert 10 Tagen einzuzahlen und danke Ihnen für die fristgerechte Überweisung. Sollte sich Ihre Zahlung mit diesem Schreiben gekreuzt haben, betrachten Sie es bitte als gegenstandslos.'
    elif tplMahnung==2:
      txt='<b>2. Mahnung</b><br/>Den unten stehenden Rechnungsposten haben Sie trotz Zahlungserinnerung nicht bezahlt. Sie ersparen sich Unannehmlichkeiten und weitere Kosten, wenn Sie den fälligen Betrag innert 15 Tagen überweisen. Sollte sich Ihre Zahlung mit diesem Schreiben gekreuzt haben, betrachten Sie es bitte als gegenstandslos.'
    else:
      txt='<b>Rechnung für</b>'

    txt+='<br/><br/><b>%s %s'%(klient[8:10])

    geb=klient[10]
    ahvOrt=klient[11]
    if ahvOrt:
      ahvOrt=ahvOrt.split(maxsplit=1)
      if len(ahvOrt)==1:
        ahvOrt.append(None)
      ahv,ort=ahvOrt
    else:
      ahv=ort=None

    if tplIV and ort:
      txt+=', '+ort
    if geb is not None: txt+=', geb: %s'%dateconvert(geb)
    if ahv is not None: txt+=', AHV-Nr: %s'%ahv
    txt+='</b>'
    story.append(rlp.Paragraph(txt,styJ))

    story.append(rlp.Spacer(1,12))

    if tplIV:
      data=[('Datum','Tarif','Tarifziffer','Inhalt',rlp.Paragraph('Anzahl a 15min',styR),'Kosten',)]
      totSum=0.
      for datBehandlung,Stundenansatz,Dauer,Bemerkung,TarZif in behandlungen:
        if Stundenansatz is None: Stundenansatz=0
        if Dauer is None: Dauer=0
        if TarZif is None:TarZif=''
        tot=Stundenansatz*Dauer/60
        totSum+=tot
        #pBemerkung=
        if Bemerkung:
          pBemerkung=rlp.Paragraph('<font size="8">'+Bemerkung+'</font>',styN)
        else:
          pBemerkung=''
        #data.append((dateconvert(datBehandlung),'%.2f'%Stundenansatz,'%d Min'%Dauer,pBemerkung,TarZif,'%.2f'%tot))
        data.append((dateconvert(datBehandlung),TarZif.split('.')[0],TarZif, pBemerkung, '%g'%(Dauer/15),'%.2f'%tot))
      #pTotSum='%.2f'%totSum
      pTotSum=rlp.Paragraph('<b>%.2f</b>'%totSum,styR)
      data.append(('','','','','',pTotSum))

      t=rlp.Table(data,colWidths=(60,40,60,200,50,50,))
      t.hAlign='LEFT'
      t.setStyle(rlp.TableStyle([#('INNERGRID',(0,0),(-1,-1),0.15,rll.colors.black),
                                 #('BOX',(0,0),(-1,-1),0.15,rll.colors.black),
                                 ('ALIGN',(0,0),(0,-1),'RIGHT'),
                                 ('ALIGN',(1,0),(2,-1),'RIGHT'),
                                 ('ALIGN',(4,0),(4,-1),'CENTER'),
                                 ('ALIGN',(5,0),(5,-1),'RIGHT'),
                                 ('LINEBELOW',(-1,-2),(-1,-1),1,rll.colors.black)]))
    else:
      data=[('Datum','Bemerkung','Stundenansatz','Minuten','Total',)]
      totSum=0.
      for datBehandlung,Stundenansatz,Dauer,Bemerkung,TarZif in behandlungen:
        if Stundenansatz is None: Stundenansatz=0
        if Dauer is None: Dauer=0
        tot=Stundenansatz*Dauer/60
        totSum+=tot
        #pBemerkung=
        if Bemerkung:
          pBemerkung=rlp.Paragraph('<font size="9">'+Bemerkung+'</font>',styN)
          #pBemerkung=rlp.Paragraph(Bemerkung,styN)
        else:
          pBemerkung=''
        data.append((dateconvert(datBehandlung),pBemerkung,'%.2f'%Stundenansatz,'%d Min'%Dauer,'%.2f'%tot))
      #pTotSum='%.2f'%totSum
      pTotSum=rlp.Paragraph('<b>%.2f</b>'%totSum,styR)
      data.append(('','','','',pTotSum))

      t=rlp.Table(data,colWidths=(60,210,50,50,50,))
      t.hAlign='LEFT'
      t.setStyle(rlp.TableStyle([#('INNERGRID',(0,0),(-1,-1),0.25,rll.colors.black),
                                 #('BOX',(0,0),(-1,-1),0.25,rll.colors.black),
                                 ('ALIGN',(0,0),(0,-1),'RIGHT'), #datum
                                 ('ALIGN',(2,0),(-1,-1),'RIGHT'), #others
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
    story.append(rlp.Spacer(1,12))
    txt='PS: Es kann über die Zusatzversicherung Ihrer Krankenkasse abgerechnet werden.'
    story.append(rlp.Paragraph(txt,styJ))
    frm.addFromList(story,canvas)

    if tplQR:
      fmt='''SPC\n0200\n1\nCH6000781622418862000\nS\nPraxis Weiterkommen Monika Kast Perry\nAlbisstrasse 11\n\n8038\nZürich\nCH\n\n\n\n\n\n\n\n%.2f\nCHF\nS\n\n\n\n\n\n\nNON\n\n%s\nEPD'''
      txt=fmt%(totSum,dateconvert(datRng)+' '+klient[8]+' '+klient[9])
      #https://www.reportlab.com/docs/reportlab-graphics-reference.pdf
      #https://www.paymentstandards.ch/dam/downloads/ig-qr-bill-de.pdf
      #https://de.wikipedia.org/wiki/QR-Rechnung
      #https://qr-rechnung.net/#/
      from reportlab.graphics.shapes import Drawing
      from reportlab.graphics.barcode import getCodes
      outDir='/tmp/barcode'
      os.makedirs(outDir,exist_ok=True)
      w=getCodes()['QR'](txt)
      w.barWidth=96
      w.barHeight=96
      g=w.draw()
      #canvas.drawImage(...)
      x0,y0,x1,y1=w.getBounds()
      drw=Drawing(x1-x0,y1-y0)
      drw.add(w)
      x=16*rlu.cm;y=19.8*rlu.cm
      drw.drawOn(canvas,x,y)
      canvas.setFont("Helvetica", 8)
      canvas.drawCentredString(x+1.7*rlu.cm,y-.1*rlu.cm,'QR-Rechnung')

      #brd=(1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm)  #l,r,t,b
      #l=brd[0];
      #r=sz[0]-brd[1];
      #t=sz[1]-brd[2];
      #b=brd[3]

      #story.append(drw)
      #drw.save(formats=('gif',),outDir=outDir,fnRoot='QR')
      #canvas.line(l,b,r,b)
      #print('gen '+outDir+'/QR.gif')
      #os.system('firefox '+outDir+'/QR.gif')

    canvas.showPage()

  def publish(self):
    self.canvas.save()
    pass


def dateconvert(dateIn,mode=0):
  #input: 2005-02-25
  #mode=0   25.02.2005
  #mode=1   25.02.05
  try:
    dateStruct=time.strptime(dateIn,'%Y-%m-%d')
  except (ValueError,TypeError) as e:
    print('error in dateconvert:"%s"'%str(dateIn),file=sys.stderr)
    return str(dateIn)
  if mode==0:
    dateOut=time.strftime('%d.%m.%Y',dateStruct)
  elif mode==1:
    dateOut=time.strftime('%d.%m.%y',dateStruct)
  return dateOut


class TherapyProgress(rlp.SimpleDocTemplate):

  def __init__(self,fn='therapy_progress.pdf'):
    super(TherapyProgress,self).__init__(fn,pagesize=rlps.A4,
                        rightMargin=2*rlu.cm,leftMargin=2*rlu.cm,
                        topMargin=1.2*rlu.cm,bottomMargin=1.7*rlu.cm)
    self.styles=styles=rls.getSampleStyleSheet()
    styles.add(rls.ParagraphStyle(name='Justify', alignment=rle.TA_JUSTIFY))
    styles.add(rls.ParagraphStyle(name='Right', alignment=rle.TA_RIGHT))
    styles.add(rls.ParagraphStyle(name='Center', alignment=rle.TA_CENTER))
    self.story=story=[]
    styN=self.styles['Normal']
    styR=self.styles['Right']
    styJ=self.styles['Justify']
    styC=self.styles['Center']
    self.defaultVars=(story,styN,styJ,styR,styC)

  def beforeDocument(self):
    canvas=self.canv
    canvas.setAuthor('name')
    canvas.setTitle('title')
    canvas.setSubject('subj')
    self.header='not yet a header'
    self.clientPage=1

  def beforePage(self):
    canvas=self.canv
    sz=rlps.A4
    brd=(1.2*rlu.cm,1.2*rlu.cm,1.2*rlu.cm,1.7*rlu.cm)#l,r,t,b
    l=brd[0];r=sz[0]-brd[1];t=sz[1]-brd[2];b=brd[3]
    canvas.setLineWidth(.3)
    canvas.line(l,t,r,t)
    canvas.line(l,b,r,b)
    #could add a frame with personal header paragraph
    pageNumber = canvas.getPageNumber()
    canvas.setFont("Helvetica",10)
    #canvas.drawString(10*rlu.cm, rlu.cm, str(pageNumber))

  def afterPage(self):
    canvas=self.canv
    sz=rlps.A4
    brd=(1.2*rlu.cm,1.2,1.2*rlu.cm,1.7*rlu.cm)#l,r,t,b
    l=brd[0];r=sz[0]-brd[1];t=sz[1]-brd[2];b=brd[3]
    canvas.drawString(10*rlu.cm, t+.2*rlu.cm, str(self.clientPage))
    canvas.setFont("Helvetica-Bold",10)
    canvas.drawRightString(r-2*rlu.cm, t+.2*rlu.cm, self.header)
    self.clientPage+=1

  def afterFlowable(self, flowable):
    if isinstance(flowable,HeaderFooter):
      self.header=flowable.txt
      self.clientPage=1

  def add(self,client,therapyLst):
    self.addClient(*client)
    for therapy in therapyLst:
      self.addTherapyProgress(*therapy)

  def addClient(self,nachname,vorname,datGeb,tel,eMail):
    (story,styN,styJ,styR,styC)=self.defaultVars
    story.append(rlp.PageBreakIfNotEmpty())
    #story.append(rlp.DocAssign('hdr',"nachname+' '+vorname"))
    if tel is None:tel=''
    if eMail is None: eMail=''
    header='%s %s %s %s %s'%(nachname,vorname,dateconvert(datGeb),tel,eMail)
    story.append(HeaderFooter(header))
    #story.append(rlp.Paragraph('<b>'+header+'</b>',styN))
    story.append(rlp.Spacer(1,18))

  def addTherapyProgress(self,date,title,treatment):
    (story,styN,styJ,styR,styC)=self.defaultVars
    story.append(rlp.Paragraph('<b>%s %s</b>'%(dateconvert(date,1),title),styN))
    story.append(rlp.Indenter(36,0))

    txt=str(treatment)
    p0=-1
    p3=0
    while True:
      m=re.search('<p\s+.*?>',txt[p3:])
      if m is None: break
      sp=m.span()
      p0=p3+sp[0];p1=p3+sp[1]
      parSty=txt[p0:p1]
      n=re.search('</p>',txt[p1:])
      sp=n.span()
      p2=p1+sp[0];p3=p1+sp[1]

      if parSty.find('center')>=0:
        sty=styC
      elif parSty.find('justify')>=0:
        sty=styJ
      elif parSty.find('right')>=0:
        sty=styR
      else:
        sty=styN
      story.append(rlp.Paragraph(txt[p1:p2],sty))
    if p0==-1: # no html text
      txt=re.sub('\n','<br/>',txt)
      story.append(rlp.Paragraph(txt,styJ))

    story.append(rlp.Indenter(-36,0))
    story.append(rlp.Spacer(1,12))
    #story.append(rlp.DocPara('doc.canv.getPageNumber()','The current page number is %(__expr__)d',style=styN))

  def publish(self):
    self.build(self.story)

def playground(fn='test.pdf',lorIps='my long sample text '*100):
  canvas=rlpg.canvas.Canvas(fn,pagesize=rlps.A4)
  styles=rls.getSampleStyleSheet()
  styles.add(rls.ParagraphStyle(name='Justify', alignment=rle.TA_JUSTIFY))
  styles.add(rls.ParagraphStyle(name='Right', alignment=rle.TA_RIGHT))
  styles.add(rls.ParagraphStyle(name='Center', alignment=rle.TA_CENTER))
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
  canvas.showPage() #adds a new page
  canvas.save()


def test1(fn):
  from reportlab.lib.styles import ParagraphStyle
  from reportlab.platypus import SimpleDocTemplate,Paragraph
  from reportlab.platypus.flowables import DocAssign,DocExec,DocPara,DocIf,DocWhile
  normal=ParagraphStyle(name='Normal',fontName='Helvetica',fontSize=8.5,leading=11)
  header=ParagraphStyle(name='Heading1',parent=normal,fontSize=14,leading=19,
                        spaceAfter=6,keepWithNext=1)
  story=[
    DocAssign('currentFrame','doc.frame.id'),
    DocAssign('currentPageTemplate','doc.pageTemplate.id'),
    DocAssign('aW','availableWidth'),
    DocAssign('aH','availableHeight'),
    DocAssign('aWH','availableWidth,availableHeight'),
    DocAssign('i',3),
    DocIf('i>3',Paragraph('The value of i is larger than 3',normal),
          Paragraph('The value of i is not larger than 3',normal)),
    DocIf('i==3',Paragraph('The value of i is equal to 3',normal),Paragraph('The value of i is not equal to 3',normal)),
    DocIf('i<3',Paragraph('The value of i is less than 3',normal),
          Paragraph('The value of i is not less than 3',normal)),
    DocWhile('i',[DocPara('i',format='The value of i is %(__expr__)d',style=normal),DocExec('i-=1')]),
    DocPara(
      '"{"+", ".join(("%s=%s" % (_k,(_v.__class__.__name__ if "<" in repr(_v) else repr(_v)[1:] if repr(_v) and repr(_v)[0] in "ub" else repr(_v))) for _k,_v in sorted(doc._nameSpace.items()) if _k not in ("_k","_v")))+"}"',
      escape=True),
    DocPara('doc.canv.getPageNumber()','The current page number is %(__expr__)d',style=normal)
  ]
  doc=SimpleDocTemplate(fn)
  doc.build(story)

def testBarcode():
  #/home/zamofing_t/Documents/prj/Mokabu/scratch/reportlab/tests/test_graphics_barcode.py
  txt='''SPC\n0200\n1\nCH6000781622418862000\nS\nPraxis weiterkommen Monika Kast Perry\nAlbisstrasse 11\n\n8038\nZürich\nCH\n\n\n\n\n\n\n\n\nCHF\n\n\n\n\n\n\n\nNON\n\n\nEPD'''
  txt='''SPC\n0200\n1\nCH6000781622418862000\nS\nPraxis weiterkommen Monika Kast Perry\nAlbisstrasse 11\n\n8038\nZürich\nCH\n\n\n\n\n\n\n\n1234.00\nCHF\nS\nPersZahlung\nStrasseZahlung\n\n5430\nWettingen\nCH\nNON\n\nMitteilung\nEPD'''
  fmt='''SPC\n0200\n1\nCH6000781622418862000\nS\nPraxis weiterkommen Monika Kast Perry\nAlbisstrasse 11\n\n8038\nZürich\nCH\n\n\n\n\n\n\n\n%.2f\nCHF\nS\n\n\n\n\n\n\nNON\n\n%s\nEPD'''
  txt=fmt%(1234,'Mitteilung')
  #https://www.paymentstandards.ch/dam/downloads/ig-qr-bill-de.pdf
  #https://de.wikipedia.org/wiki/QR-Rechnung
  #https://qr-rechnung.net/#/
  from reportlab.graphics.shapes import Drawing
  from reportlab.graphics.barcode import getCodes
  outDir='/tmp/barcode'
  os.makedirs(outDir,exist_ok=True)
  i=getCodes()['QR'](txt)  #createBarcodeDrawing('QR',txt)
  i.barWidth=300
  i.barHeight=300

  x0,y0,x1,y1=i.getBounds()
  D=Drawing(x1-x0,y1-y0)
  D.add(i)
  D.save(formats=('gif',),outDir=outDir,fnRoot='QR')
  print('gen '+outDir+'/QR.gif')
  os.system('firefox '+outDir+'/QR.gif')
  return


if __name__ == '__main__':

  lorIps='Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et:::'

  lorIps='''<p>Wenn er nicht gehorcht streicht sie das Gamen und TV schauen. In der Regel darf Aras 60 min Medienkonsum. Diesen streicht sie manchmal für die ganze Woche. Wenn er Stempel von der Schule nach Hause bringt, hat es gut gemacht, kann er sich den Medienkonsum wieder verdienen.</p>
<p align="center">Wenn er nicht gehorcht streicht sie das Gamen und TV schauen. In der Regel darf Aras 60 min Medienkonsum. Diesen streicht sie manchmal für die ganze Woche. Wenn er Stempel von der Schule nach Hause bringt, hat es gut gemacht, kann er sich den Medienkonsum wieder verdienen.</p>
<p align="right">Wenn er nicht gehorcht streicht sie das Gamen und TV schauen. In der Regel darf Aras 60 min Medienkonsum. Diesen streicht sie manchmal für die ganze Woche. Wenn er Stempel von der Schule nach Hause bringt, hat es gut gemacht, kann er sich den Medienkonsum wieder verdienen.</p>
<p align="justify">Wenn er nicht gehorcht streicht sie das Gamen und TV schauen. In der Regel darf Aras 60 min Medienkonsum. Diesen streicht sie manchmal für die ganze Woche. Wenn er Stempel von der Schule nach Hause bringt, hat es gut gemacht, kann er sich den Medienkonsum wieder verdienen.</p>
<p align="justify">Wenn er nicht <b>gehorcht</b> <i>streicht</i> <u>sie</u> das Gamen und TV schauen. In der Regel darf Aras 60 min Medienkonsum. Diesen streicht sie manchmal für die ganze Woche. Wenn er Stempel von der Schule nach Hause bringt, hat es gut gemacht, kann er sich den Medienkonsum wieder verdienen.</p>
'''


  def testInvoice(fn):
    lstKlient=\
      ((None, 'Saki', 'Karakurt', 'Meierwiesenstrasse 24', '', '', None, 'Buchs', 'Bayraktar', 'Aras', '2012-02-15', '765.234.433.454 Frick'),
      #(('Frau ','Saki','Karakurt','Meierwiesenstrasse 24','','','8107','Buchs','Bayraktar','Aras','2012-02-15','765.234.433.454 Frick'),
        ('Familie', 'Preisig U. &', 'C.', 'Sihlaustr. 3', '', '', '8134', 'Adliswil', 'Radic Baumgartner', 'Ksenija', '1975-06-18', None),)
    lstTpl=\
      (None,8,9,10,12)
      #(None,0,1,2,4,8)
    lstDatRng=\
      (('2020-03-17'),('2020-06-26'),)
    lstBeh=\
        ((('2020-05-15', 142.0, 60.0, 'Bemerkung 1', '752.34'),
          ('2020-05-22', 142.0, 60.0, 'Bemerkung 2', '752.35'),
          ('2020-05-29', 142.0, 60.0, 'Bemerkung 3', '752.36'),
          ('2020-06-03', 142.0, 60.0, 'Bemerkung 4', '752.37'),
          ('2020-06-12', 142.0, 60.0, 'Bemerkung 5', '752.38')),
         (('2020-06-19', 180.0, 60.0, 'Bemerkung 1', '752.34'),
          ('2020-07-31', 180.0, 60.0, 'Bemerkung 2', '752.35'),
          ('2020-07-31', 180.0, 60.0, 'Bemerkung 3', '752.36'),
          ('2020-08-06', 180.0, 60.0, 'Bemerkung 4', '752.37'),
          ('2020-06-19', 180.0, 60.0, 'Bemerkung 5', '752.38'),
          ('2020-07-31', 180.0, 60.0, 'Bemerkung 6', '752.39'),
          ('2020-07-31', 180.0, 60.0, 'Bemerkung 7', '753.34'),
          ('2020-08-06', 180.0, 60.0, 'Bemerkung 8', '754.34')))

    rep=Invoice(fn)
    for i in range(len(lstKlient)):
      rep.add(lstKlient[i],None,lstDatRng[i],lstBeh[i])
    for i in range(len(lstTpl)):
      rep.add(lstKlient[0],lstTpl[i],lstDatRng[0],lstBeh[0])


    rep.publish()

  def testTherapyProgress(fn):
    lstKlient=\
      (('Bayraktar', 'Aras', '2012-02-15', '', ''),
       ('Radic Baumgartner', 'Ksenija', '1975-06-18', '', ''),)
    lstBeh=\
        ((('2020-05-15', 'title00', lorIps),('2020-05-22', 'title01', lorIps),('2020-05-29', 'title02', lorIps),('2020-06-03', 'title03', lorIps),('2020-06-03', 'title03', lorIps),('2020-06-03', 'title03', lorIps),('2020-06-03', 'title03', lorIps)),
         (('2020-06-19', 'title10', lorIps),('2020-07-31', 'title11', lorIps),('2020-07-31', 'title12', '')))

    rep=TherapyProgress(fn)
    for i in range(2):
      rep.add(lstKlient[i],lstBeh[i])
      #rep.addClient(*lstKlient[i])
      #for beh in lstBeh[i]:
      #  rep.addTherapyProgress(*beh)
    rep.publish()


  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('-m', '--mode', type=int, help='mode bits', default=0xff)
  args = parser.parse_args()
  print(args)

  fn='test%d.pdf'
  idx=0
  #test1(fn%idx)
  #default_app_open(fn%idx);idx+=1

  #playground(fn%idx,lorIps)
  #default_app_open(fn%idx);idx+=1
  if args.mode&1:
    testInvoice(fn%idx)
    default_app_open(fn%idx);idx+=1

  if args.mode&2:
    testTherapyProgress(fn%idx)
    default_app_open(fn%idx);idx+=1
  if args.mode&4:
    testBarcode()
    #default_app_open(fn%idx);idx+=1
  if args.mode&8:
    Couvert(fn%idx)
    default_app_open(fn%idx);idx+=1





