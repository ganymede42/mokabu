#!/usr/bin/python3
#https://www.tutorialspoint.com/pyqt/pyqt_hello_world.htm
#https://github.com/tpgit/MDIImageViewer usefull sample application
import sys,time
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtSql as qtdb
import mokabu
import wordprocessor as wp


def MainApp(mkb,dbg):
  app=qtw.QApplication(sys.argv)
  app.mkb=mkb
  app.db=db=qtdb.QSqlDatabase.addDatabase('QSQLITE')
  db.setDatabaseName('mokabu.db')
  if not db.open():
    print('failed to open db')

  app.wndTop=set()
  mainWnd=WndMain() #must be assigned to a variable, else it 'selfsdestructs' before opening
  mainWnd.show()

  #mainWnd.OnWndPerson()

  if dbg&1:
    testPerson(mainWnd)
  if dbg&2:
    testInvoice(mainWnd)
  if dbg&4:
    testTreatment(mainWnd,idx=1)
  if dbg&8:
    mainWnd.OnWndNewInvoices()
  if dbg&16:
    mainWnd.OnWndSyncIvcAcc()


  #wpWnd=wp.MainWindow()
  #wpWnd.record_open(1)
  #WndChildAdd(wpWnd)
  #app.topLevelWindows()
  #app.topLevelWidgets()
  sys.exit(app.exec_())

def testPerson(mainWnd,idx=39):
  wnd=WndPerson('WndPerson: %s'%'TESTING')
  wnd.cbNaVo.setCurrentIndex(idx)
  wnd.OnCbSelChanged(idx)#go to idx person
  sub=qtw.QMdiSubWindow()
  sub.setWidget(wnd)
  mainWnd.mdi.addSubWindow(sub)
  sub.show()

def testInvoice(mainWnd,idx=0,fkPerson=40):
  wnd=WndInvoice('WHERE fkPerson=%d'%fkPerson,'WndInvoice: %s'%'TESTING',fkPerson)
  wnd.cbIvc.setCurrentIndex(idx)
  wnd.OnCbSelChanged(idx)#go to first invoice
  sub=qtw.QMdiSubWindow()
  sub.setWidget(wnd)
  mainWnd.mdi.addSubWindow(sub)
  sub.show()

def testTreatment(mainWnd,idx=0,fkPerson=40):
  wnd=WndTreatment('WHERE fkPerson=%d'%fkPerson,'WndTreatment: %s'%'TESTING',fkPerson)
  wnd.cbTrt.setCurrentIndex(idx)
  wnd.OnCbSelChanged(idx)#go idx treatment
  sub=qtw.QMdiSubWindow()
  sub.setWidget(wnd)
  mainWnd.mdi.addSubWindow(sub)
  sub.show()

def WndChildAdd(wnd):
  app=qtw.QApplication.instance()
  print("WndChildAdd",wnd,app.wndTop)
  app.wndTop.add(wnd)
  wnd.setAttribute(qtc.Qt.WA_DeleteOnClose)
  wnd.destroyed.connect(lambda:WndChildRemove(wnd))
  wnd.show()

def WndChildRemove(wnd):
  app=qtw.QApplication.instance()
  print("WndChildRemove",wnd,app.wndTop)
  app.wndTop.remove(wnd)

def SqlUpdate(fldLst,table,sqlWhere=None):
  sqlFld=list()
  sqlUpd=list()
  ''
  for w in fldLst:
    fld=w.windowTitle()
    try:
      val=w.text()
    except AttributeError:
      val=w.toPlainText()
    if val=='':val=None
    if fld=='id' and sqlWhere is None:
      sqlWhere=' WHERE '+fld+'=?'
      valWhere=val
    else:
      sqlFld.append(fld+'=?')
      sqlUpd.append(val)
  sqlUpd.append(valWhere)
  sqlStr='UPDATE '+table+' SET '+ ','.join(sqlFld) +sqlWhere

  print(sqlStr,sqlUpd)
  app=qtw.QApplication.instance()
  db=app.mkb.db
  dbc=db.cursor()
  dbc.execute(sqlStr,sqlUpd)
  #db.execute(sqlStr,sqlUpd)
  db.commit()

def SqlInsert(fldLst,table):
  sqlFld=list()
  sqlUpd=list()
  ''
  for w in fldLst:
    fld=w.windowTitle()
    try:
      val=w.text()
    except AttributeError:
      val=w.toPlainText()
    if val=='':val=None
    if fld=='id':
      continue
    else:
      sqlFld.append(fld)
      sqlUpd.append(val)
  sqlStr='INSERT INTO '+table+' ('+ ','.join(sqlFld)+') VALUES ('+'?,'*(len(sqlFld)-1)+'?)'

  print(sqlStr,sqlUpd)
  app=qtw.QApplication.instance()
  db=app.mkb.db
  dbc=db.cursor()
  dbc.execute(sqlStr,sqlUpd)
  #db.execute(sqlStr,sqlUpd)
  db.commit()



#Here a clean Main Window implementation.
#QMainWindow has compares to a QWidgets by default dockerbars for toolbars statusbar and menuBar
# #https://www.learnpyqt.com/courses/start/basic-widgets/
# http://zetcode.com/gui/pyqt5/menustoolbars/
def AddMenuAction(widget,parentMenu,txt,func,**kwargs):
  act=qtw.QAction(txt,widget,**kwargs)
  act.triggered.connect(func)
  parentMenu.addAction(act)
  return act


