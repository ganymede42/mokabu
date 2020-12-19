#!/usr/bin/python3
#https://www.tutorialspoint.com/pyqt/pyqt_hello_world.htm
#https://github.com/tpgit/MDIImageViewer usefull sample application
import sys,time,os
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtSql as qtdb
import mokabu
import report
import wordprocessor as wp
import traceback
import sqlite3 as lite

def excepthook(exc_type,exc_value,exc_tb):
  tb="".join(traceback.format_exception(exc_type,exc_value,exc_tb))
  print("error catched!:")
  print("error message:\n",tb)
  msg=exc_type.__name__+': '+str(exc_value)
  MsgBox(msg,title="Not handeled Error"+' '*100,msgInfo=None,detail=tb,btn=qtw.QMessageBox.Ok,icon=qtw.QMessageBox.Critical)


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
  if dbg&16:
    mainWnd.OnWndSyncIvcAcc()


  #wpWnd=wp.MainWindow()
  #wpWnd.record_open(1)
  #WndChildAdd(wpWnd)
  #app.topLevelWindows()
  #app.topLevelWidgets()
  sys.excepthook=excepthook
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
  sqlStr='SELECT MAX(id) FROM '+table
  newid=dbc.execute(sqlStr).fetchone()
  return newid[0]



#Here a clean Main Window implementation.
#QMainWindow has compares to a QWidgets by default dockerbars for toolbars statusbar and menuBar
# #https://www.learnpyqt.com/courses/start/basic-widgets/
# http://zetcode.com/gui/pyqt5/menustoolbars/
def AddMenuAction(widget,parentMenu,txt,func,**kwargs):
  act=qtw.QAction(txt,widget,**kwargs)
  act.triggered.connect(func)
  parentMenu.addAction(act)
  return act

def MsgBox(msg,title="MessageBox",msgInfo=None,detail=None,btn=qtw.QMessageBox.Ok,icon=qtw.QMessageBox.Information,defBtn=None):
  dlg=qtw.QMessageBox()
  dlg.setWindowTitle(title)
  dlg.setText(msg)
  dlg.setIcon(icon)
  dlg.setStandardButtons(btn)
  if msgInfo is not None: dlg.setInformativeText(msgInfo)
  if detail is not None: dlg.setDetailedText(detail)
  if defBtn is not None: dlg.setDefaultButton(defBtn)
  return dlg.exec_()

class QDateEdit(qtw.QLineEdit):
  """docstring for QDateEdit"""
  def __init__(self):
    super(QDateEdit, self).__init__()

  def setText(self,txt):
    if txt not in (None,''):
      try:
        txt=time.strftime('%d.%m.%y',time.strptime(txt,'%Y-%m-%d'))
      except ValueError as e:
        print('QDateEdit::setText',e)
    qtw.QLineEdit.setText(self,txt)

  def text(self):
    txt=qtw.QLineEdit.text(self)
    if txt in (None,''): return txt
    for fmt in ("%d.%m.%y","%d.%m.%Y",'%Y-%m-%d'):
      try:
        dateStruct=time.strptime(txt,fmt)
      except ValueError:
        continue
      break
    try:
      #dateEpoch=int(time.mktime(dateStruct)) # conver struct to second since 1.1.1970
      txt=time.strftime('%Y-%m-%d',dateStruct)
      #dateEpoch=int(time.strftime('%Y%m%d',dateStruct))
    except UnboundLocalError as e:
      raise UserWarning(str(txt))
    return txt

class WndSqlBase(qtw.QWidget):
  def __init__(self,geometry=(100,100,400,500)):
    super(WndSqlBase,self).__init__()
    self._changed=False

  class Validator(qtg.QValidator):
    'Validator for wndSqlBase Combobox class tht changes to a new record'

    def __init__(self,wndSqlBase):
      super(WndSqlBase.Validator,self).__init__()
      self.wndSqlBase=wndSqlBase

    #def validate(self,*args,**kwargs):
    #  print(args,kwargs)

    def validate(self,text,pos):
      self.wndSqlBase.lastCbIdx=pos
      print('Validator.validate',text,pos)
      return (qtg.QValidator.Acceptable,text,pos)

  def SqlWidget(self,txt,qWndType=None,onTxtChanged=None):
    if qWndType is None:
      if txt=='id' or txt.startswith('fk'):
        qWndType=qtw.QLabel
      else:
        qWndType=qtw.QLineEdit
      if txt.startswith('dt'):
        qWndType=QDateEdit

    w=qWndType()
    if  qWndType!=qtw.QLabel:
      w.textChanged.connect(self.OnTxtChanged)
    w.setWindowTitle(txt)
    return w

  def closeEvent(self, event):
      print("User has clicked the red x on the main window")
      if self.SwitchRecord()==True:
        event.accept()
      else:
        event.ignore()

  def OnTxtChanged(self):
    self.SetChanged(True)
    print('OnTxtChanged',self)

  def SwitchRecord(self):
    #when close or change to new record ask to save
    print('SwitchRecord',self._changed)
    if self._changed is False: return True
    res=MsgBox('save changes to actual record?',
               btn=qtw.QMessageBox.Yes|qtw.QMessageBox.No|qtw.QMessageBox.Cancel,
               icon=qtw.QMessageBox.Question)
    print('pressed',res)
    if res==qtw.QMessageBox.Yes:
      self.OnSave()
    elif res==qtw.QMessageBox.No:
      self.SetChanged(False)
    elif res==qtw.QMessageBox.Cancel:
      return False
    return True

  def SetChanged(self,chg):
    assert(type(chg)==bool)
    if self._changed!=chg:
      self._changed=chg
      title=self.windowTitle()
      print(title)
      if chg:
        self.setWindowTitle(title+'*')
      else:
        self.setWindowTitle(title[:-1])


  def OnSave(self):
    raise BaseException('overload this function')

#  def OnNew(self):
#    raise BaseException('overload this function')


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

