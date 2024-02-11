from .elements import Elements
from usdm_excel.base_sheet import BaseSheet

class TemplateBase():

  def __init__(self, parent: BaseSheet, study):
    self.parent = parent
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.elements = Elements(parent, study)
    self.methods = [func for func in dir(self.__class__) if callable(getattr(self.__class__, func)) and not func.startswith("_")]

  def valid_method(self, name):
    return name in self.methods
  
  def _reference(self, item, attribute):
    return f'<usdm:ref klass="{item.__class__.__name__}" id="{item.id}" attribute="{attribute}"></usdm:ref>'

  def _add_checking_for_tag(self, doc, tag, text):
    if text.startswith(f"<{tag}>"):
      doc.asis(text)
    else:
      with doc.tag('p'):
        doc.asis(text)