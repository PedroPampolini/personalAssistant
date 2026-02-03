from typing import *

class GptMessage(TypedDict):
  role: Literal["user", "assistant", "system"]
  content: str
  
GptChatHistory = List[GptMessage]