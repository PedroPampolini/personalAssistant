from actions.action import Action

def Exec(*code):
  # unifica os parâmetros em uma string
  code = ' '.join(code)
  print(eval(code))

ExecFunction = Action('exec', 'Executa um código qualquer em python. Parâmetros: 1) code: tipo string - o código em python que deve ser executado, é uma string com puramente qualquer código, estando atendo à quebras de linhas e identamento.', Exec, str)
