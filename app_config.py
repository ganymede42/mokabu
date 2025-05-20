#TODO:
# currently 2 settings/configs are used
# QSettings -> cat ~/.config/Paul\ Scherrer\ Institut/SwissMX.conf
# yaml -> swissmx.yaml
# QSettings are changed by program
# #yaml is fixed and not altened by program

import logging

_log = logging.getLogger(__name__)

from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
import json

class MyJsonEncoder(json.JSONEncoder):
  """ Special json encoder for numpy types """
  def default(self, obj):
    #if isinstance(obj, np.integer):
    #  return int(obj)
    #elif isinstance(obj, np.floating):
    #  return float(obj)
    #elif isinstance(obj, np.ndarray):
    #  return obj.tolist()
    #elif type(obj) not in (dict,list,str,int):
    #  _log.error('dont know how to json')
    #  return repr(obj)
    return json.JSONEncoder.default(self, obj)

class AppCfg(QSettings):
  SETTINGS='settings'

  def __init__(self):
    super(AppCfg, self).__init__("ganymede", "Mokabu")
    keys = self.allKeys()
    # Dump config to debug
    #for k in keys:
    #  print(k, self.value(k))

    #set default keys if not existing

    dflt=[]
    #dflt.append(('Key1/Key2/Key3', 'value1'))
    if AppCfg.SETTINGS not in keys:

      d={
        'images':{
          'main':'Logo_Monika.png',
          'small':'Logo_Monika_s.png',
          'icon':'logo_monika.ico',
          'icon':'logo_monika.ico',
          'signature':'signature.png'
        },
        'person':{
          'vorname':'Monika',
          'name':'Kast Perry',
          'email':'monika.kast-perry@psychologie.ch',
          'telM':'+41 76 335 72 79',
          'adr':'Weihermattstrasse 11a',
          'plz':'5242',
          'ort':'Birr',
          'qrFmt':'SPC\n0200\n1\nCH6000781622418862000\nS\nPraxis Weiterkommen Monika Kast Perry\nWeihermattstrasse 11a\n\n5242\nBirr\nCH\n\n\n\n\n\n\n\n%.2f\nCHF\n\n\n\n\n\n\n\nNON\n\n%s\nEPD',
          'GLN':7601007566037,
          'UID':'CHE327073453',
          'ZSR':'I989819',
        },
        #'CHE327073453_zh':{
        #  'adr':'Riedthofstrasse 100',
        #  'plz':'8105',
        #  'ort':'Regensdorf',
        #  'GLN':7601007566037,
        #  'ZSR':'D749131',
        #},
        'rechnung':{
          'dftTpl':0x28,
          'header':'''\
<font size="7"><b>Monika Kast Perry</b><br/>
Dr. phil., Fachpsychologin<br/>
für Kinder- & Jugendpsychologie FSP<br/>
eidg. anerkannte Psychotherapeutin.<br/>
Weihermattstrasse 11a · 5242 Birr · +41 76 335 72 79<br/>
monika.kast-perry@psychologie.ch · praxis-weiterkommen.com</font>''',
          'default':'''\
Ich bitte Sie, den Betrag von SFr. %.2f innert 30 Tagen auf folgendes Konto zu überweisen:<br/>
St. Galler Kantonalbank, IBAN-Nr. CH60 0078 1622 4188 6200 0<br/>''',
          'mahnung1':'''\
<b>Zahlungserinnerung</b><br/>
Es dürfte Ihrer Aufmerksamkeit entgangen sein, dass die nachstehend aufgeführten Rechnungsposten noch offen sind. Ich bitte Sie, die fälligen Rechnungsbeträge innert 10 Tagen einzuzahlen und danke Ihnen für die fristgerechte Überweisung. Sollte sich Ihre Zahlung mit diesem Schreiben gekreuzt haben, betrachten Sie es bitte als gegenstandslos.<br/><br/>
Bitte überweisen Sie, den Betrag von SFr. %.2f auf folgendes Konto:<br/>
St. Galler Kantonalbank, IBAN-Nr. CH60 0078 1622 4188 6200 0<br/>''',
          'mahnung2':'''\
<b>2. Mahnung</b><br/>
Den unten stehenden Rechnungsposten haben Sie trotz Zahlungserinnerung nicht bezahlt. Sie ersparen sich Unannehmlichkeiten und weitere Kosten, wenn Sie den fälligen Betrag innert 15 Tagen überweisen. Sollte sich Ihre Zahlung mit diesem Schreiben gekreuzt haben, betrachten Sie es bitte als gegenstandslos.<br/><br/>
Bitte überweisen Sie, den Betrag von SFr. %.2f auf folgendes Konto:<br/>
St. Galler Kantonalbank, IBAN-Nr. CH60 0078 1622 4188 6200 0<br/>''',
          'gruss':'Herzlichen Dank und freundliche Grüsse',
        }
      }
      dflt.append((AppCfg.SETTINGS,d))

    for k,v in dflt:
      _log.warning(f'{k} not defined. use default')
      self.setValue(k,v)

  def sync(self):
    super(AppCfg, self).sync()

  def setValue(self, key: str, val): #overload to debug
    # only simple lists, str, int, float can not be serialized nicely
    t=type(val)
    #if key in (AppCfg.PRS_Z,AppCfg.RNG):
    if t==dict:
      val=json.dumps(val, cls=MyJsonEncoder)
      val=val.replace('"',"'")
    #elif key in (AppCfg.GEO_OPT_CTR,AppCfg.GEO_BEAM_SZ,AppCfg.GEO_BEAM_POS):
    #  if type(val)==np.ndarray:
    #    val=val.tolist()
    #elif type(val)==tuple:
    #  val=list(val)
    #if type(val)==list:
    #  if len(val)==1:val=val[0]
    #  elif len(val)==0: val=''
    return super(AppCfg, self).setValue(key,val)

  def value(self,key,*vargs,**kwargs): #overload to debug
    val=super(AppCfg, self).value(key,*vargs,**kwargs)
    if key in (AppCfg.SETTINGS,):
      val=val.replace("'", '"')
      val=json.loads(val)#, object_hook=MyJsonDecoder)
    #  val=(np.array(val[0]),np.array(val[1]))
    #elif key in (AppCfg.GEO_CAM_TRF,):
    #  val=json.loads(val)#, object_hook=MyJsonDecoder)
    #  val=np.array(val)
    return val

  #@property
  #def value(self):
  #  return super(AppCfg, self).value

  def option(self,key: str) -> bool:
    try:
      return self.value(key, type=bool)
    except:
      _log.error(f"option {key} not known")
    return False

  def toggle_option(self,key: str):
    v = self.value(key, type=bool)
    self.setValue(key, not v)
    self.sync()

