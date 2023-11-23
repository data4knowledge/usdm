from usdm_excel.base_sheet import BaseSheet
from usdm_excel.id_manager import id_manager
from usdm_excel.cross_ref import cross_references
import traceback
from usdm_model.study_design_population import StudyDesignPopulation

class StudyDesignPopulationSheet(BaseSheet):

  def __init__(self, file_path):
    try:
      super().__init__(file_path=file_path, sheet_name='studyDesignPopulations')
      self.population = None
      for index, row in self.sheet.iterrows():
        level = self.read_cell_by_name(index, 'name')
        name = self.read_cell_by_name(index, 'name')
        description = self.read_description_by_name(index, ['description', 'populationDescription']) # Allow multiple names for column
        label = self.read_cell_by_name(index, 'label', default="")
        required_number = self.read_cell_by_name(index, "plannedNumberOfParticipants")
        recruit_number = self.read_cell_by_name(index, "plannedNumberOfParticipants")
        range = self.read_cell_by_name(index, "AgeOfParticipants")
        max = self.read_cell_by_name(index, "plannedMaximumAgeOfParticipants")
        codes = self._build_codes(row, index)
        try:
          pop = StudyDesignPopulation(id=id_manager.build_id(StudyDesignPopulation),
            name=name,
            description=description,
            label=label,
            plannedNumberOfParticipants=number,
            plannedMinimumAgeOfParticipants=min,
            plannedMaximumAgeOfParticipants=max,
            plannedSexOfParticipants=codes
          )
        except Exception as e:
          self._general_error(f"Failed to create StudyDesignPopulation object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          cross_references.add(name, pop)
          self.population = pop
        
    except Exception as e:
      self._general_error(f"Exception [{e}] raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")

  def _build_codes(self, row, index):
    code = self.read_cdisc_klass_attribute_cell_by_name('StudyDesignPopulation', "plannedSexOfParticipants", index, "plannedSexOfParticipants")
    return [code] if code else []
      

        