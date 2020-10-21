#!/usr/bin/python3
#https://www.tutorialspoint.com/pyqt/pyqt_hello_world.htm

import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.QtSql as qtdb
import mokabu
import wordprocessor as wp


def MainApp(mkb):
  app=qtw.QApplication(sys.argv)
  app.mkb=mkb
  app.db=db=qtdb.QSqlDatabase.addDatabase('QSQLITE')
  db.setDatabaseName('mokabu.db')
  if not db.open():
    print('failed to open db')

  app.wndTop=set()
  mainWnd=WndMain() #must be assigned to a variable, else it 'selfsdestructs' before opening
  mainWnd.show()

  #mainWnd.OnQryClient()

  #wpWnd=wp.MainWindow()
  #wpWnd.record_open(1)
  #WndChildAdd(wpWnd)
  #app.topLevelWindows()
  #app.topLevelWidgets()
  sys.exit(app.exec_())

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

#Here a clean Main Window implementation.
#QMainWindow has compares to a QWidgets by default dockerbars for toolbars statusbar and menuBar
# #https://www.learnpyqt.com/courses/start/basic-widgets/
# http://zetcode.com/gui/pyqt5/menustoolbars/
def AddMenuAction(widget,parentMenu,txt,func):
  actQuit=qtw.QAction(txt,widget)
  actQuit.triggered.connect(func)
  parentMenu.addAction(actQuit)
  return actQuit


def SqlWidget(txt,qWndType):
  w=qWndType()
  w.setWindowTitle(txt)
  return w

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

class WndClient(qtw.QWidget):
  def __init__(self,title,geometry=(100,100,400,500)):
    super(WndClient,self).__init__()
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
    itemsNaVo=dbc.execute('SELECT pkPerson, Nachname||" "||Vorname FROM tblPerson').fetchall()

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
    cb.currentIndexChanged.connect(self.cbSelChanged)

    loF.addRow('Suche',cb)
    self.fldLst=fldLst=list()

    for desc in ('pkPerson','RngAnrede','RngNachname','RngVorname','RngAdresse',
                'RngAdresse1','RngAdresse2','PLZ','Ort','Nachname',
                'Vorname','Tel1','Tel2','datGeb','eMail','AHVNr',
                ('Bemerkung',qtw.QTextEdit) ):
      if type(desc)==str:
        txt=desc;qWndType=qtw.QLineEdit
      else:
        txt,qWndType=desc
      w=SqlWidget(txt,qWndType)
      fldLst.append(w)
      loF.addRow(txt,w)

    for txt,func in (("Behandlungen",self.OnWndTreatment),("Rechnungen",self.OnWndInvoice),("Report Treatment",self.OnRptTreatmentProgress),("Save",self.OnSave)):
      btn=qtw.QPushButton(txt,self)
      if func is not None:
        btn.clicked.connect(func)
      loH.addWidget(btn)

  def cbSelChanged(self,i):
    cb=self.cbNaVo
    curData=cb.currentData()
    #print("cbSelChanged index",i,"selection changed ",cb.currentIndex(),str(curData),cb.currentText())
    if cb.currentData() is None:
      print("TODO:New Person inserted")
      cb.removeItem(i)
    else:
      dbc=self.dbc
      d=dbc.execute('SELECT * FROM tblPerson WHERE pkPerson=%d'%curData).fetchone()
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
    app.mkb.report_therapy_progress('pkPerson=%d'%curData)

  def OnWndTreatment(self):
    cb=self.cbNaVo
    pkPerson=cb.currentData()
    perStr=cb.currentText()
    wnd=WndTreatment('WHERE fkPerson=%d'%pkPerson,'WndTreatment: %s'%perStr)
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()

  def OnWndInvoice(self):
    cb=self.cbNaVo
    pkPerson=cb.currentData()
    perStr=cb.currentText()
    wnd=WndInvoice('WHERE fkPerson=%d'%pkPerson,'WndInvoice: %s'%perStr)
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.parent().parent().parent().parent().mdi.addSubWindow(sub)
    sub.show()

  def OnSave(self):
    #d=dbc.execute('SELECT * FROM tblPerson WHERE pkPerson=%d'%curData).fetchone()
    #print(d)
    for w in self.fldLst:
      fld=w.windowTitle()
      txt=w.text()
      print('UPDATE %s with %s'%(fld,txt))

