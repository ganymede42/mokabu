#!/usr/bin/python3
#https://www.tutorialspoint.com/pyqt/pyqt_hello_world.htm

import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import mokabu

def MainApp(mkb):
  app=qtw.QApplication(sys.argv)
  app.mkb=mkb
  mainWnd=WndMain() #must be assigned to a variable, else it 'selfsdestructs' before opening
  mainWnd.show()
  app.wndTop=set()
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

  def __init__(self,*args,**kwargs):
    super(WndSqlTblView,self).__init__(*args,**kwargs)
    self.setGeometry(50,50,500,300)
    self.setWindowTitle("MoKaBu")

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

  def closeEvent(self, event):
    print('closeEvent')
    app=qtw.QApplication.instance()
    if len(app.wndTop)>0:
      print('close cild windows first',app.wndTop)
      event.ignore()
      #app.wndTop.clear()

  def OnQuit(self):
    print("whooaaaa so custom!!!")
    sys.exit()

  def OnTblClients(self):
    print("OnTblClients")
    wnd=WndSqlTblView()
    WndChildAdd(wnd)

  def OnTblTreatments(self):
    print("aOnTblTreatments")
    wnd=WndSqlTblView()
    WndChildAdd(wnd)

  def OnTblInvoices(self):
    print("OnTblInvoices")
    wnd=WndSqlTblView()
    WndChildAdd(wnd)

  def OnQryClient(self):
    print("OnQryClient")
    wnd=qtw.QWidget()
    WndChildAdd(wnd)

  def OnQryTreatment(self):
    print("OnQryTreatment")
    wnd=qtw.QWidget("WndQryTreatment")
    WndChildAdd(wnd)

  def OnQryInvoice(self):
    print("OnQryInvoice")
    wnd=qtw.QWidget()
    WndChildAdd(wnd)

  def OnQryNewInvoice(self):
    print("OnQryNewInvoice")
    app=qtw.QApplication.instance()
    #app.mkb

  def OnRepInvoices(self):
    print("OnRepInvoices")
    app=qtw.QApplication.instance()
    app.mkb.report_invoice()


#https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlRelationalTableModel.html
#https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlTableModel.html
#TODO:
# quite generic QSqlTableModel UI QSqlRelationalTableModel


if __name__=='__main__':

  MainApp(None)