# https://doc.qt.io/qtforpython-5/overviews/model-view-programming.html#model-view-programming
# https://doc.qt.io/qtforpython/examples/example_widgets_itemviews_jsonmodel.html
# https://doc.qt.io/qtforpython/examples/example_widgets_tutorials_modelview.html
from typing import Any, Iterable, List, Dict, Union

from PyQt5.QtWidgets import QTreeView, QApplication, QHeaderView
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QObject, Qt, QFileInfo


class TreeItem:
    """A Json item corresponding to a line in QTreeView"""

    def __init__(self, parent: "TreeItem" = None):
        self._parent = parent
        self._key = ""
        self._value = ""
        self._value_type = None
        self._children = []

    def appendChild(self, item: "TreeItem"):
        """Add item as a child"""
        self._children.append(item)

    def child(self, row: int) -> "TreeItem":
        """Return the child of the current item from the given row"""
        return self._children[row]

    def parent(self) -> "TreeItem":
        """Return the parent of the current item"""
        return self._parent

    def childCount(self) -> int:
        """Return the number of children of the current item"""
        return len(self._children)

    def row(self) -> int:
        """Return the row where the current item occupies in the parent"""
        return self._parent._children.index(self) if self._parent else 0

    @property
    def key(self) -> str:
        """Return the key name"""
        return self._key

    @key.setter
    def key(self, key: str):
        """Set key name of the current item"""
        self._key = key

    @property
    def value(self) -> str:
        """Return the value name of the current item"""
        return self._value

    @value.setter
    def value(self, value: str):
        """Set value name of the current item"""
        self._value = value

    @property
    def value_type(self):
        """Return the python type of the item's value."""
        return self._value_type

    @value_type.setter
    def value_type(self, value):
        """Set the python type of the item's value."""
        self._value_type = value

    @classmethod
    def load(
        cls, value: Union[List, Dict], parent: "TreeItem" = None, sort=True
    ) -> "TreeItem":
        """Create a 'root' TreeItem from a nested list or a nested dictonary

        Examples:
            with open("file.json") as file:
                data = json.dump(file)
                root = TreeItem.load(data)

        This method is a recursive function that calls itself.

        Returns:
            TreeItem: TreeItem
        """
        rootItem = TreeItem(parent)
        rootItem.key = "root"

        if isinstance(value, dict):
            items = sorted(value.items()) if sort else value.items()

            for key, value in items:
                child = cls.load(value, rootItem)
                child.key = key
                child.value_type = type(value)
                rootItem.appendChild(child)

        elif isinstance(value, list):
            for index, value in enumerate(value):
                child = cls.load(value, rootItem)
                child.key = index
                child.value_type = type(value)
                rootItem.appendChild(child)

        else:
            rootItem.value = value
            rootItem.value_type = type(value)

        return rootItem