def SqlWidget(txt,qWndType=None):
  if qWndType is None:
    if txt=='id' or txt.startswith('fk'):
      qWndType=qtw.QLabel
    else:
      qWndType=qtw.QLineEdit
  w=qWndType()
  w.setWindowTitle(txt)
  return w

def MsgBox(msg,title="MessageBox",msgInfo=None,detail=None,btn=qtw.QMessageBox.Ok,icon=qtw.QMessageBox.Information):
  dlg=qtw.QMessageBox()
  dlg.setWindowTitle(title)
  dlg.setText(msg)
  dlg.setIcon(icon)
  if msgInfo is not None: dlg.setInformativeText(msgInfo)
  if detail is not None: dlg.setDetailedText(detail)
  dlg.setStandardButtons(btn)
  return dlg.exec_()


class MdiArea(qtw.QMdiArea):

  def __init__(self,background_pixmap,parent=None):

    qtw.QMdiArea.__init__(self,parent)
    self.background_pixmap=background_pixmap
    self.centered=False

  def paintEvent(self,event):

    painter=qtg.QPainter()
    painter.begin(self.viewport())

    if not self.centered:
      painter.drawPixmap(0,0,self.width(),self.height(),self.background_pixmap)
    else:
      painter.fillRect(event.rect(),self.palette().color(qtg.QPalette.Window))
      x=(self.width()-self.display_pixmap.width())/2
      y=(self.height()-self.display_pixmap.height())/2
      painter.drawPixmap(x,y,self.display_pixmap)

    painter.end()

  def resizeEvent(self,event):

    self.display_pixmap=self.background_pixmap.scaled(event.size(),qtc.Qt.KeepAspectRatio)


#class WndSqlTblView(qtw.QDialog):
class WndSqlTblView(qtw.QWidget):

  def __init__(self,title,sql,geometry=(100,100,1700,700)):
    super(WndSqlTblView,self).__init__()
    self.setGeometry(*geometry)
    self.setWindowTitle(title)

    self.mdl=mdl = qtdb.QSqlTableModel()
    if sql[:6].upper()==('SELECT'):
      qry=qtdb.QSqlQuery(sql)
      mdl.setQuery(qry)
    else:
      mdl.setTable(sql)
    mdl.setEditStrategy(qtdb.QSqlTableModel.OnFieldChange)
    mdl.select()
    #mdl.setHeaderData(0,qtc.Qt.Horizontal,'pkPerson')

    self.tbl=view=qtw.QTableView()
    view.setModel(mdl)
    vh=view.verticalHeader()
    vh.setDefaultSectionSize(22)
    #vh.setCascadingSectionResizes(True)
    vh.setMinimumSectionSize(16)
    loV=qtw.QVBoxLayout(self)
    loV.addWidget(view)

    loH=qtw.QHBoxLayout()
    loV.addLayout(loH)

    btn=qtw.QPushButton("Add a row")
    btn.clicked.connect(lambda:mdl.insertRows(mdl.rowCount(),1))
    loH.addWidget(btn)

    btn=qtw.QPushButton("Del a row")
    btn.clicked.connect(lambda:mdl.removeRow(view.currentIndex().row()))
    loH.addWidget(btn)

    btn=qtw.QPushButton("Debug")
    btn.clicked.connect(self.debug)
    loH.addWidget(btn)
    #self.setLayout(loV)
  def debug(self):
    self.tbl


class WndNewInvoices(qtw.QWidget):
  def __init__(self,title,geometry=(100,100,400,500)):
    super(WndNewInvoices,self).__init__()
    self.setGeometry(*geometry)
    self.setWindowTitle(title)

    #https://doc-snapshots.qt.io/qt5-5.15/qformlayout.html
    loV=qtw.QVBoxLayout(self)
    #loH=qtw.QHBoxLayout()
    #loF=qtw.QFormLayout()

    #loV.addLayout(loF)
    #loV.addLayout(loH)


    #Adding sql table for treatments
    self.tbTreatment=tbTrt=qtw.QTableWidget(1,6)#rows cols
    tbTrt.cellDoubleClicked.connect(self.OnTbTrtDblClick)

    tbTrt.setHorizontalHeaderLabels(('id','fkPerson','date','lstName','fstName','comment'))
    hh=tbTrt.horizontalHeader()
    hh.setMinimumSectionSize(20)
    vh=tbTrt.verticalHeader()
    vh.setDefaultSectionSize(20)
    #qTbl.resizeColumnsToContents()
    for i,w in enumerate((40,40,120,130,100,270)):
      tbTrt.setColumnWidth(i,w)
    #qTbl.setFixedWidth(400)
    tbTrt.setMinimumWidth(760)
    tbTrt.setMinimumHeight(600)
    #loF.addRow('Treatments',tbTrt)
    loV.addWidget(tbTrt)
    app=qtw.QApplication.instance()
    self.dbc=dbc=app.mkb.db.cursor()
    self.FillTreatment()

  def FillTreatment(self):
    dbc=self.dbc
    tbTrt=self.tbTreatment
    sqlData=dbc.execute('SELECT trt.id,fkPerson,dtTreatment,lstName,fstName,trt.comment FROM Treatment trt LEFT JOIN Person ps on trt.fkPerson=ps.id  WHERE fkInvoice is NULL ORDER BY ps.id,dtTreatment').fetchall()
    tbTrt.clearContents()
    tbTrt.setRowCount(len(sqlData))
    self.lstKey=lstKey=list()

    for ir,row in enumerate(sqlData):
      key=row[1];lstKey.append(key)
      for ic,data in enumerate(row[0:]):
        if data is None: data=''
        else: data=str(data)
        tw=qtw.QTableWidgetItem(data)
        tw.setFlags(qtc.Qt.ItemIsEnabled|qtc.Qt.ItemIsSelectable)
        #if ic in (1,2: tw.setTextAlignment(qtc.Qt.AlignCenter)
        #tw=qtw.QTableWidgetItem(str(data),type=int)
        #qtc.Qt.ItemIsEnabled
        tbTrt.setItem(ir,ic,tw)
    return




  def OnTbTrtDblClick(self,row,col):
    fkPerson=self.lstKey[row]
    print('Build invoice for fkPerson %d',fkPerson)
    app=qtw.QApplication.instance()
    db=app.mkb.db
    dbc=db.cursor()

    sqlStr='INSERT INTO Invoice (fkPerson,dtInvoice) VALUES (?,?)'
    dbc.execute(sqlStr,(fkPerson,time.strftime('%Y-%m-%d',time.gmtime())))
    #db.commit()
    pkInvoice=dbc.execute('SELECT MAX(id) FROM Invoice').fetchone()[0]

    sqlStr='UPDATE Treatment SET fkInvoice=? WHERE fkInvoice IS NULL AND fkPerson=?'
    dbc.execute(sqlStr,(pkInvoice,fkPerson))
    db.commit()
    app.mkb.report_invoice('iv.id=%d'%pkInvoice)
    self.FillTreatment()
    return


