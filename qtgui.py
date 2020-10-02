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

  wpWnd=wp.MainWindow()
  wpWnd.record_open(1)
  WndChildAdd(wpWnd)

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
    #cb.model()
    #cb.view()

    cpl=qtw.QCompleter(cmpNaVo)
    #cpl=qtw.QCompleter(cb.model())
    cb.setCompleter(cpl)
    cb.currentIndexChanged.connect(self.cbSelChanged)

    loF.addRow('Suche',cb)
    self.fldLst=fldLst=list()

    for txt in ('pkPerson','RngAnrede','RngNachname','RngVorname','RngAdresse','RngAdresse1','RngAdresse2','PLZ','Ort','Nachname','Vorname','Tel1','Tel2','datGeb','eMail','AHVNr'):
      w=qtw.QLineEdit()
      fldLst.append(w)
      loF.addRow(txt,w)

    w=qtw.QTextEdit()
    fldLst.append(w)
    loF.addRow('Bemerkung',w)

    for txt in ("Behandlungen","Rechnungen","Button"):
      btn=qtw.QPushButton(txt,self)
      loH.addWidget(btn)

  def cbSelChanged(self,i):
    cb=self.cbNaVo
    curData=cb.currentData()
    print("cbSelChanged index",i,"selection changed ",cb.currentIndex(),str(curData),cb.currentText())
    if cb.currentData() is None:
      print("TODO:New Person inserted")
      cb.removeItem(i)
    else:
      dbc=self.dbc
      d=dbc.execute('SELECT * FROM tblPerson WHERE pkPerson=%d'%curData).fetchone()
      print(d)
      for w,d in zip(self.fldLst,d):
        if d is None:
          d=''
        else:
          d=str(d)
        w.setText(d)


#class WndMain(qtw.QMainWindow):
class WndMain(qtw.QWidget):

  def __init__(self):
    super(WndMain,self).__init__()
    self.setGeometry(150,150,500,300)
    self.setWindowTitle("MoKaBu")
    #self.setWindowIcon(qtw.QIcon('pythonlogo.png'))

    lbl=qtw.QLabel('Thierry Zamofing\nth.zamofing@gmail.com\n(c) 2020',self)
    #lbl.setText()
    lbl.move(50,20)
    #mainMenu=self.menuBar() #this is how it is done on QMainWindow
    self.mainMenu=mainMenu=qtw.QMenuBar(self)
    #self.statusBar()  #this is how it is done on QMainWindow
    #self.statusBar=qtw.QStatusBar(self)
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
    WndChildAdd(wnd)

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
