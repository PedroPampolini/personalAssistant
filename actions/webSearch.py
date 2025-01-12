from actions.action import Action
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from bot import llmRequest
import env
from utils import debug
from bot import tts
from contants import InteractionType

def searchOnGoogle(query):
  options = webdriver.ChromeOptions()
  options.add_argument('headless')
  driver = webdriver.Chrome(options=options)
  driver.get('https://www.google.com/search?q=' + '+'.join(query.split()))

  links = driver.find_elements(By.CSS_SELECTOR, 'a[jsname="UWckNb"]')
  results = []
  for link in links:
      href = link.get_attribute('href')
      h3 = link.find_element(By.CSS_SELECTOR, 'h3')
      results.append((h3.text, href))

  results = [r for r in results if 'translate.google' not in r[1]]
  driver.quit()
  return results

def get_text_from_url(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  text = soup.get_text()
  text = ' '.join(text.split())   # Remove extra spaces
  return text

def search(query):
  results = searchOnGoogle(query)
  maxResults = 5
  index = 0
  textResult = ''
  for title, url in results:
    if index >= maxResults:
      break
    try:
      text = get_text_from_url(url)
      textResult += f"Titulo: {title}\n"
      textResult += f"Conteudo: {text}\n========================================\n"
      index += 1
    except Exception as e:
      pass

  return textResult


def SearchOnWeb(query):
  debug(f'Pesquisando na internet: {query}')
  resumePrompt = 'Vou te entregar um texto que retirei de alguns sites na internet e preciso que você faça um resumo informativo em forma de 1 parágrafo curto mostrando as principais informações, só faça o resumo informativo para mim. O texto é o seguinte: '
  results = search(query)
  prompt = resumePrompt + '\n' + results
  data = [{'role': 'user', 'content': prompt}]
  response = llmRequest.sendRequest(data)
  if env.INTERACTION_TYPE == InteractionType.TEXT:
    print(f"web: {response}")
  else:
    tts.say(response)

SearchOnWebAction = Action('searchOnWeb', 'Realiza uma pesquisa na internet e exibe o conteúdo, action para quando não se tem a informação e é necessário buscar na internet Você DEVE UTILIZAR essa função SEMPRE que necessário, principalmente quando você não tem a informação solicitada. Parâmetros: 1) query: tipo string - uma string de texto curta com o que vai ser pesquisado na internet.', SearchOnWeb, str, willRespond=False)