class WndSyncIvcAcc(qtw.QWidget):
  def __init__(self,title,geometry=(100,100,400,500)):
    super(WndSyncIvcAcc,self).__init__()
    self.setGeometry(*geometry)
    self.setWindowTitle(title)

    #https://doc-snapshots.qt.io/qt5-5.15/qformlayout.html
    loV=qtw.QVBoxLayout(self)
    loH=qtw.QHBoxLayout()
    #loF=qtw.QFormLayout()

    #loV.addLayout(loF)
    loV.addLayout(loH)


    app=qtw.QApplication.instance()
    self.dbc=dbc=app.mkb.db.cursor()

    #Adding sql table for Incoive
    lbl=('id','cnt','fkAcc','date','lstName','fstName','sum','comment')
    self.tbIvc=tbIvc=qtw.QTableWidget(1,len(lbl))#rows cols
    tbIvc.setHorizontalHeaderLabels(lbl)
    hh=tbIvc.horizontalHeader()
    hh.setMinimumSectionSize(20)
    vh=tbIvc.verticalHeader()
    vh.setDefaultSectionSize(20)
    #qTbl.resizeColumnsToContents()
    width=(40,40,40,100,100,100,50,50)
    for i,w in enumerate(width):
      tbIvc.setColumnWidth(i,w)
    #qTbl.setFixedWidth(400)
    tbIvc.setMinimumWidth(sum(width)+50)
    tbIvc.setMinimumHeight(600)
    tbIvc.cellDoubleClicked.connect(self.OnTblDblClick)
    #loF.addRow('Treatments',tbTrt)
    loH.addWidget(tbIvc)
    self.FillInvoice()

    #Adding sql table for Account
    lbl=('id','date','refText','sum','fkIvc','sumIvc')
    self.tbAcc=tbAcc=qtw.QTableWidget(1,len(lbl))#rows cols
    tbAcc.setHorizontalHeaderLabels(lbl)
    hh=tbAcc.horizontalHeader()
    hh.setMinimumSectionSize(20)
    vh=tbAcc.verticalHeader()
    vh.setDefaultSectionSize(20)
    #qTbl.resizeColumnsToContents()
    for i,w in enumerate((40,100,240,50,40,50)):
      tbAcc.setColumnWidth(i,w)
    #qTbl.setFixedWidth(400)
    tbAcc.setMinimumWidth(600)
    tbAcc.setMinimumHeight(600)
    tbAcc.cellDoubleClicked.connect(self.OnTblDblClick)
    tbAcc.itemSelectionChanged.connect(self.OnTblSelChanged)

    #loF.addRow('Treatments',tbTrt)
    loH.addWidget(tbAcc)
    self.FillAccout()



  def FillInvoice(self):
    dbc=self.dbc
    tbIvc=self.tbIvc
    sqlData=dbc.execute(\
'''SELECT iv.id,COUNT(tr.id) AS cntTrt,fkAccount,dtInvoice,ivcLstName,ivcFstName,SUM(duration*costPerHour/60) AS cost,iv.comment
   FROM Treatment tr LEFT JOIN Invoice iv  ON tr.fkInvoice=iv.id
   LEFT JOIN Person ps ON iv.fkPerson=ps.id
   WHERE iv.id NOT NULL
   GROUP BY iv.id
   ORDER BY dtInvoice''').fetchall()
    tbIvc.clearContents()
    tbIvc.setRowCount(len(sqlData))
    self.idx2ivc=idx2ivc=list()
    self.acc2ivc=acc2ivc=dict()

    col=qtg.QColor(196,255,196)  #qtg.QColor('yellow')
    for ir,row in enumerate(sqlData):
      pkIvc=row[0];idx2ivc.append(pkIvc)
      fkAcc=row[2]
      try:
        s=acc2ivc[fkAcc]
      except KeyError:
        acc2ivc[fkAcc]=s=[set(),0]
      s[0].add(pkIvc)
      try:
        s[1]+=row[6]
      except TypeError as e:
        print('WndSyncIvcAcc:FillInvoice(1):',e)
      for ic,data in enumerate(row[0:]):
        if data is None: strCell=''
        else: strCell=str(data)
        tw=qtw.QTableWidgetItem(strCell)
        tw.setFlags(qtc.Qt.ItemIsEnabled|qtc.Qt.ItemIsSelectable)
        if row[2] is not None:
          tw.setBackground(col)
        #if ic in (1,2: tw.setTextAlignment(qtc.Qt.AlignCenter)
        #tw=qtw.QTableWidgetItem(str(data),type=int)
        #qtc.Qt.ItemIsEnabled
        tbIvc.setItem(ir,ic,tw)
    tbIvc.setCurrentCell(-1,-1) #set current cell to 'invalid'
    return


  def FillAccout(self):
    dbc=self.dbc
    tbAcc=self.tbAcc
