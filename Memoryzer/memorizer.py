import json
import os



MEMORY_FILE_NAME = os.path.join(os.path.dirname(__file__), "..", "Persistence", "data", "user_memory.json")

class Memoryzer:
  def __init__(self):
    with open(MEMORY_FILE_NAME, "r", encoding="utf-8") as memoryFile:
      self.memoryData = json.load(memoryFile)
  
  def loadMemory(self) -> list:
    with open(MEMORY_FILE_NAME, "r", encoding="utf-8") as memoryFile:
      self.memoryData = json.load(memoryFile)
    return self.memoryData
  
  def saveMemory(self) -> None:
    with open(MEMORY_FILE_NAME, "w", encoding="utf-8") as memoryFile:
      json.dump(self.memoryData, memoryFile, indent=2, ensure_ascii=False)
  
  def __buildUserMemoryFormatedList(self) -> str:
    formatedList = ""
    for memoryItem in self.memoryData:
      formatedList += f'- {memoryItem}\n'
    return formatedList
  
  def getUserMemoryFormatedList(self) -> str:
    return self.__buildUserMemoryFormatedList()
  
  def processNewMemory(self, information: str) -> None:
    # TODO: Vai checar o prompt e tentar extrair novas memórias e adicionar-las
    pass
  
memoryzerInstance = Memoryzer()