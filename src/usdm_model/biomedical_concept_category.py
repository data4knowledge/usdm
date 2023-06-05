from typing import List
from .api_base_model import ApiBaseModel

class BiomedicalConceptCategory(ApiBaseModel):
  biomedicalConceptCategoryId: str
  bcCategoryChildIds: List[str] = []
  bcCategoryName: str
  bcCategoryDescription: str
  bcCategoryMemberIds: List[str] = []