#class WndSqlTblView(qtw.QDialog):
class WndQuickSelect(qtw.QTableWidget):
  def __init__(self,title='WndQuickSelect',geometry=(100,100,1700,700)):
    super(WndQuickSelect,self).__init__()
    self.setGeometry(*geometry)
    self.setWindowTitle(title)
    self.filtMode=0

    lbl=('Person','Behandlung','Rechnung','dur','comment')

    self.setColumnCount(len(lbl))
    #tbIvc.setRowCount(len(sqlData))

    self.setHorizontalHeaderLabels(lbl)
    hh=self.horizontalHeader()
    hh.setMinimumSectionSize(20)
    vh=self.verticalHeader()
    vh.setDefaultSectionSize(20)
    #qTbl.resizeColumnsToContents()
    width=(200,100,120,30,300)
    for i,w in enumerate(width):
      self.setColumnWidth(i,w)
    #qTbl.setFixedWidth(400)
    self.setMinimumWidth(sum(width)+50)
    self.setMinimumHeight(600)
    #self.cellDoubleClicked.connect(self.OnTblDblClick)
    #loF.addRow('Treatments',tbTrt)
    self.populate()
    self.cellDoubleClicked.connect(self.OnDblClick)

  def populate(self):
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    if self.filtMode==0:
      sqlCmd=\
      '''SELECT tr.fkPerson,tr.id,tr.fkInvoice,ps.fstName||' '||ps.lstName as fstLst,tr.dtTreatment,iv.dtInvoice,tr.duration,tr.comment
             FROM treatment tr
             LEFT JOIN Person ps on tr.fkPerson=ps.id
             LEFT JOIN Invoice iv on tr.fkInvoice=iv.id
             ORDER BY tr.dtTreatment DESC'''
    elif self.filtMode==1:
      sqlCmd=\
      '''SELECT tr.fkPerson,tr.id,tr.fkInvoice,ps.fstName||' '||ps.lstName as fstLst,tr.dtTreatment,iv.dtInvoice,tr.duration,tr.comment
             FROM treatment tr
             LEFT JOIN Person ps on tr.fkPerson=ps.id
             LEFT JOIN Invoice iv on tr.fkInvoice=iv.id
              WHERE tr.fkInvoice is NULL
              ORDER BY tr.fkPerson,tr.dtTreatment DESC'''
    else:
      sqlCmd=\
      '''SELECT tr.fkPerson,tr.id,tr.fkInvoice,ps.fstName||' '||ps.lstName as fstLst,tr.dtTreatment,iv.dtInvoice,tr.duration,tr.comment
             FROM treatment tr
             LEFT JOIN Person ps on tr.fkPerson=ps.id
             LEFT JOIN Invoice iv on tr.fkInvoice=iv.id
              WHERE tr.fkInvoice==-1
              ORDER BY tr.dtTreatment DESC'''

    sqlData=dbc.execute(sqlCmd).fetchall()
    self.clearContents()
    self.setRowCount(len(sqlData))

    self.idx2ref=idx2ref=list()
    for ir,row in enumerate(sqlData):
      pkTrt,fkPrs,fkIvc=row[0:3]
      idx2ref.append(row[0:3])
      for ic,data in enumerate(row[3:]):
        if ic==1: # treatment
          strCell=report.dateconvert(data,1)
        elif ic==2: # invoice
          if fkIvc is None: strCell='open'
          elif fkIvc==-1: strCell='free of charge'
          else:
            strCell=report.dateconvert(data,1)
        else:
          strCell=str(data)
        tw=qtw.QTableWidgetItem(strCell)
        tw.setFlags(qtc.Qt.ItemIsEnabled|qtc.Qt.ItemIsSelectable)
        #if row[2] is not None:
        #  tw.setBackground(col)
        self.setItem(ir,ic,tw)
    self.setCurrentCell(-1,-1) #set current cell to 'invalid'

  def OnDblClick(self,row,col):
    print('OnTblDblClick')
    idx2ref=self.idx2ref
    fkPrs,pkTrt,fkIvc=idx2ref[row]
    if col==0:
      #wnd=WndPerson('WHERE id=%d'%pkTrt,'WndTreatment: trtId==%d'%pkTrt,fkPrs)
      wnd=WndPerson(pkPerson=fkPrs)
    elif col==1:
      wnd=WndTreatment(fkPerson=fkPrs,pkTreatment=pkTrt)
    elif col==2:
      if fkIvc in (None,-1):
        MsgBox('no invoice for this treatment')
        return
      else:
        wnd=WndInvoice(fkPerson=fkPrs,pkInvoice=fkIvc)
    else:
      return

    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()

  def contextMenuEvent(self, event):
    item=self.itemAt(event.pos())
    idx=self.indexFromItem(item)
    idx2ref=self.idx2ref
    fkPrs,pkTrt,fkIvc=idx2ref[idx.row()]

    ctxMn=qtw.QMenu(self)
    actFiltAll=ctxMn.addAction('filter: all treatments')
    actFiltOpen=ctxMn.addAction('filter: open treatments')
    actFiltFree=ctxMn.addAction('filter: free of charge')
    #if idx.column()==2:
    if fkIvc is None:
      ctxMn.addSeparator()
      actIvcFree=ctxMn.addAction('set to: free of charge')
      actIvcGen=ctxMn.addAction('generate invoice')
    elif fkIvc==-1:
      ctxMn.addSeparator()
      actIvcCharge=ctxMn.addAction('set to: invoice')

    action=ctxMn.exec_(self.mapToGlobal(event.pos()))
    if not action:
      return
    if action==actFiltAll:
      self.filtMode=0
    elif action==actFiltOpen:
      self.filtMode=1
    elif action==actFiltFree:
      self.filtMode=2
    elif fkIvc is None:
      if action==actIvcFree:
        self.SetPkTreatmentFkInvoice(pkTrt,-1)
      elif action==actIvcGen:
        res=MsgBox('Generate new invoice for this person?',
                   btn=qtw.QMessageBox.Ok|qtw.QMessageBox.Cancel,
                   icon=qtw.QMessageBox.Question)
        if res==qtw.QMessageBox.Ok:
          self.GenNewInvoice(fkPrs)
    elif fkIvc==-1:
      if action==actIvcCharge:
        self.SetPkTreatmentFkInvoice(pkTrt,None)
    self.populate()

  def SetPkTreatmentFkInvoice(self,pkTrt,fkIvc):
    db=qtw.QApplication.instance().mkb.db
    dbc=db.cursor()
    dbc.execute('UPDATE Treatment SET fkInvoice=? WHERE id=?',(fkIvc,pkTrt))
    db.commit()

  def GenNewInvoice(self,fkPerson):
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
    app.mkb.report_invoice(pkInvoice=pkInvoice)
    self.populate()
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

    #Adding sql table for Incoive
    lbl=('id','fkAcc','Datum','cnt','sum','Person','Rechnung','comment')
    self.tbIvc=tbIvc=qtw.QTableWidget(1,len(lbl))#rows cols
    tbIvc.setHorizontalHeaderLabels(lbl)
    hh=tbIvc.horizontalHeader()
    hh.setMinimumSectionSize(20)
    vh=tbIvc.verticalHeader()
    vh.setDefaultSectionSize(20)
    #qTbl.resizeColumnsToContents()
    width=(40,40,70,30,45,240,10,140)
    for i,w in enumerate(width):
      tbIvc.setColumnWidth(i,w)
    #qTbl.setFixedWidth(400)
    tbIvc.setMinimumWidth(sum(width)+30)
    tbIvc.setMinimumHeight(600)
    #tbIvc.setSelectionMode(qtw.QAbstractItemView.SingleSelection)
    tbIvc.itemSelectionChanged.connect(self.OnTblIvcSelChanged)
    tbIvc.cellDoubleClicked.connect(self.OnTblIvcDblClick)
    #loF.addRow('Treatments',tbTrt)
    loH.addWidget(tbIvc)
    self.FillInvoice()

    #Adding sql table for Account
    #lbl=('id','date','refText','sum','fkIvc','sumIvc')
    lbl=('id','fkIvc','Datum','sum','diff','refText')
    self.tbAcc=tbAcc=qtw.QTableWidget(1,len(lbl))#rows cols
    tbAcc.setHorizontalHeaderLabels(lbl)
    hh=tbAcc.horizontalHeader()
    hh.setMinimumSectionSize(20)
    vh=tbAcc.verticalHeader()
    vh.setDefaultSectionSize(20)
    #qTbl.resizeColumnsToContents()
    width=(40,40,70,50,45,280)
    for i,w in enumerate(width):
      tbAcc.setColumnWidth(i,w)
    #qTbl.setFixedWidth(400)
    tbAcc.setMinimumWidth(600)
    tbAcc.setMinimumHeight(600)
    #tbAcc.cellDoubleClicked.connect(self.OnTblDblClick)
    tbAcc.itemSelectionChanged.connect(self.OnTblAccSelChanged)

    #loF.addRow('Treatments',tbTrt)
    loH.addWidget(tbAcc)
    self.FillAccout()



  def FillInvoice(self):
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    tbIvc=self.tbIvc
    sqlData=dbc.execute(\
    '''SELECT iv.id,COUNT(tr.id) AS cntTrt,fkAccount,dtInvoice,ivcLstName,ivcFstName,SUM(duration*costPerHour/60) AS cost,iv.comment,lstName,fstName
       FROM Treatment tr LEFT JOIN Invoice iv  ON tr.fkInvoice=iv.id
       LEFT JOIN Person ps ON iv.fkPerson=ps.id
       WHERE iv.id NOT NULL
       GROUP BY iv.id
       ORDER BY dtInvoice''').fetchall()
    tbIvc.clearContents()
    tbIvc.setRowCount(len(sqlData))
    self.idx2ivc=idx2ivc=list()
    self.acc2ivc=acc2ivc=dict()