#    sqlData=dbc.execute(\
#'''SELECT ac.id,iv.id,dtEvent,refText,amount FROM Account ac LEFT JOIN Invoice iv ON ac.id=iv.fkAccount
#WHERE amount >0
#ORDER BY dtEvent''').fetchall()

    sqlData=dbc.execute(\
'''SELECT ac.id,dtEvent,refText,amount FROM Account ac WHERE amount >=0 ORDER BY dtEvent''').fetchall()
    tbAcc.clearContents()
    tbAcc.setRowCount(len(sqlData))
    self.idx2acc=idx2acc=list()
    acc2ivc=self.acc2ivc

    col=qtg.QColor(196,255,196)  #qtg.QColor('yellow')

    for ir,row in enumerate(sqlData):
      pkAcc=row[0]
      idx2acc.append(pkAcc)
      try:
        ivcInfo=acc2ivc[pkAcc]
        diff=row[-1]-ivcInfo[1]
        if diff==0:diff=''
        ivcLst=(str(ivcInfo[0]).strip('{}'),diff)
      except KeyError:
        ivcLst=(None,None)
      row=row+ivcLst
      for ic,data in enumerate(row):
        if data is None: strCell=''
        else: strCell=str(data)
        tw=qtw.QTableWidgetItem(strCell)
        tw.setFlags(qtc.Qt.ItemIsEnabled|qtc.Qt.ItemIsSelectable)
        if ivcLst[0] is not None:
          tw.setBackground(col)

        #if ic in (1,2: tw.setTextAlignment(qtc.Qt.AlignCenter)
        #tw=qtw.QTableWidgetItem(str(data),type=int)
        #qtc.Qt.ItemIsEnabled
        tbAcc.setItem(ir,ic,tw)
    tbAcc.setCurrentCell(-1,-1) #set current cell to 'invalid'
    return

  def OnTblDblClick(self,row,col):
    print('OnTblDblClick')
    tbIvc=self.tbIvc
    tbAcc=self.tbAcc
    acc2ivc=self.acc2ivc

    rwIvc=tbIvc.currentRow()
    rwAcc=tbAcc.currentRow()
    if rwIvc<0 or rwAcc<0:
      MsgBox('need selection on invoice and account table')
      return

    pkIvc=self.idx2ivc[rwIvc]
    pkAcc=self.idx2acc[rwAcc]
    app=qtw.QApplication.instance()
    db=app.mkb.db
    dbc=self.dbc
    sqlStr='SELECT fkAccount FROM Invoice WHERE id=?'
    oldVal=dbc.execute(sqlStr,(pkIvc,)).fetchone()[0]
    print(pkIvc,pkAcc,oldVal)
    #acc2ivc[pkAccount]
    try:
      ivcInfo=acc2ivc[pkAcc]
    except KeyError:
      acc2ivc[pkAcc]=ivcInfo=[set(),float(tbAcc.item(rwAcc,3).text())]
      fkAcc=pkAcc

    if oldVal is None:
      fkAcc=pkAcc
      ivcInfo[0].add(pkIvc)
      ivcInfo[1]=ivcInfo[1]-float(tbIvc.item(rwIvc,6).text())
    else:
      try:
        ivcInfo[0].remove(pkIvc)
      except KeyError:
        MsgBox('wrong selection to remove')
        return
      fkAcc=None
      ivcInfo[1]=ivcInfo[1]+float(tbIvc.item(rwIvc,6).text())

    twIvc=tbIvc.item(rwIvc,2)
    if fkAcc is None:
      strIvc=strIvc=''
      col=qtg.QColor(255,255,255)
    else:
      strIvc=str(pkAcc)
      col=qtg.QColor(196,255,196)#qtg.QColor('yellow')
    twIvc.setText(strIvc) #  twAcc.setBackground(col)
    for i in range(tbIvc.columnCount()):
      tbIvc.item(rwIvc,i).setBackground(col)

    if len(ivcInfo[0])==0:
      acc2ivc.pop(pkAcc)
      col=qtg.QColor(255,255,255)
      ivcLst=('','')
    else:
      diff=ivcInfo[1]
      if diff==0:diff=''
      else:diff='%g'%diff
      col=qtg.QColor(196,255,196)
      ivcLst=(str(ivcInfo[0]).strip('{}'),diff)

    tbAcc.item(rwAcc,4).setText(ivcLst[0])
    tbAcc.item(rwAcc,5).setText(ivcLst[1])

    for i in range(tbAcc.columnCount()):
      tbAcc.item(rwAcc,i).setBackground(col)

    #self.FillInvoice()
    sqlStr='UPDATE Invoice SET fkAccount=? WHERE id=?'
    dbc.execute(sqlStr,(fkAcc,pkIvc))
    db.commit()

    return

  def OnTblSelChanged(self):
    print('OnTblSelChanged')
    col=qtg.QColor(32,255,32)  #qtg.QColor('yellow')
    tbIvc=self.tbIvc
    tbAcc=self.tbAcc
    rwAcc=tbAcc.currentRow()

    idx2acc=self.idx2acc
    idx2ivc=self.idx2ivc
    acc2ivc=self.acc2ivc

    #unhighlight
    try:
      lstPkIvc=self.lstIvcHighlight
    except AttributeError:
      pass
    else:
      col=qtg.QColor(192,255,192)  #qtg.QColor('yellow')
      for pkIvc in lstPkIvc:
        idxIvc=idx2ivc.index(pkIvc)
        for i in range(tbIvc.columnCount()):
          tbIvc.item(idxIvc,i).setBackground(col)

    col=qtg.QColor(32,255,32)  #qtg.QColor('yellow')
    pkAcc=idx2acc[rwAcc]
    try:
      self.lstIvcHighlight=lstPkIvc=acc2ivc[pkAcc][0]
    except KeyError:
      pass
    else:
      for pkIvc in lstPkIvc:
        idxIvc=idx2ivc.index(pkIvc)
        for i in range(tbIvc.columnCount()):
          tbIvc.item(idxIvc,i).setBackground(col)


