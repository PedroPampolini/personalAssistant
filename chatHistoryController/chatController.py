from gptService.gptTypes import GptChatHistory
from gptService.gptHelper import getResponse
import os
import json

CHAT_HISTORY_SAVE_FILE = os.path.join(os.path.dirname(__file__), "..", "Persistence", "data", "chat_history.json")

class ChatHistoryController:
  def __init__(self):
    self.chatHistory: GptChatHistory = []

  def addUserMessage(self,content: str) -> None:
    self.chatHistory.append({"role": "user", "content": content})
			
  def addAssistantMessage(self,content: str) -> None:
    self.chatHistory.append({"role": "assistant", "content": content})
			
  def addSystemMessage(self,content: str) -> None:
    self.chatHistory = self.chatHistory[1:] if len(self.chatHistory) > 0 and self.chatHistory[0]["role"] == "system" else self.chatHistory
    self.chatHistory.insert(0, {"role": "system", "content": content})
  
  def loadChatHistory(self, fileName:str = CHAT_HISTORY_SAVE_FILE) -> None:
    try:
      with open(fileName, "r", encoding="utf-8") as f:
        self.chatHistory = json.load(f)
    except FileNotFoundError:
      self.chatHistory = []
 
  def saveChatHistory(self, fileName:str = CHAT_HISTORY_SAVE_FILE) -> None:
    with open(fileName, "w", encoding="utf-8") as f:
      json.dump(self.chatHistory, f, ensure_ascii=False, indent=2)
   
  def getResponse(self) -> GptChatHistory:
    print(f"Chat history before getResponse: {self.chatHistory}")
    responseContent = getResponse(self.chatHistory)
    self.addAssistantMessage(responseContent)
    return self.chatHistory
   
  def clearChatHistory(self) -> None:
    self.chatHistory = []
    
chatHistoryControllerInstance = ChatHistoryController()
	