#idx2ivc table index to invoice id
#idx2acc table index to account id
#acc2ivc account id to set of invoices

# 0 ivcId
# 1 cntTrt
# 2 fkAccount
# 3 dtInvoice
# 4 ivcLstName
# 5 ivcFstName
# 6 cost
# 7 iv.comment
# 8 lstName
# 9 fstName
    col=qtg.QColor(196,255,196)  #qtg.QColor('yellow')
    for ir,row in enumerate(sqlData):
      pkIvc=row[0];idx2ivc.append(pkIvc)
      cntTrt=row[1]
      fkAcc=row[2]
      dtIvc=report.dateconvert(row[3],1)
      ivcName=' '.join(filter(None,row[4:6]))
      cost=row[6]
      ivcCmt=row[7]
      prsName=' '.join(filter(None,row[8:10]))
      data=(pkIvc,fkAcc,dtIvc,cntTrt,cost,prsName,ivcName,ivcCmt)
      try:
        s=acc2ivc[fkAcc]
      except KeyError:
        acc2ivc[fkAcc]=s=[set(),0]
      s[0].add(pkIvc)
      try:
        s[1]+=row[6]
      except TypeError as e:
        print('WndSyncIvcAcc:FillInvoice(1):',e)
      for ic,data in enumerate(data):
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
    dbc=qtw.QApplication.instance().mkb.db.cursor()
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
    lbl=('id','fkIvc','Datum','sum','diff','refText')

    for ir,row in enumerate(sqlData):
      pkAcc=row[0]
      dtEvent=report.dateconvert(row[1],1)
      amount=row[3]
      refText=row[2]
      idx2acc.append(pkAcc)
      try:
        ivcInfo=acc2ivc[pkAcc]
        diff=amount-ivcInfo[1]
        if diff==0:diff=''
        fkIvc=str(ivcInfo[0]).strip('{}')
      except KeyError:
        fkIvc=diff=None
      row=(pkAcc,fkIvc,dtEvent,amount,diff,refText)
      for ic,data in enumerate(row):
        if data is None: strCell=''
        else: strCell=str(data)
        tw=qtw.QTableWidgetItem(strCell)
        tw.setFlags(qtc.Qt.ItemIsEnabled|qtc.Qt.ItemIsSelectable)
        if fkIvc is not None:
          tw.setBackground(col)

        #if ic in (1,2: tw.setTextAlignment(qtc.Qt.AlignCenter)
        #tw=qtw.QTableWidgetItem(str(data),type=int)
        #qtc.Qt.ItemIsEnabled
        tbAcc.setItem(ir,ic,tw)
    tbAcc.setCurrentCell(-1,-1) #set current cell to 'invalid'
    return

  def OnTblIvcSelChanged(self):
    print('OnTblIvcSelChanged')

  def OnTblIvcDblClick(self,row,col):
    print('OnTblIvcDblClick')
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    idx2ivc=self.idx2ivc
    fkIvc=idx2ivc[row]
    sqlData=dbc.execute('SELECT iv.fkPerson FROM Invoice iv WHERE id=?',(fkIvc,)).fetchone()
    fkPrs=sqlData[0]
    if col in (5,6):
      wnd=WndPerson(pkPerson=fkPrs)
    else:
      wnd=WndInvoice(fkPerson=fkPrs,pkInvoice=fkIvc)
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()

  def OnTblAccSelChanged(self):
    print('OnTblAccSelChanged')
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

    #highlight
    col=qtg.QColor(32,255,32)  #qtg.QColor('yellow')
    pkAcc=idx2acc[rwAcc]
    try:
      self.lstIvcHighlight=lstPkIvc=acc2ivc[pkAcc][0]
    except KeyError:
      pass
    else:
      for pkIvc in lstPkIvc:
        idxIvc=idx2ivc.index(pkIvc)
        item = self.tbIvc.item(idxIvc, 0)
        #self.tbIvc.scrollToItem(item, hint=qtg.QAbstractItemView.PositionAtCenter)
        self.tbIvc.scrollToItem(item)
        for i in range(tbIvc.columnCount()):
          tbIvc.item(idxIvc,i).setBackground(col)


  def LinkAccIvc(self,link=True):
    print('OnLinkAccIvc')
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
    db=qtw.QApplication.instance().mkb.db
    dbc=db.cursor()
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

  def contextMenuEvent(self, event):
    pos=event.pos()
    cld=self.childAt(pos)
    if not cld: return
    tbl=cld.parent()
    if tbl==self.tbIvc:
      mode=0
    elif tbl==self.tbAcc:
      mode=1
    else:
      return

    pos=pos-tbl.pos()
    item=tbl.itemAt(pos)
    idx=tbl.indexFromItem(item)

    ctxMn=qtw.QMenu(self)
    actFiltAll=ctxMn.addAction('filter: all invoices')
    actFiltOpen=ctxMn.addAction('filter: open invoices')

    actFiltUnLink=actFiltLink=actFiltAlign=None

    if mode==0:
      #idx2acc=self.idx2acc
      idx2ivc=self.idx2ivc
      #acc2ivc=self.acc2ivc
      row=idx.row()-1
      fkIvc=idx2ivc[row]
      db=qtw.QApplication.instance().mkb.db
      dbc=db.cursor()
      sqlData=dbc.execute('SELECT fkPerson,fkAccount FROM Invoice iv WHERE id=?',(fkIvc,)).fetchone()
      fkPrs,fkAcc=sqlData
      actFiltAlign=ctxMn.addAction('align invoice to account')
      rwAcc=self.tbAcc.currentRow()
      if rwAcc>0:
        pkAcc=self.idx2acc[rwAcc]
        actFiltLink=ctxMn.addAction('link invoice to account %d'%pkAcc)
      if fkAcc is not None:
        actFiltUnLink=ctxMn.addAction('unlink invoice from account %d'%fkAcc)
      pass
    else: # tb==1
      #idx2ref=self.idx2refAcc
      #fkPrs,pkTrt,fkIvc=idx2ref[idx.row()]
      pass

    #TODO: implement these functions
    #align invoice to account is done by selecting an invoice
    # by selecting an account if there are mote than one invoice align first to top
    #doubleclick on invoice opens the invoice
    #doubleclick on person opens the person


    #if idx.column()==2:
    #if fkIvc is None:
    #  ctxMn.addSeparator()
    #  actIvcFree=ctxMn.addAction('set to: free of charge')
    #  actIvcGen=ctxMn.addAction('generate invoice')
    #elif fkIvc==-1:
    #  ctxMn.addSeparator()
    #  actIvcCharge=ctxMn.addAction('set to: invoice')

    action=ctxMn.exec_(self.mapToGlobal(event.pos()))
    if not action:
      return

    if action==actFiltUnLink:
      self.LinkAccIvc(True)
    elif action==actFiltLink:
      self.LinkAccIvc(False)
    #elif action==:
    #elif action==:
    #  self.filtMode=0
    #elif action==actFiltOpen:
    #  self.filtMode=1
    #elif action==actFiltFree:
    #  self.filtMode=2
    #elif fkIvc is None:
    #  if action==actIvcFree:
    #    self.SetPkTreatmentFkInvoice(pkTrt,-1)
    #  elif action==actIvcGen:
    #    res=MsgBox('Generate new invoice for this person?',
     #              btn=qtw.QMessageBox.Ok|qtw.QMessageBox.Cancel,
    #               icon=qtw.QMessageBox.Question)
    #    if res==qtw.QMessageBox.Ok:
    #      self.GenNewInvoice(fkPrs)
    #elif fkIvc==-1:
    #  if action==actIvcCharge:
    #    self.SetPkTreatmentFkInvoice(pkTrt,None)
    #    self.OnLinkAccIvc(fkIvc,link=true/false)
    #self.populate()