class WndPerson(qtw.QWidget):
  def __init__(self,title,geometry=(100,100,400,500)):
    super(WndPerson,self).__init__()
    self.setGeometry(*geometry)
    self.setWindowTitle(title)

    #https://doc-snapshots.qt.io/qt5-5.15/qformlayout.html
    loV=qtw.QVBoxLayout(self)
    loH=qtw.QHBoxLayout()
    loF=qtw.QFormLayout()

    loV.addLayout(loF)
    loV.addLayout(loH)
    self.cbNaVo=cb=qtw.QComboBox()
    #self.cbNaVoPkPers

    app=qtw.QApplication.instance()
    self.dbc=dbc=app.mkb.db.cursor()
    itemsNaVo=dbc.execute('SELECT id, lstName||" "||fstName FROM Person').fetchall()

    #items=["Java","C#","Python"]
    cb.setEditable(True)
    #v=qtg.QIntValidator(100, 999, self) #QValidator()
    #cb.setValidator(v)
    #cb.InsertPolicy(qtw.QComboBox.NoInsert) does not work
    cmpNaVo=[]
    for pkPers,naVo in itemsNaVo:
      cmpNaVo.append(naVo)
      cb.addItem(naVo,pkPers)
    cb.setCurrentIndex(-1) #by default the text will be the first item. This clears the value
    #cb.model()
    #cb.view()

    cpl=qtw.QCompleter(cmpNaVo)
    #cpl=qtw.QCompleter(cb.model())
    cb.setCompleter(cpl)
    cb.currentIndexChanged.connect(self.OnCbSelChanged)

    loF.addRow('Suche',cb)
    self.fldLst=fldLst=list()

    for desc in ('id','ivcPrefix','ivcLstName','ivcFstName','ivcAddress','ivcAddress1','ivcAddress2','zipCode','city','lstName',
                 'fstName','phone','phone1','phone2','dtBirth','eMail','eMail1','eMail2','ahvNr',
                 ('comment',qtw.QTextEdit) ):
      if type(desc)==str:
        w=SqlWidget(desc);txt=desc
      else:
        w=SqlWidget(*desc);txt=desc[0]
      fldLst.append(w)
      loF.addRow(txt,w)

    for txt,func in (("Treatment",self.OnWndTreatment),("Invoice",self.OnWndInvoice),("Report Treatment",self.OnRptTreatmentProgress),("New",self.OnNew),("Save",self.OnSave)):
      btn=qtw.QPushButton(txt,self)
      if func is not None:
        btn.clicked.connect(func)
      loH.addWidget(btn)

  def OnCbSelChanged(self,i):
    cb=self.cbNaVo
    curData=cb.currentData()
    #print("OnCbSelChanged index",i,"selection changed ",cb.currentIndex(),str(curData),cb.currentText())
    if cb.currentData() is None:
      print("TODO:New Person inserted")
      cb.removeItem(i)
    else:
      dbc=self.dbc
      d=dbc.execute('SELECT * FROM Person WHERE id=%d'%curData).fetchone()
      #print(d)
      for w,d in zip(self.fldLst,d):
        if d is None:
          d=''
        else:
          d=str(d)
        w.setText(d)

  def OnRptTreatmentProgress(self):
    print('OnRptTreatmentProgress')
    app=qtw.QApplication.instance()
    curData=self.cbNaVo.currentData()
    app.mkb.report_therapy_progress('fkPerson=%d'%curData)

  def OnWndTreatment(self):
    cb=self.cbNaVo
    pkPerson=cb.currentData()
    perStr=cb.currentText()
    wnd=WndTreatment('WHERE fkPerson=%d'%pkPerson,'WndTreatment: %s'%perStr,pkPerson)
    wnd.cbTrt.setCurrentIndex(wnd.cbTrt.count()-1)
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()

  def OnWndInvoice(self):
    cb=self.cbNaVo
    pkPerson=cb.currentData()
    perStr=cb.currentText()
    wnd=WndInvoice('WHERE fkPerson=%d'%pkPerson,'WndInvoice: %s'%perStr,pkPerson)
    wnd.cbIvc.setCurrentIndex(wnd.cbIvc.count()-1)
    wnd.fkPerson=pkPerson
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()

  def OnSave(self):
    for w in self.fldLst:
      fld=w.windowTitle()
      if fld!='id': continue
      id=w.text()
    if id=='':
      SqlInsert(self.fldLst,'Person')
    else:
      SqlUpdate(self.fldLst,'Person')

  def OnNew(self):
    self.cbNaVo.setCurrentIndex(-1)
    for w in self.fldLst:
      w.setText('')



