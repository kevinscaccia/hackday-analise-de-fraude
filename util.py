from faker import Faker
import numpy as np
import random
import re
#
PROB_EMAIL_FRAUDE_EMAIL_COM_NOME = 0.2
PROB_EMAIL_FRAUDE_SOBRENOME_CERTO = 0.2
PROB_EMAIL_FRAUDE_EMAIL_ERRADO = 0.5 
#
PROB_EMAIL_REAL_EMAIL_COM_NOME = 0.8


def gera_nome_e_email(fake, fraude=False):
  first_name = fake.first_name()
  last_name = fake.last_name()
  domain_name = fake.domain_name()
  #
  email = ""
  if fraude:
    # pega email de outra pessoa
    if gera_prob(PROB_EMAIL_FRAUDE_EMAIL_ERRADO):
      email = fake.email()
    else:
      # email com dados certos
      if gera_prob(PROB_EMAIL_FRAUDE_EMAIL_COM_NOME):
        email += trata_string(first_name) + "."
      last_name_c = trata_string(last_name)
      email = f"{email}{last_name_c}@{domain_name}"
  else:
    # email com dados certos
    if gera_prob(PROB_EMAIL_REAL_EMAIL_COM_NOME):
      email += trata_string(first_name) + "."
    #
    last_name_c = trata_string(last_name)
    email = f"{email}{last_name_c}@{domain_name}"


  return first_name, last_name, email


#
# Gera probabilidade 
#  - retorna true com probabilidade = prob
def gera_prob(prob):
  return random.random() <= prob


def trata_string(string):
  string = re.sub('[^A-Za-z0-9]+', '', string)
  string = string.replace(" ","")
  return string.lower()

  
# from gerador_endereco import *

# def getAddress(cep):
#     r = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
#     r.status_code
#     return r.json()