class WndPerson(WndSqlBase):
  def __init__(self,pkPerson=None,geometry=(100,100,400,500)):
    super(WndPerson,self).__init__(geometry)
    title='WndPerson'
    self.setWindowTitle(title)
    #https://doc-snapshots.qt.io/qt5-5.15/qformlayout.html
    loV=qtw.QVBoxLayout(self)
    loH=qtw.QHBoxLayout()
    loF=qtw.QFormLayout()

    loV.addLayout(loF)
    loV.addLayout(loH)
    self.cbNaVo=cb=qtw.QComboBox()
    cb.setEditable(True)
    cb.activated.connect(self.OnCbSelChanged)

    loF.addRow('Suche',cb)
    self.fldLst=fldLst=list()

    fld2lbl={
      'ivcPrefix':'Anrede',
      'ivcLstName':'Rng Name',
      'ivcFstName':'Rng Vorname',
      'ivcAddress':'Rng Adresse',
      'ivcAddress1':'Rng Adresse1',
      'ivcAddress2':'Rng Adresse2',
      'zipCode':'PLZ',
      'city':'Ort',
      'lstName':'Patient Name',
      'fstName':'Patient Vorname',
      'phone': 'Telefon',
      'phone1':'Telefon1',
      'phone2':'Telefon2',
      'dtBirth':'Geburtsdatum',
      'ahvNr':'AHV-Nr.',
      'comment':'Bemerkung'
    }
    for desc in ('id','ivcPrefix','ivcLstName','ivcFstName','ivcAddress','ivcAddress1','ivcAddress2','zipCode','city','lstName',
                 'fstName','phone','phone1','phone2','dtBirth','eMail','eMail1','eMail2','ahvNr',
                 ('comment',qtw.QTextEdit) ):
      if type(desc)==str:
        w=self.SqlWidget(desc);fld=desc
      else:
        w=self.SqlWidget(*desc);fld=desc[0]
      fldLst.append(w)
      lbl=fld2lbl.get(fld,fld)
      loF.addRow(lbl,w)

    self.CbNaVoPopulate(pkPerson)

    for txt,func in (("Treatment",self.OnWndTreatment),("Invoice",self.OnWndInvoice),("Report Treatment",self.OnRptTreatmentProgress),("Delete",self.OnDelete),("New",self.OnNew),("Save",self.OnSave)):
      btn=qtw.QPushButton(txt,self)
      if func is not None:
        btn.clicked.connect(func)
      loH.addWidget(btn)

  def CbNaVoPopulate(self,pkPerson=None):
    cb=self.cbNaVo
    cb.clear()
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    itemsNaVo=dbc.execute('SELECT id, lstName||" "||fstName FROM Person ORDER BY lstName,fstName').fetchall()

    cmpNaVo=[]
    setIdx=-1
    for pkPers,naVo in itemsNaVo:
      cmpNaVo.append(naVo)
      cb.addItem(naVo,pkPers)
      if pkPers==pkPerson:
        setIdx=cb.count()-1
    cb.setCurrentIndex(setIdx) #by default the text will be the first item. This clears the value
    if pkPerson:
      if setIdx==-1:
        MsgBox('pkPerson %d not found'%pkPerson,icon=qtw.QMessageBox.Warning)
      else:
        self.OnCbSelChanged(setIdx)

    cpl=qtw.QCompleter(cmpNaVo)
    cpl.setCaseSensitivity(qtc.Qt.CaseInsensitive)
    cpl.setFilterMode(qtc.Qt.MatchContains)
    cb.setCompleter(cpl)
    #cb.setValidator(WndSqlBase.Validator(self))

  def OnCbSelChanged(self,i):
    cb=self.cbNaVo
    curData=cb.currentData()
    #print("OnCbSelChanged index",i,"selection changed ",cb.currentIndex(),str(curData),cb.currentText())
    print('OnCbSelChanged',i,curData,cb.currentIndex())
    if not self.SwitchRecord():
      cb.setCurrentText('')
      return
    if cb.currentData() is None:
      print("TODO:New Person inserted")
      cb.removeItem(i)
    else:
      dbc=qtw.QApplication.instance().mkb.db.cursor()
      d=dbc.execute('SELECT * FROM Person WHERE id=%d'%curData).fetchone()
      #print(d)
      for w,d in zip(self.fldLst,d):
        if d is None:
          d=''
        else:
          d=str(d)
        w.setText(d)
      self.SetChanged(False)

  def OnRptTreatmentProgress(self):
    print('OnRptTreatmentProgress')
    app=qtw.QApplication.instance()
    pkPerson=self.cbNaVo.currentData()
    if pkPerson is None:
      MsgBox('No selected person')
      return
    app.mkb.report_therapy_progress(pkPerson=pkPerson)

  def OnWndTreatment(self):
    cb=self.cbNaVo
    pkPerson=cb.currentData()
    if pkPerson is None:
      MsgBox('No selected person')
      return
    wnd=WndTreatment(fkPerson=pkPerson)
    idx=wnd.cbTrt.count()-1
    wnd.cbTrt.setCurrentIndex(idx)
    wnd.OnCbSelChanged(idx)
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle(wnd.windowTitle())
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()

  def OnWndInvoice(self):
    cb=self.cbNaVo
    pkPerson=cb.currentData()
    if pkPerson is None:
      MsgBox('No selected person')
      return
    perStr=cb.currentText()
    wnd=WndInvoice(fkPerson=pkPerson)
    idx=wnd.cbIvc.count()-1
    wnd.cbIvc.setCurrentIndex(wnd.cbIvc.count()-1)
    wnd.OnCbSelChanged(idx)
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()

  def OnSave(self):
    for w in self.fldLst:
      fld=w.windowTitle()
      if fld=='id': break
    if w.text()=='':
      newId=SqlInsert(self.fldLst,'Person')
      w.setText(str(newId)) #TODO add entry to combobox
    else:
      SqlUpdate(self.fldLst,'Person')
    self.SetChanged(False)

  def OnDelete(self):
    #TODO
    MsgBox('NOT YET IMPLEMENTED')


  def OnNew(self):
    if not self.SwitchRecord(): return
    self.cbNaVo.setCurrentIndex(-1)
    for w in self.fldLst:
      w.setText('')
    self.SetChanged(False)


