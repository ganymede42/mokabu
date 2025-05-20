# raw text of TarZif for psychologie:
#https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fwww.psychologie.ch%2Fsites%2Fdefault%2Ffiles%2F2022-06%2F20220602_psytarif_einfuehrungsversion_tarifstruktur_de.xlsx&wdOrigin=BROWSELINK
# raw text of TarZif for psychologie IV -> document from IV

import logging
_log=logging.getLogger(__name__)
import yaml

def tuple_constructor(loader, node):
  # Load the sequence of values from the YAML node
  values=loader.construct_sequence(node)
  # Return a tuple constructed from the sequence
  return tuple(values)

# Register the constructor with PyYAML
yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:seq', tuple_constructor)

class Lut:
  @classmethod
  def open(cls):
    dict()
    with open('TarZif.yaml', 'r') as fh:
      cls._lutTarZif=lut=yaml.safe_load(fh)
    pass

  @classmethod
  def tar_zif(cls,tz):
    return cls._lutTarZif[tz]

Lut.open()

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(module)s:%(lineno)d:%(funcName)s:%(message)s ')
  for k,v in Lut._lutTarZif.items():
    print(k,v)
  pass
