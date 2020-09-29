#!/usr/bin/python3
#https://www.tutorialspoint.com/pyqt/pyqt_hello_world.htm

import sys
import PyQt5.QtWidgets as qtw
import mokabu


def MainApp(mkb):
  app=qtw.QApplication(sys.argv)
  app.mkb=mkb
  GUI=WndMain()
  sys.exit(app.exec_())


#Here a clean Main Window implementation.
#QMainWindow has compares to a QWidgets by default dockerbars for toolbars statusbar and menuBar
# #https://www.learnpyqt.com/courses/start/basic-widgets/
# http://zetcode.com/gui/pyqt5/menustoolbars/
def AddMenuAction(widget,parentMenu,txt,func):
  actQuit=qtw.QAction(txt,widget)
  actQuit.triggered.connect(func)
  parentMenu.addAction(actQuit)
  return actQuit

class WndMain(qtw.QWidget):

  def __init__(self):
    super(WndMain,self).__init__()
    self.setGeometry(50,50,500,300)
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
    act=AddMenuAction(self,mnEdit,"Table Clients",self.OnQuit)
    act=AddMenuAction(self,mnEdit,"Table Treatment",self.OnQuit)
    act=AddMenuAction(self,mnEdit,"Table Invoice",self.OnQuit)
    act=AddMenuAction(self,mnEdit,"Client",self.OnQuit)
    act=AddMenuAction(self,mnEdit,"Treatment",self.OnQuit)
    act=AddMenuAction(self,mnEdit,"Invoice",self.OnQuit)
    act=AddMenuAction(self,mnEdit,"New Invoice",self.OnQuit)
    mnRpt=mainMenu.addMenu('&Report')
    act=AddMenuAction(self,mnRpt,"Invoices",self.OnRepInvoices)
    self.show()

  def OnQuit(self):
    print("whooaaaa so custom!!!")
    sys.exit()

  def OnRepInvoices(self):
    print("OnRepInvoices!!!")
    app=qtw.QApplication.instance()
    app.mkb.report_invoice()




#https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlRelationalTableModel.html
#https://doc.qt.io/qtforpython/PySide2/QtSql/QSqlTableModel.html
#TODO:
# quite generic QSqlTableModel UI QSqlRelationalTableModel


if __name__=='__main__':

  MainApp(None)