class WndTreatment(WndSqlBase):
  def __init__(self,sqlCombo=None,fkPerson=None,pkTreatment=None,geometry=(100,100,800,500)):
    super(WndTreatment,self).__init__(geometry)
    self.args=(sqlCombo,fkPerson)
    if sqlCombo:
      title=sqlCombo
    elif fkPerson:
      dbc=qtw.QApplication.instance().mkb.db.cursor()
      row=dbc.execute("SELECT fstName,lstName FROM Person WHERE id=?",(fkPerson,)).fetchone()
      title='Treatments: %s %s'%row
    else:
      title='Treatments'
    self.setWindowTitle(title)

    #https://doc-snapshots.qt.io/qt5-5.15/qformlayout.html
    loV=qtw.QVBoxLayout(self)
    loH=qtw.QHBoxLayout()
    loF=qtw.QFormLayout()

    loV.addLayout(loF)
    self.cbTrt=cb=qtw.QComboBox()
    cb.setEditable(True)
    cb.setMaxVisibleItems(20)
    cb.activated.connect(self.OnCbSelChanged)

    loF.addRow('Suche',cb)
    self.fldLst=fldLst=list()
    for txt in ('id','fkInvoice','fkPerson','dtTreatment','duration','costPerHour','comment','tarZif'):
      w=self.SqlWidget(txt)
      if fkPerson is not None and txt=='fkPerson': w.setText(str(fkPerson))
      fldLst.append(w)
      loF.addRow(txt,w)

    txt='document'
    w=self.SqlWidget(txt,qtw.QTextEdit)
    w.setMinimumWidth(1000)
    w.setMaximumHeight(400)

    fldLst.append(w)
    #loF.addRow(txt,w)
    loV.addWidget(w)
    loV.addLayout(loH)

    self.CbTrtPopulate(pkTreatment)

    for txt,func in (("Ext. Edit",self.OnWndTreatment),("Delete",self.OnDelete),("New",self.OnNew),("Save",self.OnSave)):#("Rechnungen",self.OnWndInvoice),("Report Treatment",self.OnRptTreatmentProgress)):
      btn=qtw.QPushButton(txt,self)
      if func is not None:
        btn.clicked.connect(func)
      loH.addWidget(btn)

  def CbTrtPopulate(self,pkTreatment=None):
    (sqlCombo,fkPerson)=self.args
    cb=self.cbTrt
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    if sqlCombo:
      itemsTrt=dbc.execute(sqlCombo).fetchall()
    elif fkPerson:
      sqlCombo='SELECT id, dtTreatment, comment FROM Treatment WHERE fkPerson=? ORDER BY fkPerson,dtTreatment'
      itemsTrt=dbc.execute(sqlCombo,(fkPerson,)).fetchall()
    else:
      sqlCombo='SELECT id, dtTreatment, comment FROM Treatment ORDER BY fkPerson,dtTreatment'
      itemsTrt=dbc.execute(sqlCombo).fetchall()
    cmpTrt=[]
    setIdx=-1
    for pkTrt,datTrt,comment in itemsTrt:
      datTrt=time.strftime('%d.%m.%y',time.strptime(datTrt,'%Y-%m-%d'))
      cmpTrt.append(datTrt)
      cb.addItem(datTrt+' '+str(comment),pkTrt)
      if pkTrt==pkTreatment:
        setIdx=cb.count()-1
    cb.setCurrentIndex(setIdx) #by default the text will be the first item. This clears the value if -1 or set to the selected one
    if pkTreatment:
      if setIdx==-1:
        MsgBox('pkTreatment %d not found'%pkTreatment,icon=qtw.QMessageBox.Warning)
      else:
        self.OnCbSelChanged(setIdx)
    cpl=qtw.QCompleter(cmpTrt)
    cpl.setCaseSensitivity(qtc.Qt.CaseInsensitive)
    cpl.setFilterMode(qtc.Qt.MatchContains)
    cb.setCompleter(cpl)

  def OnCbSelChanged(self,i):
    cb=self.cbTrt
    curData=cb.currentData()
    print('OnCbSelChanged',i,curData,cb.currentIndex())
    if not self.SwitchRecord():
      cb.setCurrentText('')
      return
    if cb.currentData() is None:
      print("TODO:New Person inserted")
      cb.removeItem(i)
    else:
      dbc=qtw.QApplication.instance().mkb.db.cursor()
      row=dbc.execute('SELECT * FROM Treatment WHERE id=%d'%curData).fetchone()
      #print(d)
      for w,d in zip(self.fldLst,row):
        if d is None:
          d=''
        else:
          d=str(d)
        w.setText(d)
      self.SetChanged(False)

  def OnWndTreatment(self):
    cb=self.cbTrt
    pkBehandlung=cb.currentData()
    wpWnd=wp.MainWindow()
    wpWnd.record_open(pkBehandlung)
    WndChildAdd(wpWnd)

  def OnSave(self):
    for w in self.fldLst:
      fld=w.windowTitle()
      if fld=='id': break
    if w.text()=='':
      newId=SqlInsert(self.fldLst,'Treatment')
      w.setText(str(newId)) #TODO add entry to combobox
    else:
      SqlUpdate(self.fldLst,'Treatment')
    self.SetChanged(False)

  def OnDelete(self):
    #TODO
    MsgBox('NOT YET IMPLEMENTED')

  def OnNew(self):
    if not self.SwitchRecord(): return
    self.cbTrt.setCurrentIndex(-1)
    for w in self.fldLst:
      if w.windowTitle()=='fkPerson':
        fkPerson=int(w.text())
        continue
      elif w.windowTitle()=='costPerHour':
        w.setText('180')
      elif w.windowTitle()=='duration':
        w.setText('60')
      elif w.windowTitle()=='dtTreatment':
        qtw.QLineEdit.setText(w,(time.strftime('%d.%m.%y',time.gmtime())))
      elif w.windowTitle()=='comment':
        dbc=qtw.QApplication.instance().mkb.db.cursor()
        row=dbc.execute('SELECT fstName FROM Person WHERE id=%d'%fkPerson).fetchone()
        w.setText('Therapie mit %s'%row[0])
      else:
        w.setText('')
    self.SetChanged(False)