class JsonModel(QAbstractItemModel):
    """ An editable model of Json data """

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._rootItem = TreeItem()
        self._headers = ("key", "value")

    def clear(self):
        """ Clear data from the model """
        self.load({})

    def load(self, document: dict):
        """Load model from a nested dictionary returned by json.loads()

        Arguments:
            document (dict): JSON-compatible dictionary
        """

        assert isinstance(
            document, (dict, list, tuple)
        ), "`document` must be of dict, list or tuple, " f"not {type(document)}"

        self.beginResetModel()

        self._rootItem = TreeItem.load(document)
        self._rootItem.value_type = type(document)

        self.endResetModel()

        return True

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> Any:
        """Override from QAbstractItemModel

        Return data from a json item according index and role

        """
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return item.key

            if index.column() == 1:
              if item.key=='qrFmt':  # change font only for cell(0,0)
                v=item.value.replace('\n','|')
                return v
              else:
                return item.value

        elif role == Qt.EditRole:
            if index.column() == 1:
              if item.key=='qrFmt':  # change font only for cell(0,0)
                v=item.value.replace('\n', '|')
                return v
              else:
                return item.value

    def setData(self, index: QModelIndex, value: Any, role: Qt.ItemDataRole):
        """Override from QAbstractItemModel
        Set json item according index and role
        Args:
            index (QModelIndex)
            value (Any)
            role (Qt.ItemDataRole)
        """
        if role == Qt.EditRole:
            if index.column() == 1:
                item = index.internalPointer()
                if item.key=='qrFmt':  # change font only for cell(0,0)
                  value=value.replace('|','\n')
                item.value = str(value)
                self.dataChanged.emit(index, index, [Qt.EditRole])
                return True
        return False

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override from QAbstractItemModel
        For the JsonModel, it returns only data for columns (orientation = Horizontal)
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._headers[section]

    def index(self, row: int, column: int, parent=QModelIndex()) -> QModelIndex:
        """Override from QAbstractItemModel
        Return index according row, column and parent
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        """Override from QAbstractItemModel
        Return parent index of index
        """

        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self._rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        """Override from QAbstractItemModel
        Return row count from parent index
        """
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent=QModelIndex()):
        """Override from QAbstractItemModel
        Return column number. For the model, it always return 2 columns
        """
        return 2

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """Override from QAbstractItemModel
        Return flags of index
        """
        flags = super(JsonModel, self).flags(index)

        if index.column() == 1:
            return Qt.ItemIsEditable | flags
        else:
            return flags

    def to_json(self, item=None):

        if item is None:
            item = self._rootItem

        nchild = item.childCount()

        if item.value_type is dict:
            document = {}
            for i in range(nchild):
                ch = item.child(i)
                document[ch.key] = self.to_json(ch)
            return document

        elif item.value_type == list:
            document = []
            for i in range(nchild):
                ch = item.child(i)
                document.append(self.to_json(ch))
            return document

        else:
            return item.value

class WndSetting(QTreeView):
  def __init__(self):
    super().__init__()
    app=QApplication.instance()
    self._mdl=mdl=JsonModel()
    self.setModel(mdl)
    doc=app._cfg.value(AppCfg.SETTINGS)
    mdl.load(doc)
    #self.header().setSectionResizeMode(0, QHeaderView.Stretch)
    self.header().setSectionResizeMode(0,QHeaderView.ResizeMode.ResizeToContents,)
    self.setAlternatingRowColors(True)
    #self.resize(900, 500)
    self.setGeometry(100,100,1000,600)


  def closeEvent(self, event): #overloaded function
    _log.info('save app settings')
    doc=self._mdl.to_json()
    app=QApplication.instance()
    app._cfg.setValue(AppCfg.SETTINGS,doc)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG,format='%(levelname)s:%(module)s:%(lineno)d:%(funcName)s:%(message)s ')

  import sys

  app=QApplication([])
  app._cfg=AppCfg()

  view=WndSetting()
  model=JsonModel()
  view.setModel(model)
  doc=app._cfg.value(AppCfg.SETTINGS)
  model.load(doc)
  view.show()

  if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
      QApplication.instance().exec_()
