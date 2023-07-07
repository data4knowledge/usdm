from typing import List, Union
from .api_base_model import ApiNameDescriptionModel
from .code import Code
from .transition_rule import TransitionRule


class Encounter(ApiNameDescriptionModel):
  previousEncounterId: Union[str, None] = None
  nextEncounterId: Union[str, None] = None
  encounterType: Union[Code, None] = None
  encounterEnvironmentalSetting: Union[Code, None] = None
  encounterContactModes: List[Code] = []
  transitionStartRule: Union[TransitionRule, None] = None
  transitionEndRule: Union[TransitionRule, None] = None
  encounterScheduledAtTimingId: Union[str, None] = None