class TblInvoice(qtw.QTableWidget):
  def __init__(self,wndInvoice):
    super(TblInvoice,self).__init__(1,4)#rows cols
    self.setHorizontalHeaderLabels(('date','min','comment','Fr/h',))
    hh=self.horizontalHeader()
    hh.setMinimumSectionSize(20)
    vh=self.verticalHeader()
    vh.setDefaultSectionSize(20)
    #qTbl.resizeColumnsToContents()
    for i,w in enumerate((100,40,270,40)):
      self.setColumnWidth(i,w)
    #qTbl.setFixedWidth(400)
    self.setMinimumWidth(500)
    self.wndInvoice=wndInvoice
    self.cellDoubleClicked.connect(self.OnTbTrtDblClick)

  def populate(self,pkInvoice,fkPerson):
    self.key=(pkInvoice,fkPerson)
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    sqlData=dbc.execute('SELECT id,fkPerson,dtTreatment,duration,comment,costPerHour FROM Treatment WHERE fkInvoice=%d ORDER BY dtTreatment;'%pkInvoice).fetchall()
    self.clearContents()
    rc=len(sqlData)
    self.setRowCount(rc+1)
    self.lstTrtKey=lstTrtKey=list()

    for ir,row in enumerate(sqlData):
      key=row[0:2];lstTrtKey.append(key)
      for ic,data in enumerate(row[2:]):
        if ic==0: data=time.strftime('%d.%m.%y',time.strptime(data,'%Y-%m-%d'))
        else:     data=str(data)
        tw=qtw.QTableWidgetItem(data)
        tw.setFlags(qtc.Qt.ItemIsEnabled|qtc.Qt.ItemIsSelectable)
        if ic!=2: tw.setTextAlignment(qtc.Qt.AlignCenter)
        #tw=qtw.QTableWidgetItem(str(data),type=int)
        #qtc.Qt.ItemIsEnabled
        self.setItem(ir,ic,tw)

    self.cbTrt=cb=qtw.QComboBox()
    sqlData=dbc.execute('SELECT id,fkPerson,dtTreatment FROM Treatment WHERE fkInvoice is NULL AND fkPerson=%d ORDER BY dtTreatment;'%fkPerson).fetchall()
    cb.addItem('',-1)
    cb.currentIndexChanged.connect(self.OnCbSelTrtCng)
    for row in sqlData:
      date=time.strftime('%d.%m.%y',time.strptime(row[2],'%Y-%m-%d'))
      cb.addItem(date,row[0])
      #cb.addItem(str(row),row[0])
    #cb.setCurrentIndex(-1) #by default the text will be the first item. This clears the value
    self.setCellWidget(rc,0,cb)
    return

  def OnCbSelTrtCng(self,i):
    #add a treatment to the current invoice
    app=qtw.QApplication.instance()
    db=app.mkb.db
    dbc=db.cursor()
    cb=self.cbTrt
    pkTreatment=cb.currentData()
    pkInvoice=self.wndInvoice.cbIvc.currentData()
    print('add Treatment %d to invoice %d'%(pkTreatment,pkInvoice))
    sqlStr='UPDATE Treatment SET fkInvoice=? WHERE id=?'
    dbc.execute(sqlStr,(pkInvoice,pkTreatment))
    self.populate(*self.key)
    db.commit()

  def OnTbTrtDblClick(self,row,col):
    #open tretment that was double clicked
    trtKey=self.lstTrtKey[row]
    print('Open treatment',trtKey)
    wnd=WndTreatment(fkPerson=trtKey[1],pkTreatment=trtKey[0])
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.wndInvoice.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()
    return

  def contextMenuEvent(self, event):
    ctxMn=qtw.QMenu(self)
    actDel=ctxMn.addAction('remove from invoice')
    action=ctxMn.exec_(self.mapToGlobal(event.pos()))
    if action==actDel:
      print('delete')
      item=self.itemAt(event.pos())
      idx=self.indexFromItem(item)
      idx.row()
      idx.data()
      pkTreatment,fkPerson=self.lstTrtKey[idx.row()]

      db=qtw.QApplication.instance().mkb.db
      dbc=db.cursor()
      sqlStr='UPDATE Treatment SET fkInvoice=NULL WHERE id=?'
      dbc.execute(sqlStr,(pkTreatment,))
      self.populate(*self.key)
      db.commit()


