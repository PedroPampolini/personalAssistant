from actions.lockWindows import LockWindowsAction
from actions.saveLog import SaveLogAction
from actions.reminder import ReminderAction
from actions.closeAssistant import CloseAssistantAction
from actions.debugPopup import DebugPopupAction
from actions.takePicture import TakePictureAction
from actions.exec import ExecFunction
from actions.webSearch import SearchOnWebAction

allActions = {action.keyword: action for action in [
  LockWindowsAction,
  SaveLogAction,
  ReminderAction,
  CloseAssistantAction,
  DebugPopupAction,
  TakePictureAction,
  #ExecFunction,
  SearchOnWebAction,
  ]}