class WndTreatment(qtw.QWidget):
  def __init__(self,sqlFilter=None,title='WndTreatment',fkPerson=None,geometry=(100,100,800,500)):
    super(WndTreatment,self).__init__()
    self.setGeometry(*geometry)
    self.sqlFilter=sqlFilter
    self.setWindowTitle(title)

    #https://doc-snapshots.qt.io/qt5-5.15/qformlayout.html
    loV=qtw.QVBoxLayout(self)
    loH=qtw.QHBoxLayout()
    loF=qtw.QFormLayout()

    loV.addLayout(loF)
    loV.addLayout(loH)
    self.cbTrt=cb=qtw.QComboBox()

    app=qtw.QApplication.instance()
    self.dbc=dbc=app.mkb.db.cursor()
    sqlQry='SELECT id, dtTreatment, comment FROM Treatment'
    if sqlFilter is not None: sqlQry+=' '+sqlFilter
    sqlQry+=' ORDER BY fkPerson,dtTreatment'
    itemsTrt=dbc.execute(sqlQry).fetchall()

    cb.setEditable(True)
    cmpTrt=[]
    for pkTrt,datTrt,comment in itemsTrt:
      cmpTrt.append(datTrt)
      cb.addItem(datTrt+' '+str(comment),pkTrt)
    cb.setCurrentIndex(-1) #by default the text will be the first item. This clears the value
    cpl=qtw.QCompleter(cmpTrt)
    cb.setCompleter(cpl)
    cb.setMaxVisibleItems(20)
    cb.currentIndexChanged.connect(self.OnCbSelChanged)

    loF.addRow('Suche',cb)
    self.fldLst=fldLst=list()


    for txt in ('id','fkInvoice','fkPerson','dtTreatment','duration','costPerHour','comment','tarZif'):
      w=SqlWidget(txt)
      if fkPerson is not None and txt=='fkPerson': w.setText(str(fkPerson))
      fldLst.append(w)
      loF.addRow(txt,w)

    txt='document'
    w=SqlWidget(txt,qtw.QTextEdit)
    w.setMinimumWidth(1000) #TODO...
    w.setMaximumHeight(400) #TODO...

    fldLst.append(w)
    loF.addRow(txt,w)

    for txt,func in (("Ext. Edit",self.OnWndTreatment),("New",self.OnNew),("Save",self.OnSave)):#("Rechnungen",self.OnWndInvoice),("Report Treatment",self.OnRptTreatmentProgress)):
      btn=qtw.QPushButton(txt,self)
      if func is not None:
        btn.clicked.connect(func)
      loH.addWidget(btn)


  def OnCbSelChanged(self,i):
    cb=self.cbTrt
    curData=cb.currentData()
    #print("OnCbSelChanged index",i,"selection changed ",cb.currentIndex(),str(curData),cb.currentText())
    if cb.currentData() is None:
      print("TODO:New Person inserted")
      cb.removeItem(i)
    else:
      dbc=self.dbc
      d=dbc.execute('SELECT * FROM Treatment WHERE id=%d'%curData).fetchone()
      #print(d)
      for w,d in zip(self.fldLst,d):
        if d is None:
          d=''
        else:
          d=str(d)
        w.setText(d)

  def OnWndTreatment(self):
    cb=self.cbTrt
    pkBehandlung=cb.currentData()
    wpWnd=wp.MainWindow()
    wpWnd.record_open(pkBehandlung)
    WndChildAdd(wpWnd)

  def OnSave(self):
    for w in self.fldLst:
      fld=w.windowTitle()
      if fld!='id': continue
      id=w.text()
    if id=='':
      SqlInsert(self.fldLst,'Treatment')
    else:
      SqlUpdate(self.fldLst,'Treatment')


  def OnNew(self):
    self.cbTrt.setCurrentIndex(-1)
    for w in self.fldLst:
      if w.windowTitle()=='fkPerson':
        continue
      else:
        w.setText('')

