from typing import Union
from .api_base_model import ApiBaseModel
from .code import Code

class Timing(ApiBaseModel):
  timingId: str
  timingType: Code
  timingValue: str
  timingDescription: Union[str, None] = None
  timingRelativeToFrom: Code
  relativeFromScheduledInstanceId: Union[str, None] = None
  relativeToScheduledInstanceId: Union[str, None] = None
  timingWindowLower: Union[str, None] = None
  timingWindowUpper: Union[str, None] = None
  timingWindow: Union[str, None] = None
