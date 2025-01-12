from utils import debug

class Action:
  def __init__(self, keyword, description, action, *argsTypes, willRespond=True):
    self.keyword = keyword
    self.description = description
    self.action = action
    self.argsTypes = argsTypes
    self.args = []
    self.willRespond = willRespond

  def _checkTyping(self, args):
    if len(args) != len(self.argsTypes):
      raise Exception(f'Expected {len(self.argsTypes)} arguments, but got {len(args)}')
    for i in range(len(args)):
      if type(args[i]) != self.argsTypes[i]:
        try:
          args[i] = self.argsTypes[i](args[i])
        except Exception as e:
          raise Exception(f'Expected argument {i} to be of type {self.argsTypes[i]}, but got {type(args[i])}')

  def connectArgs(self, args):
    debug(f'Connecting args: {args}')
    self.args = args

  def __call__(self):
    self._checkTyping(self.args)
    if self.args:
      self.action(*self.args)
    else:
      self.action()
    return self.willRespond