class WndInvoice(qtw.QWidget):
  def __init__(self,sqlFilter=None,title='WndInvoice',fkPerson=None,geometry=(100,100,800,500)):
    super(WndInvoice,self).__init__()
    self.setGeometry(*geometry)
    self.sqlFilter=sqlFilter
    self.setWindowTitle(title)

    #https://doc-snapshots.qt.io/qt5-5.15/qformlayout.html
    loV=qtw.QVBoxLayout(self)
    loH=qtw.QHBoxLayout()
    loF=qtw.QFormLayout()

    loV.addLayout(loF)
    loV.addLayout(loH)
    self.cbIvc=cb=qtw.QComboBox()
    #self.cbNaVoPkPers

    app=qtw.QApplication.instance()
    self.dbc=dbc=app.mkb.db.cursor()
    sqlQry='SELECT id, dtInvoice FROM Invoice'
    if sqlFilter is not None: sqlQry+=' '+sqlFilter
    sqlQry+=' ORDER BY fkPerson,dtInvoice'

    itemsRng=dbc.execute(sqlQry).fetchall()
    cb.setEditable(True)
    cmpRng=[]
    for pkRng, datRng in itemsRng:
      cmpRng.append(datRng)
      cb.addItem(datRng,pkRng)
    cb.setCurrentIndex(-1) #by default the text will be the first item. This clears the value
    #cb.model()
    #cb.view()
    cpl=qtw.QCompleter(cmpRng)
    #cpl=qtw.QCompleter(cb.model())
    cb.setCompleter(cpl)
    cb.currentIndexChanged.connect(self.OnCbSelChanged)

    loF.addRow('Suche',cb)


    self.fldLst=fldLst=list()

    for txt in ('id','fkPerson','fkAccount','tplInvoice','dtInvoice'):
      w=SqlWidget(txt)
      if fkPerson is not None and txt=='fkPerson': w.setText(str(fkPerson))
      fldLst.append(w)
      loF.addRow(txt,w)

    txt='comment'
    w=SqlWidget(txt,qtw.QTextEdit)
    w.setMinimumWidth(200)
    w.setMinimumHeight(40)
    fldLst.append(w)
    loF.addRow(txt,w)

    #Adding sql table for treatments
    self.tbTreatment=tbTrt=qtw.QTableWidget(1,4)#rows cols
    tbTrt.cellDoubleClicked.connect(self.OnTbTrtDblClick)

    tbTrt.setHorizontalHeaderLabels(('date','min','comment','Fr/h',))
    hh=tbTrt.horizontalHeader()
    hh.setMinimumSectionSize(20)
    vh=tbTrt.verticalHeader()
    vh.setDefaultSectionSize(20)
    #qTbl.resizeColumnsToContents()
    for i,w in enumerate((100,40,270,40)):
      tbTrt.setColumnWidth(i,w)
    #qTbl.setFixedWidth(400)
    tbTrt.setMinimumWidth(500)
    loF.addRow('Treatments',tbTrt)

    for txt,func in (("Report Invoice",self.OnRptInvoice),("New",self.OnNew),("Save",self.OnSave)):
      btn=qtw.QPushButton(txt,self)
      if func is not None:
        btn.clicked.connect(func)
      loH.addWidget(btn)

  def OnTbTrtDblClick(self,row,col):
    trtId=self.lstTrtId[row]
    print('Open treatment',trtId)
    wnd=WndTreatment('WHERE id=%d'%trtId,'WndTreatment: trtId==%d'%trtId)
    idx=0
    wnd.cbTrt.setCurrentIndex(idx)
    wnd.OnCbSelChanged(idx)#go to first invoice

    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()
    return

  def OnCbSelChanged(self,i):
    cb=self.cbIvc
    pkInvoice=cb.currentData()
    #print("OnCbSelChanged index",i,"selection changed ",cb.currentIndex(),str(pkInvoice),cb.currentText())
    if pkInvoice is None: return
    dbc=self.dbc
    d=dbc.execute('SELECT * FROM Invoice WHERE id=%d'%pkInvoice).fetchone()
    #print(d)
    for w,d in zip(self.fldLst,d):
      if d is None:
        d=''
      else:
        d=str(d)
      w.setText(d)
    sqlData=dbc.execute('SELECT id,dtTreatment,duration,comment,costPerHour FROM Treatment WHERE fkInvoice=%d;'%pkInvoice).fetchall()
    tbTrt=self.tbTreatment
    tbTrt.clearContents()
    tbTrt.setRowCount(len(sqlData))
    self.lstTrtId=lstTrtId=list()

    for ir,row in enumerate(sqlData):
      id=row[0];lstTrtId.append(id)
      for ic,data in enumerate(row[1:]):
        tw=qtw.QTableWidgetItem(str(data))
        tw.setFlags(qtc.Qt.ItemIsEnabled|qtc.Qt.ItemIsSelectable)
        if ic!=2: tw.setTextAlignment(qtc.Qt.AlignCenter)
        #tw=qtw.QTableWidgetItem(str(data),type=int)
        #qtc.Qt.ItemIsEnabled
        tbTrt.setItem(ir,ic,tw)
    return

  def OnRptInvoice(self):
    print('OnRptInvoice')
    app=qtw.QApplication.instance()
    curData=self.cbIvc.currentData()
    app.mkb.report_invoice('iv.id=%d'%curData)

  def OnSave(self):
    for w in self.fldLst:
      fld=w.windowTitle()
      if fld!='id': continue
      id=w.text()
    if id=='':
      SqlInsert(self.fldLst,'Invoice')
    else:
      SqlUpdate(self.fldLst,'Invoice')

  def OnNew(self):
    self.cbIvc.setCurrentIndex(-1)
    for w in self.fldLst:
      if w.windowTitle()=='fkPerson':
        continue
      else:
        w.setText('')
    tbTrt=self.tbTreatment
    tbTrt.clearContents();tbTrt.setRowCount(1)

