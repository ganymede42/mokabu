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

class Invoice():

  def __init__(self,fn='invoice.pdf'):
    #dimension by default 1/72 inch
    self.canvas=canvas=rlpg.canvas.Canvas(fn,pagesize=rlps.A4)
    self.styles=styles=rls.getSampleStyleSheet()
    styles.add(rls.ParagraphStyle(name='Justify', alignment=rle.TA_JUSTIFY))
    styles.add(rls.ParagraphStyle(name='Right', alignment=rle.TA_RIGHT))
    styles.add(rls.ParagraphStyle(name='Center', alignment=rle.TA_CENTER))

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
    #canvas.line(l,t,r,t)
    #canvas.line(l,b,r,b)
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
      if adr: # not None and not empty
        txt+=adr+'<br/>'
    txt+='%s %s<br/>'''%klient[6:8]

    story.append(rlp.Spacer(1,36))
    story.append(rlp.Paragraph(txt,styN))
    txt='Zürich, %s'%dateconvert(datRng)
    story.append(rlp.Spacer(1,36))
    story.append(rlp.Paragraph(txt,styN))
    story.append(rlp.Spacer(1,36))
    txt='Rechnung für<br/><br/><b>%s %s'%(klient[8:10])
    if klient[10] is not None: txt+=', geb: %s'%dateconvert(klient[10])
    if klient[11]  is not None: txt+=' AHV-Nr: %s'%klient[11]
    txt+='</b>'
    story.append(rlp.Paragraph(txt,styN))

    story.append(rlp.Spacer(1,12))
    data=[('Datum','Stundenansatz','Minuten','Bemerkung','TarifZif','Total',)]
    totSum=0.
    for datBehandlung,Stundenansatz,Dauer,Bemerkung,TarZif in behandlungen:
      tot=Stundenansatz*Dauer/60
      totSum+=tot
      #pBemerkung=
      if Bemerkung:
        pBemerkung=rlp.Paragraph('<font size="8">'+Bemerkung+'</font>',styN)
      else:
        pBemerkung=''
      data.append((dateconvert(datBehandlung),'%.2f'%Stundenansatz,'%d Min'%Dauer,pBemerkung,TarZif,'%.2f'%tot))
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
    return 'xx.xx.xx.'
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

  def addClient(self,nachname,vorname,datGeb,tel1,eMail):
    (story,styN,styJ,styR,styC)=self.defaultVars
    story.append(rlp.PageBreakIfNotEmpty())
    #story.append(rlp.DocAssign('hdr',"nachname+' '+vorname"))
    if tel1 is None:tel1=''
    if eMail is None: eMail=''
    header='%s %s %s %s %s'%(nachname,vorname,dateconvert(datGeb),tel1,eMail)
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
      (('Frau ', 'Saki', 'Karakurt', 'Meierwiesenstrasse 24', '', '', '8107', 'Buchs', 'Bayraktar', 'Aras', '2012-02-15', ''),
       ('Familie', 'Preisig U. &', 'C.', 'Sihlaustr. 3', '', '', '8134', 'Adliswil', 'Radic Baumgartner', 'Ksenija', '1975-18-06', ''),)
    lstDatRng=\
      (('2020-03-17'),('2020-06-26'),)
    lstBeh=\
        ((('2020-05-15', 142.0, 60.0, '', ''),('2020-05-22', 142.0, 60.0, '', ''),('2020-05-29', 142.0, 60.0, '', ''),('2020-06-03', 142.0, 60.0, '', ''),('2020-06-12', 142.0, 60.0, '', '')),
         (('2020-06-19', 180.0, 60.0, '', ''),('2020-07-31', 180.0, 60.0, '', ''),('2020-07-31', 180.0, 60.0, '', ''),('2020-08-06', 180.0, 60.0, '', ''),('2020-06-19', 180.0, 60.0, '', ''),('2020-07-31', 180.0, 60.0, '', ''),('2020-07-31', 180.0, 60.0, '', ''),('2020-08-06', 180.0, 60.0, '', '')))

    rep=Invoice(fn)
    for i in range(2):
      rep.add(lstKlient[i],lstDatRng[i],lstBeh[i])
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


  fn='test%d.pdf'
  idx=0
  #test1(fn%idx)
  #default_app_open(fn%idx);idx+=1

  #playground(fn%idx,lorIps)
  #default_app_open(fn%idx);idx+=1

  #testInvoice(fn%idx)
  #default_app_open(fn%idx);idx+=1

  testTherapyProgress(fn%idx)
  default_app_open(fn%idx);idx+=1