class WndTreatment(qtw.QWidget):
  def __init__(self,sqlFilter=None,title='WndTreatment',geometry=(100,100,800,500)):
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
    sqlQry='SELECT pkBehandlung, datBehandlung FROM tblBehandlung'
    if sqlFilter is not None: sqlQry+=' '+sqlFilter
    sqlQry+=' ORDER BY fkPerson,datBehandlung'
    itemsTrt=dbc.execute(sqlQry).fetchall()

    cb.setEditable(True)
    cmpTrt=[]
    for pkTrt,datTrt in itemsTrt:
      cmpTrt.append(datTrt)
      cb.addItem(datTrt,pkTrt)
    cb.setCurrentIndex(-1) #by default the text will be the first item. This clears the value
    cpl=qtw.QCompleter(cmpTrt)
    cb.setCompleter(cpl)
    cb.currentIndexChanged.connect(self.cbSelChanged)

    loF.addRow('Suche',cb)
    self.fldLst=fldLst=list()

    for txt in ('pkBehandlung','fkRechnung','fkPerson','datBehandlung','Dauer','Stundenansatz','Bemerkung','TarZif'):
      w=qtw.QLineEdit();w.setWindowTitle(txt)
      fldLst.append(w)
      loF.addRow(txt,w)

    txt='AktenEintrag'
    w=qtw.QTextEdit();w.setWindowTitle(txt)
    fldLst.append(w)
    loF.addRow(txt,w)

    for txt,func in (("Behandlungen",self.OnWndTreatment),):#("Rechnungen",self.OnWndInvoice),("Report Treatment",self.OnRptTreatmentProgress)):
      btn=qtw.QPushButton(txt,self)
      if func is not None:
        btn.clicked.connect(func)
      loH.addWidget(btn)


  def cbSelChanged(self,i):
    cb=self.cbTrt
    curData=cb.currentData()
    #print("cbSelChanged index",i,"selection changed ",cb.currentIndex(),str(curData),cb.currentText())
    if cb.currentData() is None:
      print("TODO:New Person inserted")
      cb.removeItem(i)
    else:
      dbc=self.dbc
      d=dbc.execute('SELECT * FROM tblBehandlung WHERE pkBehandlung=%d'%curData).fetchone()
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