class WndInvoice(WndSqlBase):
  def __init__(self,sqlCombo=None,fkPerson=None,pkInvoice=None,geometry=(100,100,800,500)):
    super(WndInvoice,self).__init__(geometry)
    self.args=(sqlCombo,fkPerson)
    if sqlCombo:
      title=sqlCombo
    elif fkPerson:
      dbc=qtw.QApplication.instance().mkb.db.cursor()
      row=dbc.execute("SELECT fstName,lstName FROM Person WHERE id=?",(fkPerson,)).fetchone()
      title='Invoices: %s %s'%row
    else:
      title='Invoices'
    self.setWindowTitle(title)

    #https://doc-snapshots.qt.io/qt5-5.15/qformlayout.html
    loV=qtw.QVBoxLayout(self)
    loH=qtw.QHBoxLayout()
    loF=qtw.QFormLayout()

    loV.addLayout(loF)
    loV.addLayout(loH)
    self.cbIvc=cb=qtw.QComboBox()
    cb.setEditable(True)
    cb.activated.connect(self.OnCbSelChanged)
    loF.addRow('Suche',cb)

    self.fldLst=fldLst=list()

    for txt in ('id','fkPerson','fkAccount','tplInvoice','dtInvoice'):
      w=self.SqlWidget(txt)
      if fkPerson is not None and txt=='fkPerson': w.setText(str(fkPerson))
      fldLst.append(w)
      loF.addRow(txt,w)

    txt='comment'
    w=self.SqlWidget(txt,qtw.QTextEdit)
    w.setMinimumWidth(200)
    w.setMinimumHeight(40)
    fldLst.append(w)
    loF.addRow(txt,w)

    #Adding sql table for treatments
    self.tbTreatment=tbTrt=TblInvoice(self)
    loF.addRow('Treatments',tbTrt)

    self.CbIvcPopulate(pkInvoice)

    for txt,func in (("Report Invoice",self.OnRptInvoice),("Delete",self.OnDelete),("New",self.OnNew),("Save",self.OnSave)):
      btn=qtw.QPushButton(txt,self)
      if func is not None:
        btn.clicked.connect(func)
      loH.addWidget(btn)

  def CbIvcPopulate(self,pkInvoice):
    (sqlCombo,fkPerson)=self.args
    cb=self.cbIvc
    cb.clear()
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    if sqlCombo:
      itemsIvc=dbc.execute(sqlCombo).fetchall()
    elif fkPerson:
      sqlCombo='SELECT id,dtInvoice FROM Invoice WHERE fkPerson=? ORDER BY dtInvoice'
      itemsIvc=dbc.execute(sqlCombo,(fkPerson,)).fetchall()
    else:
      #sqlCombo='SELECT id,fkPerson||" "||dtInvoice FROM Invoice ORDER BY fkPerson,dtInvoice'
      sqlCombo='SELECT id,dtInvoice FROM Invoice ORDER BY fkPerson,dtInvoice'
      itemsIvc=dbc.execute(sqlCombo).fetchall()
    cmpIvc=[]
    setIdx=-1
    for pkIvc, datIvc in itemsIvc:
      try:
        datIvc=time.strftime('%d.%m.%y',time.strptime(datIvc,'%Y-%m-%d'))
      except BaseException as e:
        datIvc=str(datIvc)
      cmpIvc.append(datIvc)
      cb.addItem(datIvc,pkIvc)
      if pkIvc==pkInvoice:
        setIdx=cb.count()-1
    cb.setCurrentIndex(setIdx) #by default the text will be the first item. This clears the value
    if pkInvoice:
      if setIdx==-1:
        MsgBox('pkInvoice %d not found'%pkInvoice,icon=qtw.QMessageBox.Warning)
      else:
        self.OnCbSelChanged(setIdx)

    cpl=qtw.QCompleter(cmpIvc)
    cpl.setCaseSensitivity(qtc.Qt.CaseInsensitive)
    cpl.setFilterMode(qtc.Qt.MatchContains)
    cb.setCompleter(cpl)

  def OnCbSelChanged(self,i):
    #changed the current invoice
    cb=self.cbIvc
    if not self.SwitchRecord():
      cb.setCurrentText('')
      return
    pkInvoice=cb.currentData()
    if pkInvoice is None: return
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    dbRow=dbc.execute('SELECT * FROM Invoice WHERE id=%d'%pkInvoice).fetchone()
    #print(d)
    for w,d in zip(self.fldLst,dbRow):
      if d is None:
        d=''
      else:
        d=str(d)
      w.setText(d)
    self.SetChanged(False)
    fkPerson=dbRow[1]
    self.tbTreatment.populate(pkInvoice,fkPerson)

  def OnRptInvoice(self):
    print('OnRptInvoice')
    app=qtw.QApplication.instance()
    curData=self.cbIvc.currentData()
    app.mkb.report_invoice(pkInvoice=curData)

  def OnSave(self):
    for w in self.fldLst:
      fld=w.windowTitle()
      if fld=='id': break
    if w.text()=='':
      pkInvoice=SqlInsert(self.fldLst,'Invoice')
      w.setText(str(pkInvoice)) #TODO add entry to combobox
      self.CbIvcPopulate(pkInvoice)
      (sqlCombo,fkPerson)=self.args
      self.tbTreatment.populate(pkInvoice,fkPerson)
    else:
      SqlUpdate(self.fldLst,'Invoice')
    self.SetChanged(False)

  def OnDelete(self):
    #TODO
    curData=self.cbIvc.currentData()
    db=qtw.QApplication.instance().mkb.db
    dbc=db.cursor()
    sqlStr='DELETE FROM Invoice WHERE id=?'
    try:
      dbc.execute(sqlStr,(curData,))
    except lite.IntegrityError as e:
      detail='Failed:\n'+str(type(e))+'\n'+str(e)+'\n'+sqlStr
      MsgBox('Delete not possible.\nThe invoice must have no assigned treatments',title="SQL error"+' '*100,msgInfo=None,detail=detail,btn=qtw.QMessageBox.Ok,
             icon=qtw.QMessageBox.Critical)
      return
    db.commit()
    self.CbIvcPopulate(None)
    self.tbTreatment.clearContents()
    for w in self.fldLst:
      if w.windowTitle()=='fkPerson':
        continue
      else:
        w.setText('')
    self.SetChanged(False)
    MsgBox('Invoice deleted',title="SQL info",btn=qtw.QMessageBox.Ok)

  def OnNew(self):
    if not self.SwitchRecord(): return
    self.cbIvc.setCurrentIndex(-1)
    for w in self.fldLst:
      if w.windowTitle()=='fkPerson':
        continue
      else:
        w.setText('')
    tbTrt=self.tbTreatment
    tbTrt.clearContents();tbTrt.setRowCount(1)
    self.SetChanged(False)

