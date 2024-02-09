import re
from yattag import Doc
from .elements import Elements
from .base import DocumentBase
from usdm_excel.cross_ref import cross_references

class PlainTemplate(DocumentBase):

  def __init__(self, study):
    super().__init__()
    self.study = study
    self.study_version = study.versions[0]
    self.study_design = self.study_version.studyDesigns[0]
    self.protocol_document_version = self.study.documentedBy.versions[0]
    self.elements = Elements(study)

  def title_page(self):
    doc = Doc()
    with doc.tag('table'):
      self._title_page_entry(doc, 'Full Title:', f'{self.elements.study_full_title()}')
      self._title_page_entry(doc, 'Trial Acronym:', f'{self.elements.study_acronym()}')
      self._title_page_entry(doc, 'Protocol Identifier:', f'{self.elements.study_identifier()}')
      self._title_page_entry(doc, 'Version Number:', f'{self.elements.study_version_identifier()}')
      self._title_page_entry(doc, 'Version Date:', f'{self.elements.study_date()}')
      self._title_page_entry(doc, 'Amendment Identifier:', f'{self.elements.amendment()}')
      self._title_page_entry(doc, 'Amendment Scope:', f'{self.elements.amendment_scopes()}')
      self._title_page_entry(doc, 'Trial Phase:', f'{self.elements.study_phase()}')
      self._title_page_entry(doc, 'Short Title:', f'{self.elements.study_short_title()}')
      self._title_page_entry(doc, 'Sponsor Name and Address:', f'{self.elements.organization_name_and_address()}')
      self._title_page_entry(doc, 'Regulatory Agency Identifier Number(s):', f'{self.elements.study_regulatory_identifiers()}')
      self._title_page_entry(doc, 'Spondor Approval Date:', f'{self.elements.approval_date()}')
    result = doc.getvalue()
    return result

  def inclusion(self):  
    return self._criteria("C25532")
  
  def exclusion(self):  
    return self._criteria("C25370")

  def objective_endpoints(self):
    doc = Doc()
    with doc.tag('table', klass='table'):
      for item in self._objective_endpoints_list():
        self._objective_endpoints_entry(doc, item['objective'], item['endpoints'])
    return doc.getvalue()

  def _criteria(self, type):
    doc = Doc()
    with doc.tag('table', klass='table'):
      for criterion in self._criteria_list(type):
        self._critieria_entry(doc, criterion['identifier'], criterion['text'])
    return doc.getvalue()

  def _critieria_entry(self, doc, identifier, entry):
    with doc.tag('tr'):
      with doc.tag('td'):
        self._add_checking_for_tag(doc, 'p', identifier)
      with doc.tag('td'):
        self._add_checking_for_tag(doc, 'p', entry)

  def _objective_endpoints_entry(self, doc, objective, endpoints):
    with doc.tag('tr'):
      with doc.tag('td'):
        self._add_checking_for_tag(doc, 'p', objective)
      with doc.tag('td'):
        for endpoint in endpoints:
          self._add_checking_for_tag(doc, 'p', endpoint)

  def _title_page_entry(self, doc, title, entry):
    with doc.tag('tr'):
      with doc.tag('th'):
        self._add_checking_for_tag(doc, 'p', title)
      with doc.tag('td'):
        self._add_checking_for_tag(doc, 'p', entry)

  def _criteria_list(self, type):
    results = []
    items = [c for c in self.study_design.population.criteria if c.category.code == type ]
    items.sort(key=lambda d: d.identifier)
    for item in items:
      result = {'identifier': item.identifier, 'text': item.text}
      dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', item.dictionaryId)
      if dictionary:
        result['text'] = self._substitute_tags(result['text'], dictionary)
      results.append(result)
    return results

  def _objective_endpoints_list(self):
    results = []
    for item in self.study_design.objectives:
      result = {'objective': item.text, 'endpoints': []}
      dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', item.dictionaryId)
      if dictionary:
        result['objective'] = self._substitute_tags(result['objective'], dictionary)
      for endpoint in item.endpoints:
        dictionary = cross_references.get_by_id('SyntaxTemplateDictionary', endpoint.dictionaryId)
        ep_text = endpoint.text
        if dictionary:
          ep_text = self._substitute_tags(ep_text, dictionary)
        result['endpoints'].append(ep_text)
      results.append(result)
    return results

  def _substitute_tags(self, text, dictionary):
    tags = re.findall(r'\[([^]]*)\]', text)
    for tag in tags:
      if tag in dictionary.parameterMap:
        map = dictionary.parameterMap[tag]
        text = text.replace(f"[{tag}]", f'<usdm:ref klass="{map["klass"]}" id="{map["id"]}" attribute="{map["attribute"]}"/>')
    return text

  def _add_checking_for_tag(self, doc, tag, text):
    if text.startswith(f"<{tag}>"):
      doc.asis(text)
    else:
      with doc.tag('p'):
        doc.asis(text)