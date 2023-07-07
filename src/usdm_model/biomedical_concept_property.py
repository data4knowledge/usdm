from typing import List
from .alias_code import AliasCode
from .api_base_model import ApiIdModel
from .response_code import ResponseCode

class BiomedicalConceptProperty(ApiIdModel):
  bcPropertyName: str
  bcPropertyRequired: bool
  bcPropertyEnabled: bool
  bcPropertyDatatype: str
  bcPropertyResponseCodes: List[ResponseCode] = []
  bcPropertyConceptCode: AliasCode
