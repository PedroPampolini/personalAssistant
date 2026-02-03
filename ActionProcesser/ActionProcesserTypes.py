from typing import *

class Action(TypedDict):
  name: str
  description: str
  parameters: Dict[str, Any]