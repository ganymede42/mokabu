#!/usr/bin/python3
#https://www.tutorialspoint.com/pyqt/pyqt_hello_world.htm
#https://github.com/tpgit/MDIImageViewer usefull sample application
import logging
_log=logging.getLogger(__name__)

import sys,time,subprocess
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtSql as qtdb
import report
import wordprocessor as wp
import traceback
import sqlite3 as lite
from app_config import AppCfg,WndSetting
from TarZif import Lut as LutTarZif

def get_version(path='.'):
  #sys.stdout.write('getVersion() -> using git command -> ')
  p = subprocess.Popen(f'git -C {path} describe --match "*.*.*" --long --tags --dirty=-mod', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  retval = p.wait()
  res=p.stdout.readline()
  p.stdout.close()
  #res=res.decode()[1:-1].split('-',2)
  res=res.decode()[:-1].split('-',2)
  ver='.'.join(res[:2])
  gitcmt=res[2][1:]
  return (ver,gitcmt)

def excepthook(exc_type,exc_value,exc_tb):
  tb="".join(traceback.format_exception(exc_type,exc_value,exc_tb))
  _log.info(f"error catched!:\n:error message:\n{tb}")
  msg=exc_type.__name__+': '+str(exc_value)
  MsgBox(msg,title="Not handeled Error"+' '*100,msgInfo=None,detail=tb,btn=qtw.QMessageBox.Ok,icon=qtw.QMessageBox.Critical)


def MainApp(mkb,dbg):
  app=qtw.QApplication(sys.argv)
  app.mkb=mkb
  app.db=db=qtdb.QSqlDatabase.addDatabase('QSQLITE')
  db.setDatabaseName('mokabu.db')
  if not db.open():
    _log.error('failed to open db')
  app._cfg=AppCfg()

  app.wndTop=set()
  mainWnd=WndMain() #must be assigned to a variable, else it 'selfsdestructs' before opening
  mainWnd.show()

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

  #Check if in debug mode
  gettrace=sys.gettrace()
  if gettrace:
    _log.debug(gettrace)
  else:
    sys.excepthook=excepthook
  sys.exit(app.exec_())

def testPerson(mainWnd,idx=39):
  wnd=WndPerson('WndPerson: %s'%'TESTING')
  wnd._cbNaVo.setCurrentIndex(idx)
  wnd.OnCbSelChanged(idx)#go to idx person
  sub=qtw.QMdiSubWindow()
  sub.setWidget(wnd)
  mainWnd.mdi.addSubWindow(sub)
  sub.show()

def testInvoice(mainWnd,idx=0,fkPerson=40):
  wnd=WndInvoice('WHERE fkPerson=%d'%fkPerson,'WndInvoice: %s'%'TESTING',fkPerson)
  wnd._cbIvc.setCurrentIndex(idx)
  wnd.OnCbSelChanged(idx)#go to first invoice
  sub=qtw.QMdiSubWindow()
  sub.setWidget(wnd)
  mainWnd.mdi.addSubWindow(sub)
  sub.show()

def testTreatment(mainWnd,idx=0,fkPerson=106,pkTreatment=881):
  wnd=WndTreatment(fkPerson=fkPerson, pkTreatment=pkTreatment)
  wnd._cbTrt.setCurrentIndex(idx)
  wnd.OnCbSelChanged(idx)#go idx treatment
  sub=qtw.QMdiSubWindow()
  sub.setWidget(wnd)
  mainWnd.mdi.addSubWindow(sub)
  sub.show()

def WndChildAdd(wnd):
  app=qtw.QApplication.instance()
  _log.debug(f"WndChildAdd {wnd},{app.wndTop}")
  app.wndTop.add(wnd)
  wnd.setAttribute(qtc.Qt.WA_DeleteOnClose)
  wnd.destroyed.connect(lambda:WndChildRemove(wnd))
  wnd.show()

def WndChildRemove(wnd):
  app=qtw.QApplication.instance()
  _log.debug(f"WndChildRemove{wnd},{app.wndTop}")
  app.wndTop.remove(wnd)

def SqlUpdate(fldLst,table,sqlWhere=None):
  app=qtw.QApplication.instance()
  sqlFld=list()
  sqlUpd=list()
  ''
  for w in fldLst:
    fld=w.windowTitle()
    if type(w)==qtw.QComboBox and fld=='tarZif':
      val=w.currentText().split(':', 1)[0]
      if val:
        assert (val in LutTarZif._lutTarZif.keys())
    elif type(w)==qtw.QTextEdit: #and fld=='document':
      val=w.toPlainText()
    else:
      val=w.text()
    if val=='':val=None
    if fld=='id' and sqlWhere is None:
      sqlWhere=' WHERE '+fld+'=?'
      valWhere=val
    else:
      sqlFld.append(fld+'=?')
      sqlUpd.append(val)
  sqlUpd.append(valWhere)
  sqlStr='UPDATE '+table+' SET '+ ','.join(sqlFld) +sqlWhere

  _log.debug(f'{sqlStr},{sqlUpd}')
  db=app.mkb.db
  dbc=db.cursor()
  dbc.execute(sqlStr,sqlUpd)
  #db.execute(sqlStr,sqlUpd)
  db.commit()

def SqlInsert(fldLst,table):
  app=qtw.QApplication.instance()
  sqlFld=list()
  sqlUpd=list()
  ''
  for w in fldLst:
    fld=w.windowTitle()
    if table=='Treatment' and fld=='tarZif':
      val=w.currentText().split(':', 1)[0]
      if val:
        assert (val in LutTarZif._lutTarZif.keys())
    elif type(w)==qtw.QTextEdit:
      val=w.toPlainText()
    else:
      val=w.text()
    if val=='':val=None
    if fld=='id':
      continue
    else:
      sqlFld.append(fld)
      sqlUpd.append(val)
  sqlStr='INSERT INTO '+table+' ('+ ','.join(sqlFld)+') VALUES ('+'?,'*(len(sqlFld)-1)+'?)'

  _log.debug(f'{sqlStr},{sqlUpd}')
  app=qtw.QApplication.instance()
  db=app.mkb.db
  dbc=db.cursor()
  dbc.execute(sqlStr,sqlUpd)
  #db.execute(sqlStr,sqlUpd)
  db.commit()
  sqlStr='SELECT MAX(id) FROM '+table
  newid=dbc.execute(sqlStr).fetchone()
  return newid[0]

def SqlDelete(where,table):
  app=qtw.QApplication.instance()
  sqlStr='DELETE FROM '+table+' WHERE '+where
  _log.debug(sqlStr)
  app=qtw.QApplication.instance()
  db=app.mkb.db
  dbc=db.cursor()
  dbc.execute(sqlStr)
  db.commit()
  return


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
        _log.warning(f'QDateEdit::setText: {e}')
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
      _log.debug(f'Validator.validate {text},{pos}')
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
    if qWndType not in (qtw.QLabel,qtw.QComboBox):
      w.textChanged.connect(self.OnTxtChanged)
    w.setWindowTitle(txt)
    return w

  def closeEvent(self, event):
      _log.debug("User has clicked the red x on the main window")
      if self.SwitchRecord()==True:
        event.accept()
      else:
        event.ignore()

  def OnTxtChanged(self):
    self.SetChanged(True)
    _log.debug(self)

  def SwitchRecord(self):
    #when close or change to new record ask to save
    _log.debug(self._changed)
    if self._changed is False: return True
    res=MsgBox('save changes to actual record?',
               btn=qtw.QMessageBox.Yes|qtw.QMessageBox.No|qtw.QMessageBox.Cancel,
               icon=qtw.QMessageBox.Question)
    _log.debug(f'pressed{res}')
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
      _log.debug(title)
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
      '''SELECT tr.fkPerson,tr.id,tr.fkInvoice,ps.cltFstName||' '||ps.cltLstName as fstLst,tr.dtTreatment,iv.dtInvoice,tr.duration,tr.comment
             FROM treatment tr
             LEFT JOIN Person ps on tr.fkPerson=ps.id
             LEFT JOIN Invoice iv on tr.fkInvoice=iv.id
             ORDER BY tr.dtTreatment DESC'''
    elif self.filtMode==1:
      sqlCmd=\
      '''SELECT tr.fkPerson,tr.id,tr.fkInvoice,ps.cltFstName||' '||ps.cltLstName as fstLst,tr.dtTreatment,iv.dtInvoice,tr.duration,tr.comment
             FROM treatment tr
             LEFT JOIN Person ps on tr.fkPerson=ps.id
             LEFT JOIN Invoice iv on tr.fkInvoice=iv.id
              WHERE tr.fkInvoice is NULL
              ORDER BY tr.fkPerson,tr.dtTreatment DESC'''
    else:
      sqlCmd=\
      '''SELECT tr.fkPerson,tr.id,tr.fkInvoice,ps.cltFstName||' '||ps.cltLstName as fstLst,tr.dtTreatment,iv.dtInvoice,tr.duration,tr.comment
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
    _log.debug('')
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
    #tbIvc.setSelectionMode(qtw.QAbstractItemView.NoSelection)
    #tbIvc.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)
    #https://doc.qt.io/archives/qt-4.8/qabstractitemview.html#SelectionMode-enum
    #SelectionMode = 0 => NoSelection
    #SelectionMode = 1 => SingleSelection
    #SelectionMode = 2 => MultiSelection
    #SelectionMode = 3 => ExtendedSelection
    #SelectionMode = 4 => ContiguousSelection


    tbIvc.currentCellChanged.connect(self.OnIvcCellChd)

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
    tbAcc.currentCellChanged.connect(self.OnAccCellChd)

    #loF.addRow('Treatments',tbTrt)
    loH.addWidget(tbAcc)
    self.FillAccout()

  def FillInvoice(self):
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    tbIvc=self.tbIvc
    sqlData=dbc.execute(\
    '''SELECT iv.id,COUNT(tr.id) AS cntTrt,fkAccount,dtInvoice,ivcLstName,ivcFstName,SUM(duration*costPerHour/60) AS cost,iv.comment,cltLstName,cltFstName
       FROM Treatment tr LEFT JOIN Invoice iv  ON tr.fkInvoice=iv.id
       LEFT JOIN Person ps ON iv.fkPerson=ps.id
       WHERE iv.id NOT NULL
       GROUP BY iv.id
       ORDER BY dtInvoice''').fetchall()
    tbIvc.clearContents()
    tbIvc.setRowCount(len(sqlData))
    self.ivcData=ivcData=dict()
    self.idx2ivc=idx2ivc=list()
    self.accData=accData=dict()

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
# 8 cltLstName
# 9 cltFstName
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
      ivcData[pkIvc]=(cost,)
      try:
        s=accData[fkAcc]
      except KeyError:
        accData[fkAcc]=s=(set(),None)
      s[0].add(pkIvc)
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
    #tbIvc.selectRow(10)
    tbIvc.scrollToBottom()
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
    ivcData=self.ivcData
    accData=self.accData

    col=qtg.QColor(196,255,196)  #qtg.QColor('yellow')
    lbl=('id','fkIvc','Datum','sum','diff','refText')

    for ir,row in enumerate(sqlData):
      pkAcc=row[0]
      dtEvent=report.dateconvert(row[1],1)
      amount=row[3]
      refText=row[2]
      idx2acc.append(pkAcc)
      try:
        ivcSet=accData[pkAcc][0]
      except KeyError:
        ivcSet=set()
      accData[pkAcc]=(ivcSet,amount)
      diff=amount
      for pkIvc in ivcSet:
        diff-=ivcData[pkIvc][0]
      if diff==0:
        diff=None
      else:
        diff=round(diff,2)
      #if ivcSet: fkIvc=str(ivcSet).strip('{}')
      if ivcSet: fkIvc=str(sorted(ivcSet)).strip('[]')
      else: fkIvc=None
      row=(pkAcc,fkIvc,dtEvent,amount,diff,refText)
      for ic,data in enumerate(row):
        if data is None: strCell=''
        #elif ic==4: strCell='%.2f'%data
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
    tbAcc.scrollToBottom()
    return

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

  def OnIvcCellChd(self,currentRow, currentColumn, previousRow, previousColumn):
    print('OnIvcCellChd',currentRow, currentColumn, previousRow, previousColumn)
    #self.tbIvc.selectRow(currentRow)
    #self.tbAcc.selectRow(currentRow)
    idx2ivc=self.idx2ivc
    accData=self.accData
    ivc=idx2ivc[currentRow]
    acc=None
    for k,v in accData.items():
      if ivc in v[0]:
        acc=k;break

    if acc is not None:
      accIdx=self.idx2acc.index(acc)
      if self.tbAcc.currentRow()!=accIdx:
        self.tbAcc.selectRow(accIdx)

  def OnAccCellChd(self,currentRow, currentColumn, previousRow, previousColumn):
    print('OnAccCellChd',currentRow, currentColumn, previousRow, previousColumn)
    if currentRow==previousRow: return
    col=qtg.QColor(32,255,32)  #qtg.QColor('yellow')
    tbIvc=self.tbIvc
    tbAcc=self.tbAcc
    rwAcc=currentRow

    idx2acc=self.idx2acc
    idx2ivc=self.idx2ivc
    accData=self.accData

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
      self.lstIvcHighlight=lstPkIvc=accData[pkAcc][0]
    except KeyError:
      pass
    else:
      idxIvcLst=list()
      for pkIvc in sorted(lstPkIvc):
        idxIvc=idx2ivc.index(pkIvc)
        idxIvcLst.append(idxIvc)
        item = self.tbIvc.item(idxIvc, 0)
        #self.tbIvc.scrollToItem(item, hint=qtg.QAbstractItemView.PositionAtCenter)
        if pkAcc>=0:
          self.tbIvc.scrollToItem(item)
        for i in range(tbIvc.columnCount()):
          tbIvc.item(idxIvc,i).setBackground(col)
      if self.tbIvc.currentRow() not in idxIvcLst:
        if idxIvcLst: idx=idxIvcLst[0]
        else: idx=-1
        self.tbIvc.selectRow(idx)

  def LinkAccIvc(self,ivcRow,accRow,pkIvc,pkAcc,link):
    tbIvc=self.tbIvc
    tbAcc=self.tbAcc
    ivcData=self.ivcData
    accData=self.accData
    db=qtw.QApplication.instance().mkb.db
    dbc=db.cursor()
    sqlStr='SELECT fkAccount FROM Invoice WHERE id=?'
    oldVal=dbc.execute(sqlStr,(pkIvc,)).fetchone()[0]
    print('LinkAccIvc',ivcRow,accRow,pkIvc,pkAcc,link,oldVal)

    accInfo=accData[pkAcc]

    if link:
      fkAcc=pkAcc
      accInfo[0].add(pkIvc)
    else:
      accInfo[0].remove(pkIvc)
      fkAcc=None

    if fkAcc is None:
      strIvc=strIvc=''
      col=qtg.QColor(255,255,255)
    else:
      strIvc=str(pkAcc)
      #col=qtg.QColor(196,255,196)#qtg.QColor('yellow')
      col=qtg.QColor(32,255,32)  #qtg.QColor('yellow')
    tw=tbIvc.item(ivcRow,1)
    tw.setText(strIvc) #  twAcc.setBackground(col)
    for i in range(tbIvc.columnCount()):
      tbIvc.item(ivcRow,i).setBackground(col)

    if len(accInfo[0])==0:
      col=qtg.QColor(255,255,255)
      fldTxt=('','')
    else:
      diff=accInfo[1]
      for pk in accInfo[0]:
        diff-=ivcData[pk][0]
      if diff==0:diff=''
      else:diff=str(round(diff,2))
      col=qtg.QColor(196,255,196)
      #fldTxt=(str(accInfo[0]).strip('{}'),diff)
      fldTxt=(str(sorted(accInfo[0])).strip('[]]'),diff)

    tbAcc.item(accRow,1).setText(fldTxt[0])
    tbAcc.item(accRow,4).setText(fldTxt[1])

    for i in range(tbAcc.columnCount()):
      tbAcc.item(accRow,i).setBackground(col)

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

    ivcRow=self.tbIvc.currentRow()
    accRow=self.tbAcc.currentRow()
    #print(ivcRow,accRow)
    #pos=pos-tbl.pos()
    #item=tbl.itemAt(pos)
    #idx=tbl.indexFromItem(item)

    ctxMn=qtw.QMenu(self)
    actFiltAll=ctxMn.addAction('filter: all invoices')
    actFiltOpen=ctxMn.addAction('filter: open invoices')

    actFiltLink=actFiltAlign=None

    if ivcRow>=0 and accRow>=0:
      pkIvc=self.idx2ivc[ivcRow]
      pkAcc=self.idx2acc[accRow]
      try:
        ivcSet=self.accData[pkAcc][0]
      except KeyError:
        ivcSet=set()
      if pkIvc in ivcSet:
        link=False
        actFiltLink=ctxMn.addAction('unlink invoice %d from account %d'%(pkIvc,pkAcc))
      else:
        link=True
        actFiltLink=ctxMn.addAction('link invoice %d to account %d'%(pkIvc,pkAcc))

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

    if action==actFiltLink:
      self.LinkAccIvc(ivcRow,accRow,pkIvc,pkAcc,link)

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
    self._cbNaVo=cb=qtw.QComboBox()
    cb.setEditable(True)
    cb.activated.connect(self.OnCbSelChanged)

    loF.addRow('Suche',cb)
    self._fldLst=fldLst=list()

    fld2lbl={
      'cltPrefix' :'Patient Anrede',
      'cltLstName':'Patient Name',
      'cltFstName':'Patient Vorname',
      'cltAddress':'Patient Adresse',
      'cltZipCode':'Patient PLZ',
      'cltCity'   :'Patient Ort',
      'cltAhvNr'  :'Patient AHV-Nr.',
      'cltDtBirth':'Patient Geburtsdatum',

      'ivcPrefix' :'Rng Anrede',
      'ivcLstName':'Rng Name',
      'ivcFstName':'Rng Vorname',
      'ivcAddress':'Rng Adresse',
      'ivcZipCode':'Rng PLZ',
      'ivcCity'   :'Rng Ort',

      'phone'  :'Telefon',
      'phone1' :'Telefon1',
      'phone2' :'Telefon2',
      'eMail'  :'eMail',
      'eMail1' :'eMail1',
      'eMail2' :'eMail2',
      'comment':'Bemerkung',
    }
    for desc in ('id','cltPrefix','cltLstName','cltFstName','cltAddress','cltZipCode','cltCity','cltAhvNr',('cltDtBirth',QDateEdit),
                 'ivcPrefix','ivcLstName','ivcFstName','ivcAddress','ivcZipCode','ivcCity',
                 'phone','phone1','phone2','eMail','eMail1','eMail2',('comment',qtw.QTextEdit) ):
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
    cb=self._cbNaVo
    cb.clear()
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    itemsNaVo=dbc.execute('SELECT id, cltLstName||" "||cltFstName FROM Person ORDER BY cltLstName,cltFstName').fetchall()

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
    cb=self._cbNaVo
    curData=cb.currentData()
    #print("OnCbSelChanged index",i,"selection changed ",cb.currentIndex(),str(curData),cb.currentText())
    _log.debug(f'{i},{curData},{cb.currentIndex()}')
    if not self.SwitchRecord():
      cb.setCurrentText('')
      return
    if cb.currentData() is None:
      _log.warning("TODO:New Person inserted")
      cb.removeItem(i)
    else:
      dbc=qtw.QApplication.instance().mkb.db.cursor()
      d=dbc.execute('SELECT * FROM Person WHERE id=%d'%curData).fetchone()
      #print(d)
      for w,d in zip(self._fldLst, d):
        if d is None:
          d=''
        else:
          d=str(d)
        w.setText(d)
      self.SetChanged(False)

  def OnRptTreatmentProgress(self):
    _log.debug('')
    app=qtw.QApplication.instance()
    pkPerson=self._cbNaVo.currentData()
    if pkPerson is None:
      MsgBox('No selected person')
      return
    app.mkb.report_therapy_progress(pkPerson=pkPerson)

  def OnWndTreatment(self):
    cb=self._cbNaVo
    pkPerson=cb.currentData()
    if pkPerson is None:
      MsgBox('No selected person')
      return
    wnd=WndTreatment(fkPerson=pkPerson)
    idx=wnd._cbTrt.count()-1
    wnd._cbTrt.setCurrentIndex(idx)
    wnd.OnCbSelChanged(idx) #force to update at beginning
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle(wnd.windowTitle())
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()

  def OnWndInvoice(self):
    cb=self._cbNaVo
    pkPerson=cb.currentData()
    if pkPerson is None:
      MsgBox('No selected person')
      return
    perStr=cb.currentText()
    wnd=WndInvoice(fkPerson=pkPerson)
    idx=wnd._cbIvc.count()-1
    wnd._cbIvc.setCurrentIndex(wnd._cbIvc.count()-1)
    wnd.OnCbSelChanged(idx)
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()

  def OnSave(self):
    for w in self._fldLst:
      fld=w.windowTitle()
      if fld=='id': break
    if w.text()=='':
      newId=SqlInsert(self._fldLst, 'Person')
      w.setText(str(newId)) #TODO add entry to combobox
    else:
      SqlUpdate(self._fldLst, 'Person')
    self.SetChanged(False)
    self._cbNaVo.clear() #clear all entries before repopulate
    self.CbNaVoPopulate(None)

  def OnDelete(self):
    w=self._fldLst[0]
    assert(w.windowTitle()=='id')
    txt=w.text()
    if txt:
      res=MsgBox('really delete this record?',
                 btn=qtw.QMessageBox.Yes|qtw.QMessageBox.No|qtw.QMessageBox.Cancel,
                 icon=qtw.QMessageBox.Question)
      _log.debug(f'pressed{res}')
      if res==qtw.QMessageBox.Yes:
        SqlDelete(f'id={txt}','Person')
    self.OnNew()
    self.SetChanged(False)
    self._cbNaVo.clear() #clear all entries before repopulate
    self.CbNaVoPopulate(None)


  def OnNew(self):
    if not self.SwitchRecord(): return
    self._cbNaVo.setCurrentIndex(-1)
    for w in self._fldLst:
      w.setText('')
    self.SetChanged(False)

class WndTreatment(WndSqlBase):
  def __init__(self,sqlCombo=None,fkPerson=None,pkTreatment=None,geometry=(100,100,800,500)):
    super(WndTreatment,self).__init__(geometry)
    self._args=(sqlCombo, fkPerson)
    if sqlCombo:
      title=sqlCombo
    elif fkPerson:
      dbc=qtw.QApplication.instance().mkb.db.cursor()
      row=dbc.execute("SELECT cltFstName,cltLstName FROM Person WHERE id=?",(fkPerson,)).fetchone()
      title='Treatments: %s %s'%row
    else:
      title='Treatments'
    self.setWindowTitle(title)

    #https://doc-snapshots.qt.io/qt5-5.15/qformlayout.html
    loV=qtw.QVBoxLayout(self)
    loH=qtw.QHBoxLayout()
    loF=qtw.QFormLayout()

    loV.addLayout(loF)
    self._cbTrt=cb=qtw.QComboBox()
    cb.setEditable(True)
    cb.setMaxVisibleItems(20)
    cb.activated.connect(self.OnCbSelChanged)

    loF.addRow('Suche',cb)
    self._fldLst=fldLst=list()
    for desc in ('id','fkInvoice','fkPerson','dtTreatment','duration','costPerHour','comment',('tarZif',qtw.QComboBox)):
      if type(desc)==str:
        w=self.SqlWidget(desc);fld=desc
      else:
        w=self.SqlWidget(*desc);fld=desc[0]
      if fkPerson is not None and fld=='fkPerson': w.setText(str(fkPerson))
      if fld=='tarZif':
        self._cbTarZif=w
        self.TarZifPopulate(w)
      fldLst.append(w)
      loF.addRow(fld,w)

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
    (sqlCombo,fkPerson)=self._args
    cb=self._cbTrt
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
    cb=self._cbTrt
    curData=cb.currentData()
    _log.debug(f'{i},{curData},{cb.currentIndex()}')
    if not self.SwitchRecord():
      cb.setCurrentText('')
      return
    if curData is None:
      _log.warning("First treatment inserted")
      self.OnNew()
    else:
      dbc=qtw.QApplication.instance().mkb.db.cursor()
      row=dbc.execute('SELECT * FROM Treatment WHERE id=%d'%curData).fetchone()
      #print(d)
      for w,d in zip(self._fldLst, row):
        if d is None:
          d=''
        else:
          d=str(d)
        if type(w)==qtw.QComboBox:
          self.OnTarZifSelChanged(d,False)
        else:
          w.setText(d)
      self.SetChanged(False)

  def TarZifPopulate(self,cb):
    cb.setEditable(True)
    cb.setMaxVisibleItems(20)
    cmpTbl=[]
    for k,v in LutTarZif._lutTarZif.items():
      txt=k+': '+str(v[2])
      cmpTbl.append(txt)
      cb.addItem(txt)
    cpl=qtw.QCompleter(cmpTbl)
    cpl.setCaseSensitivity(qtc.Qt.CaseInsensitive)
    cpl.setFilterMode(qtc.Qt.MatchContains)
    cb.setCompleter(cpl)
    self._cbTarZif=cb
    cb.currentTextChanged.connect(lambda x:self.OnTarZifSelChanged(x, True))
    pass

  def OnTarZifSelChanged(self,txt,updateCost):
    _log.debug(str(txt))

    cb=self._cbTarZif
    cb.blockSignals(True)
    if txt=='':
      cb.setCurrentText('')
      cb.blockSignals(False)
      return
    kv=txt.split(':',1)
    if len(kv)<2:
      cpl=cb.completer()
      cpl.setCompletionPrefix(txt)
      n=cpl.completionCount()
      _log.debug(f'{n} -> {cpl.currentCompletion()}')
      if n==1:
        cb.setCurrentText(cpl.currentCompletion())
    if updateCost:
      w=self._fldLst[5]
      assert(w.windowTitle()=='costPerHour')
      try:
        tz=LutTarZif.tar_zif(kv[0])
      except KeyError as e:
        _log.debug(f"Can't update costPerHour:  {e}")
      else:
        if tz[1]==0:
          txt=f'{float(tz[0]):0.2f}'
        else:
          txt=f'{float(tz[0]*60/tz[1]):0.2f}'
        w.setText(txt)
    cb.blockSignals(False)

  def OnWndTreatment(self):
    cb=self._cbTrt
    pkBehandlung=cb.currentData()
    wpWnd=wp.MainWindow()
    wpWnd.record_open(pkBehandlung)
    WndChildAdd(wpWnd)

  def OnSave(self):
    for w in self._fldLst:
      fld=w.windowTitle()
      if fld=='id': break
    if w.text()=='':
      pkTreatment=SqlInsert(self._fldLst, 'Treatment')
      #w.setText(str(pkTreatment)) #TODO add entry to combobox
    else:
      SqlUpdate(self._fldLst, 'Treatment')
      pkTreatment=self._cbTrt.currentData()
    self.SetChanged(False)
    self._cbTrt.clear() #clear all entries before repopulate
    self.CbTrtPopulate(pkTreatment)

  def OnDelete(self):
    w=self._fldLst[0]
    assert(w.windowTitle()=='id')
    txt=w.text()
    if txt:
      res=MsgBox('really delete this record?',
                 btn=qtw.QMessageBox.Yes|qtw.QMessageBox.No|qtw.QMessageBox.Cancel,
                 icon=qtw.QMessageBox.Question)
      _log.debug(f'pressed{res}')
      if res==qtw.QMessageBox.Yes:
        SqlDelete(f'id={txt}','Treatment')
    self.OnNew()
    self.SetChanged(False)
    self._cbTrt.clear() #clear all entries before repopulate
    self.CbTrtPopulate(None)

  def OnNew(self):
    if not self.SwitchRecord(): return
    self._cbTrt.setCurrentIndex(-1)
    self.OnTarZifSelChanged('PA010',True)
    for w in self._fldLst:
      t=w.windowTitle()
      if t=='fkPerson':
        fkPerson=int(w.text())
        continue
      elif t=='duration':
        w.setText('60')
      elif t=='dtTreatment':
        qtw.QLineEdit.setText(w,(time.strftime('%d.%m.%y',time.gmtime())))
      elif t=='comment':
        dbc=qtw.QApplication.instance().mkb.db.cursor()
        row=dbc.execute('SELECT cltFstName FROM Person WHERE id=%d'%fkPerson).fetchone()
        w.setText('Therapie mit %s'%row[0])
      elif t=='costPerHour':
        pass
      elif type(w)!=qtw.QComboBox:
        w.setText('')
    self.SetChanged(False)

class TblInvoice(qtw.QTableWidget):
  def __init__(self,wndInvoice):
    cols=('date','min','comment','Fr/h','TarZif',)
    super(TblInvoice,self).__init__(1,len(cols))#rows cols
    self.setHorizontalHeaderLabels(cols)
    hh=self.horizontalHeader()
    hh.setMinimumSectionSize(20)
    vh=self.verticalHeader()
    vh.setDefaultSectionSize(20)
    #qTbl.resizeColumnsToContents()
    colsW=(100,40,200,50,80)
    totW=15 #(start to add row counter
    for i,w in enumerate(colsW):
      self.setColumnWidth(i,w)
      totW+=w
    #qTbl.setFixedWidth(400)
    self.setMinimumWidth(totW)
    self.wndInvoice=wndInvoice
    self.cellDoubleClicked.connect(self.OnTbTrtDblClick)

  def populate(self,pkInvoice,fkPerson):
    self.key=(pkInvoice,fkPerson)
    dbc=qtw.QApplication.instance().mkb.db.cursor()
    sqlData=dbc.execute('SELECT id,fkPerson,dtTreatment,duration,comment,costPerHour,tarZif FROM Treatment WHERE fkInvoice=%d ORDER BY dtTreatment;'%pkInvoice).fetchall()
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
    pkInvoice=self.wndInvoice._cbIvc.currentData()
    _log.debug('add Treatment %d to invoice %d'%(pkTreatment,pkInvoice))
    sqlStr='UPDATE Treatment SET fkInvoice=? WHERE id=?'
    dbc.execute(sqlStr,(pkInvoice,pkTreatment))
    self.populate(*self.key)
    db.commit()

  def OnTbTrtDblClick(self,row,col):
    #open tretment that was double clicked
    trtKey=self.lstTrtKey[row]
    _log.debug(f'Open treatment {trtKey}')
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
      _log.debug('delete')
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
      row=dbc.execute("SELECT cltFstName,cltLstName FROM Person WHERE id=?",(fkPerson,)).fetchone()
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
    self._cbIvc=cb=qtw.QComboBox()
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
    cb=self._cbIvc
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
    cb=self._cbIvc
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
    _log.debug('')
    app=qtw.QApplication.instance()
    curData=self._cbIvc.currentData()
    app.mkb.report_invoice(pkInvoice=curData)

  def OnSave(self):
    for w in self.fldLst:
      fld=w.windowTitle()
      if fld=='id': break
    if w.text()=='':
      pkInvoice=SqlInsert(self.fldLst,'Invoice')
      w.setText(str(pkInvoice))
      (sqlCombo,fkPerson)=self.args
      self.tbTreatment.populate(pkInvoice,fkPerson)
    else:
      SqlUpdate(self.fldLst,'Invoice')
      pkInvoice=self._cbIvc.currentData()
    self.SetChanged(False)
    #self._cbIvc.clear() #clear all entries before repopulate
    self.CbIvcPopulate(pkInvoice)



  def OnDelete(self):
    curData=self._cbIvc.currentData()
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
    (sqlCombo,fkPerson)=self.args
    self._cbIvc.setCurrentIndex(-1)
    tbTrt=self.tbTreatment
    tbTrt.clearContents();tbTrt.setRowCount(1)
    self.SetChanged(False)
    db=qtw.QApplication.instance().mkb.db
    dbc=db.cursor()
    sqlStr='INSERT INTO Invoice (fkPerson,dtInvoice) VALUES (?,?)'
    dt=time.gmtime()
    dbc.execute(sqlStr,(fkPerson,time.strftime('%Y-%m-%d',dt)))
    #db.commit()
    pkInvoice=dbc.execute('SELECT MAX(id) FROM Invoice').fetchone()[0]

    for w in self.fldLst:
      t=w.windowTitle()
      if t=='fkPerson':
        continue
      elif t=='pkInvoice':
        w.setText(str(pkInvoice))
      elif t=='dtInvoice':
        datIvc=time.strftime('%d.%m.%y',dt)
        w.setText(datIvc)
      else:
        w.setText('')
    self.tbTreatment.populate(pkInvoice,fkPerson)
    self.CbIvcPopulate(pkInvoice)



class WndMain(qtw.QMainWindow):

  def __init__(self):
    super(WndMain,self).__init__()
    app=qtw.QApplication.instance()
    cfg=app._cfg.value(AppCfg.SETTINGS)
    try:
      imgFn=cfg['images']['main']
      img=qtg.QPixmap(imgFn)
      icoFn=cfg['images']['icon']
      ico=qtg.QIcon(icoFn)
    except KeyError as e:
      _log.warning(f'failed to load main image or icon: {e}')
      img=ico=None
    self.setGeometry(50,50,1700,1100)
    self.setWindowTitle("MoKaBu")
    self.setWindowIcon(ico)
    #self.setWindowIcon(qtw.QIcon('pythonlogo.png'))
    #self.mdi=qtw.QMdiArea()
    self.mdi=mdi=MdiArea(img);mdi.centered=True
    self.setCentralWidget(self.mdi)
    mainMenu=self.menuBar()
    self.statusBar()
    mnFile=mainMenu.addMenu('&File')

    act=AddMenuAction(self,mnFile,"Settings...",self.OnSettings)
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
    mnHlp=mainMenu.addMenu('&Help')
    act=AddMenuAction(self,mnHlp,"About...",self.OnAbout)
    mnDbg=mainMenu.addMenu('&Debug')
    act=AddMenuAction(self,mnDbg,"Table Person",self.OnTblPerson,shortcut="Ctrl+Shift+A")
    act=AddMenuAction(self,mnDbg,"Table Treatment",self.OnTblTreatment,shortcut="Ctrl+Shift+S")
    act=AddMenuAction(self,mnDbg,"Table Invoice",self.OnTblInvoice,shortcut="Ctrl+Shift+D")
    act=AddMenuAction(self,mnDbg,"Table Account",self.OnTblAccount,shortcut="Ctrl+Shift+F")
    act=AddMenuAction(self,mnDbg,"OnWndChildTest",self.OnWndChildTest)

  def closeEvent(self, event):
    _log.debug('')
    app=qtw.QApplication.instance()
    #app.wndTop.clear()  #free and close all instances
    #if len(app.wndTop)>0:
    #  print('close cild windows first',app.wndTop)
    #  event.ignore()
    sys.exit()

  def OnSettings(self):
    wnd=WndSetting()
    WndChildAdd(wnd)
  def OnQuit(self):
    _log.debug('')
    sys.exit()

  def OnTblPerson(self):
    _log.debug('')
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
    _log.debug('')
    wnd=WndSqlTblView('TblTreatments:','Treatment',geometry=(100,100,1200,700))
    for i in range(wnd.mdl.columnCount()):
      wnd.tbl.resizeColumnToContents(i)
    WndChildAdd(wnd)

  def OnTblInvoice(self):
    _log.debug('')
    wnd=WndSqlTblView('TblInvoices:','Invoice',geometry=(100,100,600,700))
    for i in range(wnd.mdl.columnCount()):
      wnd.tbl.resizeColumnToContents(i)
    WndChildAdd(wnd)

  def OnTblAccount(self):
    _log.debug('')
    wnd=WndSqlTblView('TblAccount:','Account',geometry=(100,100,600,700))
    for i in range(wnd.mdl.columnCount()):
      wnd.tbl.resizeColumnToContents(i)
    WndChildAdd(wnd)

  def OnWndPerson(self):
    _log.debug('')
    wnd=WndPerson()
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.mdi.addSubWindow(sub)
    sub.show()

  def OnImportCSV(self):
    _log.debug('')
    #https://doc.qt.io/qt-5/qfiledialog.html#Option-enum
    (fname,filter)=qtw.QFileDialog.getOpenFileName(self,'Open file','/home/zamofing_t/Documents/prj/Mokabu','CSV files (*.csv);;TXT files (*.txt)',
    options=qtw.QFileDialog.Option.DontUseNativeDialog |
    qtw.QFileDialog.Option.DontResolveSymlinks |
    qtw.QFileDialog.Option.DontUseSheet |
    qtw.QFileDialog.Option.DontUseCustomDirectoryIcons)
    _log.debug(fname)
    if fname:
      app=qtw.QApplication.instance()
      cnt=app.mkb.sync_invoice(fname)
      MsgBox('CSV Import done\n\n%d ignored duplicates\n%d new entries'%cnt)

  def OnWndSyncIvcAcc(self):
    _log.debug('')
    wnd=WndSyncIvcAcc('WndSyncIvcAcc')
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.mdi.addSubWindow(sub)
    sub.show()

  def OnWndQuickSelect(self):
    _log.debug('')
    wnd=WndQuickSelect()
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.mdi.addSubWindow(sub)
    sub.show()

  def OnRepInvoices(self):
    _log.debug('')
    app=qtw.QApplication.instance()
    app.mkb.report_invoice()

  def OnRepTherapyProgress(self):
    _log.debug('')
    app=qtw.QApplication.instance()
    app.mkb.report_therapy_progress()

  def OnCouvert(self):
    _log.debug('')
    report.Couvert('Couvert.pdf')
    report.default_app_open('Couvert.pdf')

  def OnWndChildTest(self):
    _log.debug('')
    wnd=qtw.QWidget();wnd.setWindowTitle("WndQryTreatment")
    WndChildAdd(wnd)

  def OnAbout(self):
    try:
      ver, gitcmt=get_version()
      v_MK=f'{ver} git:{gitcmt}'
    except:
      v_MK='git version failed'

    txt=f'''About Mokabu:

  Mokabu: {v_MK}

  Copyright (c) 2020
  Author Thierry Zamofing (th.zamofing@gmail.com)
  latest package at:
  https://github.com/ganymede42/mokabu/archive/refs/heads/master.zip
  '''
    qtw.QMessageBox.about(self, "Mokabu", txt)



#https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlRelationalTableModel.html
#https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlTableModel.html
#TODO:
# quite generic QSqlTableModel UI QSqlRelationalTableModel


if __name__=='__main__':

  MainApp(None)