class WndMain(qtw.QMainWindow):

  def __init__(self):
    super(WndMain,self).__init__()
    self.setGeometry(50,50,1300,800)
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
    act=AddMenuAction(self,mnEdit,"Person",self.OnWndPerson,shortcut="Ctrl+A")
    act=AddMenuAction(self,mnEdit,"Quick Select Table",self.OnWndQuickSelect,shortcut="Ctrl+Q")
    mnEdit.addSeparator()
    act=AddMenuAction(self,mnEdit,"Sync Invoice->Account",self.OnWndSyncIvcAcc,shortcut="Ctrl+S")
    act=AddMenuAction(self,mnEdit,"Import Account CSV",self.OnImportCSV,shortcut="Ctrl+W")
    mnRpt=mainMenu.addMenu('&Report')
    act=AddMenuAction(self,mnRpt,"Invoices",self.OnRepInvoices)
    act=AddMenuAction(self,mnRpt,"Therapy Progress",self.OnRepTherapyProgress)
    act=AddMenuAction(self,mnRpt,"Couvert",self.OnCouvert)
    mnDbg=mainMenu.addMenu('&Debug')
    act=AddMenuAction(self,mnDbg,"Table Person",self.OnTblPerson,shortcut="Ctrl+Shift+A")
    act=AddMenuAction(self,mnDbg,"Table Treatment",self.OnTblTreatment,shortcut="Ctrl+Shift+S")
    act=AddMenuAction(self,mnDbg,"Table Invoice",self.OnTblInvoice,shortcut="Ctrl+Shift+D")
    act=AddMenuAction(self,mnDbg,"Table Account",self.OnTblAccount,shortcut="Ctrl+Shift+F")
    act=AddMenuAction(self,mnDbg,"OnWndChildTest",self.OnWndChildTest)

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
    wnd=WndPerson()
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.mdi.addSubWindow(sub)
    sub.show()

  def OnImportCSV(self):
    print("OnImportCSV")
    #https://doc.qt.io/qt-5/qfiledialog.html#Option-enum
    (fname,filter)=qtw.QFileDialog.getOpenFileName(self,'Open file','/home/zamofing_t/Documents/prj/Mokabu','CSV files (*.csv);;TXT files (*.txt)',
    options=qtw.QFileDialog.Option.DontUseNativeDialog |
    qtw.QFileDialog.Option.DontResolveSymlinks |
    qtw.QFileDialog.Option.DontUseSheet |
    qtw.QFileDialog.Option.DontUseCustomDirectoryIcons)
    print(fname)
    if fname:
      app=qtw.QApplication.instance()
      cnt=app.mkb.sync_invoice(fname)
      MsgBox('CSV Import done\n\n%d ignored duplicates\n%d new entries'%cnt)

  def OnWndSyncIvcAcc(self):
    print("OnWndSyncIvcAcc")
    wnd=WndSyncIvcAcc('WndSyncIvcAcc')
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.mdi.addSubWindow(sub)
    sub.show()

  def OnWndQuickSelect(self):
    print("OnWndQuickSelect")
    wnd=WndQuickSelect()
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.mdi.addSubWindow(sub)
    sub.show()

  def OnRepInvoices(self):
    print("OnRepInvoices")
    app=qtw.QApplication.instance()
    app.mkb.report_invoice()

  def OnRepTherapyProgress(self):
    print("OnRepTherapyProgress")
    app=qtw.QApplication.instance()
    app.mkb.report_therapy_progress()

  def OnCouvert(self):
    print("OnCouvert")
    report.Couvert('Couvert.pdf')
    report.default_app_open('Couvert.pdf')

  def OnWndChildTest(self):
    print("OnWndChildTest")
    wnd=qtw.QWidget();wnd.setWindowTitle("WndQryTreatment")
    WndChildAdd(wnd)


#https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlRelationalTableModel.html
#https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlTableModel.html
#TODO:
# quite generic QSqlTableModel UI QSqlRelationalTableModel


if __name__=='__main__':

  MainApp(None)