class WndMain(qtw.QMainWindow):

  def __init__(self):
    super(WndMain,self).__init__()
    self.setGeometry(150,150,1300,900)
    self.setWindowTitle("MoKaBu")
    self.setWindowIcon(qtg.QIcon('logo_monika.ico'))
    #self.setWindowIcon(qtw.QIcon('pythonlogo.png'))
    #self.mdi=qtw.QMdiArea()
    self.mdi=mdi=MdiArea(qtg.QPixmap('Logo_Monika.png'));mdi.centered=True

    self.setCentralWidget(self.mdi)

    mainMenu=self.menuBar()
    self.statusBar()
    mnFile=mainMenu.addMenu('&File')

    act=AddMenuAction(self,mnFile,"Quit",self.OnQuit)
    mnEdit=mainMenu.addMenu('&Edit')
    act=AddMenuAction(self,mnEdit,"Table Person",self.OnTblPerson,shortcut="Ctrl+Shift+A")
    act=AddMenuAction(self,mnEdit,"Table Treatment",self.OnTblTreatment,shortcut="Ctrl+Shift+S")
    act=AddMenuAction(self,mnEdit,"Table Invoice",self.OnTblInvoice,shortcut="Ctrl+Shift+D")
    act=AddMenuAction(self,mnEdit,"Table Account",self.OnTblAccount,shortcut="Ctrl+Shift+F")
    act=AddMenuAction(self,mnEdit,"Person",self.OnWndPerson,shortcut="Ctrl+A")
    act=AddMenuAction(self,mnEdit,"New Assisted Invoices",self.OnWndNewInvoices)
    act=AddMenuAction(self,mnEdit,"Sync Invoice->Account",self.OnWndSyncIvcAcc)
    act=AddMenuAction(self,mnEdit,"OnQryTreatment",self.OnQryTreatment)
    act=AddMenuAction(self,mnEdit,"OnQryInvoice",self.OnQryInvoice)
    act=AddMenuAction(self,mnEdit,"OnQryNewInvoice",self.OnQryNewInvoice)
    mnRpt=mainMenu.addMenu('&Report')
    act=AddMenuAction(self,mnRpt,"Invoices",self.OnRepInvoices)
    act=AddMenuAction(self,mnRpt,"Therapy Progress",self.OnRepTherapyProgress)

  def closeEvent(self, event):
    print('closeEvent')
    app=qtw.QApplication.instance()
    #app.wndTop.clear()  #free and close all instances
    #if len(app.wndTop)>0:
    #  print('close cild windows first',app.wndTop)
    #  event.ignore()
    sys.exit()

  def OnQuit(self):
    print("whooaaaa so custom!!!")
    sys.exit()

  def OnTblPerson(self):
    print("OnTblPerson")
    wnd=WndSqlTblView('TblClients:','Person')
    #wnd=WndSqlTblView('TblClients:','SELECT * FROM Person WHERE id<10')
    #wnd=WndSqlTblView('TblClients:',
    #                  'SELECT RngAnrede,RngNachname,RngVorname,RngAdresse,RngAdresse1,PLZ,Ort FROM tblPerson ORDER BY RngNachname,RngVorname',
    #                  geometry=(100,100,1200,700))
    #wnd.tbl.setColumnWidth(2,200)
    for i in range(wnd.mdl.columnCount()):
      wnd.tbl.resizeColumnToContents(i)
    WndChildAdd(wnd)
  def OnTblTreatment(self):
    print("aOnTblTreatment")
    wnd=WndSqlTblView('TblTreatments:','Treatment',geometry=(100,100,1200,700))
    for i in range(wnd.mdl.columnCount()):
      wnd.tbl.resizeColumnToContents(i)
    WndChildAdd(wnd)

  def OnTblInvoice(self):
    print("OnTblInvoice")
    wnd=WndSqlTblView('TblInvoices:','Invoice',geometry=(100,100,600,700))
    for i in range(wnd.mdl.columnCount()):
      wnd.tbl.resizeColumnToContents(i)
    WndChildAdd(wnd)

  def OnTblAccount(self):
    print("OnTblAccount")
    wnd=WndSqlTblView('TblAccount:','Account',geometry=(100,100,600,700))
    for i in range(wnd.mdl.columnCount()):
      wnd.tbl.resizeColumnToContents(i)
    WndChildAdd(wnd)

  def OnWndPerson(self):
    print("OnWndPerson")
    wnd=WndPerson('QryClient')
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.mdi.addSubWindow(sub)
    sub.show()

  def OnWndNewInvoices(self):
    print("OnWndNewInvoices")
    wnd=WndNewInvoices('NewInvoices')
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.mdi.addSubWindow(sub)
    sub.show()

  def OnWndSyncIvcAcc(self):
    print("OnWndSyncIvcAcc")
    wnd=WndSyncIvcAcc('WndSyncIvcAcc')
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.mdi.addSubWindow(sub)
    sub.show()

  def OnQryTreatment(self):
    print("OnQryTreatment")
    wnd=qtw.QWidget();wnd.setWindowTitle("WndQryTreatment")
    WndChildAdd(wnd)

  def OnQryInvoice(self):
    print("OnQryInvoice")
    wnd=qtw.QWidget();wnd.setWindowTitle("WndQryInvoice")

    WndChildAdd(wnd)

  def OnQryNewInvoice(self):
    print("OnQryNewInvoice")
    wnd=qtw.QWidget();wnd.setWindowTitle("WndQryNewInvoice")
    WndChildAdd(wnd)

  def OnRepInvoices(self):
    print("OnRepInvoices")
    app=qtw.QApplication.instance()
    app.mkb.report_invoice()

  def OnRepTherapyProgress(self):
    print("OnRepTherapyProgress")
    app=qtw.QApplication.instance()
    app.mkb.report_therapy_progress()


#https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlRelationalTableModel.html
#https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlTableModel.html
#TODO:
# quite generic QSqlTableModel UI QSqlRelationalTableModel


if __name__=='__main__':

  MainApp(None)
