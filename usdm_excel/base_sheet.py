import pandas as pd
from usdm_excel.id_manager import IdManager
from usdm_excel.cdisc import CDISC

class BaseSheet():

  def __init__(self, sheet, id_manager: IdManager):
    self.sheet = sheet
    self.id_manager = id_manager

  def clean_cell(self, row, index, field_name):
    try:
      if pd.isnull(row[field_name]):
        return ""
      else:
        return str(row[field_name]).strip()
    except Exception as e:
      print("Clean cell error (%s) for field '%s' in row %s" % (e, field_name, index + 1))
      return ""

  def clean_cell_unnamed(self, rindex, cindex):
    try:
      if pd.isnull(self.sheet.iloc[rindex, cindex]):
        return ""
      else:
        return self.sheet.iloc[rindex, cindex].strip()
    except Exception as e:
      print("Clean cell unnamed error (%s) for cell [%s, %s]" % (e, rindex + 1, cindex + 1))
      return ""

  def clean_cell_unnamed_new(self, rindex, cindex):
    try:
      if pd.isnull(self.sheet.iloc[rindex, cindex]):
        return "", True
      else:
        return self.sheet.iloc[rindex, cindex].strip(), False
    except Exception as e:
      print("Clean cell unnamed error (%s) for cell [%s, %s]" % (e, rindex + 1, cindex + 1))
      return "", True

  def clean_cell_unnamed_with_previous(self, rindex, cindex, first_cindex):
    try:
      i = cindex
      while i >= first_cindex:
        if pd.isnull(self.sheet.iloc[rindex, i]):
          i -= 1
        else:
          return self.sheet.iloc[rindex, i].strip(), False
      print("Clean cell unnamed with previous is blank for cell [%s, %s]" % (rindex + 1, cindex + 1))
      return "", True
    except Exception as e:
      print("Clean cell unnamed with previous error (%s) for cell [%s, %s]" % (e, rindex + 1, cindex + 1))
      return "", True

  # def process_cdisc(self, value):
  #   print("CDISC", value)
  #   parts = value.split("=")
  #   return self.cdisc_code(code=parts[0].strip(), decode=parts[1].strip())

  def cdisc_code_cell(self, value):
    parts = value.split("=")
    try:
      return CDISC(self.id_manager).code(code=parts[0].strip(), decode=parts[1].strip())
    except Exception as e:
      print("CDISC code error (%s) for data %s" % (e, value))
      return None

  def cdisc_code_set_cell(self, items):
    results = []
    parts = items.split(",")
    for part in parts:
      result = self.cdisc_code_cell(part)
      if not result == None:
        results.append(result)
    return results

  # def double_link(self, items, id, prev, next):
  #   #print("DL1", items, id, prev, next)
  #   for idx, item in enumerate(items):
  #     if idx == 0:
  #       print("DL2", item, prev, item.keys())
  #       if prev in item:
  #         print("DL3", item[prev])
  #       item[prev] = None
  #     else:
  #       uuid = items[idx-1][id]
  #       item[prev] = uuid
  #     if idx == len(items)-1:  
  #       item[next] = None
  #     else:
  #       uuid = items[idx+1][id]
  #       item[next] = uuid