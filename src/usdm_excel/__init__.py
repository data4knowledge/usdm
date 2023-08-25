import json
from usdm_excel.id_manager import id_manager
from usdm_excel.configuration_sheet import ConfigurationSheet
from usdm_excel.study_sheet.study_sheet import StudySheet
from usdm_excel.nodes_and_edges import NodesAndEdges
from usdm_excel.cross_ref import cross_references
from usdm_excel.ct_version_manager import ct_version_manager
from usdm_excel.errors.errors import error_manager, Errors
from usdm_excel.option_manager import option_manager as om # Using 'om' as a name clash in pytest
from usdm_excel.cdisc_biomedical_concept import cdisc_bc_library

class USDMExcel():

  FULL_VIEW = NodesAndEdges.FULL
  TIMELINE_VIEW = NodesAndEdges.TIMELINE

  def __init__(self, file_path):
    id_manager.clear()
    cross_references.clear()
    ct_version_manager.clear()
    error_manager.clear()
    om.clear()
    self.configuration = ConfigurationSheet(file_path)
    self.study = StudySheet(file_path)

  def identifier(self):
    study = self.study.the_study()
    if study == None:
      return None
    else:
      return study.study_identifier()

  def the_study(self):
    return self.study.the_study()
  
  def to_json(self):
    try:
      raw_json = self.study.api_root().to_json()
    except Exception as e:
      message = f"Failed to generate JSON output, exception {e}"
      error_manager.add(None, None, None, message)
      raw_json = json.dumps({'error': message}, indent = 2)
    return raw_json

  def to_html(self):
    try:
      html = self.study.to_html()
    except Exception as e:
      message = f"Failed to generate HTML output, exception {e}"
      error_manager.add(None, None, None, message)
      html = f"<p>{message}</p>"
    return html

  def to_pdf(self):
    try:
      bytes = self.study.to_pdf()
    except Exception as e:
      message = f"Failed to generate PDF output, exception {e}"
      error_manager.add(None, None, None, message)
      bytes = bytearray()
      bytes.extend(map(ord, message))    
    return bytes

  def to_nodes_and_edges(self, view=FULL_VIEW):
    return NodesAndEdges(self.study.the_study(), view).nodes_and_edges()

  def errors(self):
    return error_manager.dump(Errors.WARNING)