class WndInvoice(qtw.QWidget):
  def __init__(self,sqlFilter=None,title='WndInvoice',geometry=(100,100,800,500)):
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
    self.cbRng=cb=qtw.QComboBox()
    #self.cbNaVoPkPers

    app=qtw.QApplication.instance()
    self.dbc=dbc=app.mkb.db.cursor()
    sqlQry='SELECT pkRechnung, datRechnung FROM tblRechnung'
    if sqlFilter is not None: sqlQry+=' '+sqlFilter
    sqlQry+=' ORDER BY fkPerson,datRechnung'

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
    cb.currentIndexChanged.connect(self.cbSelChanged)

    loF.addRow('Suche',cb)
    self.fldLst=fldLst=list()

    for txt in ('pkRechnung','fkPerson','datRechnung','datGedruckt','datBezahlt'):
      w=qtw.QLineEdit()
      fldLst.append(w)
      loF.addRow(txt,w)

    w=qtw.QTextEdit()
    fldLst.append(w)
    loF.addRow('Bemerkung',w)

    #Adding sql table for treatments
    self.mdl=mdl = qtdb.QSqlTableModel()
    #qry=qtdb.QSqlQuery('SELECT * from tblBehandlung')
    #mdl.setQuery(qry)
    mdl.setEditStrategy(qtdb.QSqlTableModel.OnFieldChange)
    mdl.select()
    #mdl.setHeaderData(0,qtc.Qt.Horizontal,'pkPerson')
    self.tbl=view=qtw.QTableView()
    view.setModel(mdl)
    vh=view.verticalHeader()
    vh.setDefaultSectionSize(22)
    #vh.setCascadingSectionResizes(True)
    vh.setMinimumSectionSize(16)
    loF.addRow('Behandlungen',view)

    #for txt,func in (("Behandlungen",self.OnWndTreatment),("Rechnungen",self.OnWndInvoice),("Report Treatment",self.OnRptTreatmentProgress),("Save",self.OnSave)):
    for txt,func in (("Report Invoice",self.OnRptInvoice),("Save",self.OnSave)):
      btn=qtw.QPushButton(txt,self)
      if func is not None:
        btn.clicked.connect(func)
      loH.addWidget(btn)

  def cbSelChanged(self,i):
    cb=self.cbRng
    curData=cb.currentData()
    #print("cbSelChanged index",i,"selection changed ",cb.currentIndex(),str(curData),cb.currentText())
    if cb.currentData() is None:
      print("TODO:New Person inserted")
      cb.removeItem(i)
    else:
      dbc=self.dbc
      d=dbc.execute('SELECT * FROM tblRechnung WHERE pkRechnung=%d'%curData).fetchone()
      #print(d)
      for w,d in zip(self.fldLst,d):
        if d is None:
          d=''
        else:
          d=str(d)
        w.setText(d)
    mdl=self.mdl
    qry=qtdb.QSqlQuery('SELECT pkBehandlung,fkRechnung,fkPerson,datBehandlung,Dauer,Stundenansatz,Bemerkung,TarZif FROM tblBehandlung WHERE fkRechnung=%d'%curData)
    mdl.setQuery(qry)


  def OnRptInvoice(self):
    print('OnRptInvoice')
    app=qtw.QApplication.instance()
    curData=self.cbRng.currentData()
    app.mkb.report_invoice('pkRechnung=%d'%curData)

  def OnSave(self):
    #d=dbc.execute('SELECT * FROM tblPerson WHERE pkPerson=%d'%curData).fetchone()
    #print(d)
    for w in self.fldLst:
      fld=w.windowTitle()
      txt=w.text()
      print('UPDATE %s with %s'%(fld,txt))

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
    act=AddMenuAction(self,mnEdit,"Table Clients",self.OnTblClients)
    act=AddMenuAction(self,mnEdit,"Table Treatments",self.OnTblTreatments)
    act=AddMenuAction(self,mnEdit,"Table Invoices",self.OnTblInvoices)
    act=AddMenuAction(self,mnEdit,"Client",self.OnQryClient)
    act=AddMenuAction(self,mnEdit,"Treatment",self.OnQryTreatment)
    act=AddMenuAction(self,mnEdit,"Invoice",self.OnQryInvoice)
    act=AddMenuAction(self,mnEdit,"New Invoice",self.OnQryNewInvoice)
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

  def OnTblClients(self):
    print("OnTblClients")
    wnd=WndSqlTblView('TblClients:','tblPerson')
    #wnd=WndSqlTblView('TblClients:','SELECT * FROM tblPerson')
    #wnd=WndSqlTblView('TblClients:',
    #                  'SELECT RngAnrede,RngNachname,RngVorname,RngAdresse,RngAdresse1,PLZ,Ort FROM tblPerson ORDER BY RngNachname,RngVorname',
    #                  geometry=(100,100,1200,700))
    #wnd.tbl.setColumnWidth(2,200)
    for i in range(wnd.mdl.columnCount()):
      wnd.tbl.resizeColumnToContents(i)
    WndChildAdd(wnd)

  def OnTblTreatments(self):
    print("aOnTblTreatments")
    wnd=WndSqlTblView('TblTreatments:','tblBehandlung',geometry=(100,100,1200,700))
    for i in range(wnd.mdl.columnCount()):
      wnd.tbl.resizeColumnToContents(i)
    WndChildAdd(wnd)

  def OnTblInvoices(self):
    print("OnTblInvoices")
    wnd=WndSqlTblView('TblInvoices:','tblRechnung',geometry=(100,100,600,700))
    for i in range(wnd.mdl.columnCount()):
      wnd.tbl.resizeColumnToContents(i)
    WndChildAdd(wnd)

  def OnQryClient(self):
    print("OnQryClient")
    wnd=WndClient('QryClient')
    sub=qtw.QMdiSubWindow()
    sub.setWidget(wnd)
    #sub.setWindowTitle("subwindow"+str(MainWindow.count))
    self.mdi.addSubWindow(sub)
    sub.show()

    #WndChildAdd(wnd)

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
