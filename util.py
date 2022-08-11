from faker import Faker
import numpy as np
import random
import re
#
PROB_EMAIL_FRAUDE_EMAIL_COM_NOME = 0.2
PROB_EMAIL_FRAUDE_SOBRENOME_CERTO = 0.2
PROB_EMAIL_FRAUDE_EMAIL_ERRADO = 0.5 
PROB_EMAIL_FRAUDE_PRODUTO_NO_EMAIL = 0.5
#
PROB_EMAIL_REAL_EMAIL_COM_NOME = 0.8
PROB_DOMINIO_REAL_DIFERENTE_PADRAO = 0.1
PROB_DOMINIO_FRAUDE_DIFERENTE_PADRAO = 0.2
PROB_EMAIL_FRAUDE_NUMERO_NO_EMAIL = 0.4
MAX_NUMEROS_EMAIL_FRAUDE = 9999999
DOMINIOS_VALIDOS = ['gmail.com','globo.com','outlook.com','bol.com','hotmail.com','yahoo.com']



def gera_nome_e_email(fake, produto, fraude=False):
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

      if not gera_prob(PROB_DOMINIO_FRAUDE_DIFERENTE_PADRAO):
        domain_name = random.choice(DOMINIOS_VALIDOS)

      

      # produto no email
      if gera_prob(PROB_EMAIL_FRAUDE_PRODUTO_NO_EMAIL) and len(produto) > 0:
        email = f"{trata_string(produto)}.{last_name_c}@{domain_name}"
      else:
        email = f"{email}{last_name_c}@{domain_name}"
      #
      if gera_prob(PROB_EMAIL_FRAUDE_NUMERO_NO_EMAIL):
        num = np.random.randint(999, MAX_NUMEROS_EMAIL_FRAUDE)
        email = str(num) + email

  else:
    # email com dados certos
    if gera_prob(PROB_EMAIL_REAL_EMAIL_COM_NOME):
      email += trata_string(first_name) + "."
    #
    last_name_c = trata_string(last_name)
  
    if not gera_prob(PROB_DOMINIO_REAL_DIFERENTE_PADRAO):
      domain_name = random.choice(DOMINIOS_VALIDOS)
    
    email = f"{email}{last_name_c}@{domain_name}"


  return first_name, last_name, email


#
# Gera probabilidade 
#  - retorna true com probabilidade = prob
def gera_prob(prob):
  return random.random() <= prob


def gera_vazio(campo, prob):
  if gera_prob(prob):
    return campo
  return ""

def trata_string(string):
  string = re.sub('[^A-Za-z0-9]+', '', string)
  string = string.replace(" ","")
  return string.lower()


def get_ceps():
    ceps = []
    with open('address.txt') as f:
        for line in f.readlines():
            formatted_line = line.replace('\n', '').split("	")
            ceps.append(formatted_line[0])
    return ceps


def get_addresses():
    address_by_cep = {}
    with open('address.txt') as f:
        for line in f.readlines():
            formatted_line = line.replace('\n', '').split("	")
            cep = formatted_line[0]
            city = formatted_line[1].split("/")[0]
            state = formatted_line[1].split("/")[1]
            neighborhood = formatted_line[2]
            street = formatted_line[3]
            address_by_cep[cep] = {
                'city': city,
                'state': state,
                'neighborhood': neighborhood,
                'street': street,
            }
    return address_by_cep

# Src: https://github.com/arthurdejong/python-stdnum/blob/master/stdnum/luhn.py
def imei_checksum(number, alphabet='0123456789'):
    """
    Calculate the Luhn checksum over the provided number.
    The checksum is returned as an int.
    Valid numbers should have a checksum of 0.
    """
    n = len(alphabet)
    number = tuple(alphabet.index(i)
                   for i in reversed(str(number)))
    return (sum(number[::2]) +
            sum(sum(divmod(i * 2, n))
                for i in number[1::2])) % n


def imei_calc_check_digit(number, alphabet='0123456789'):
    """Calculate the extra digit."""
    check_digit = imei_checksum(number + alphabet[0])
    return alphabet[-check_digit]


def get_imei(phone_number):
    imei = phone_number

    # Randomly compute the remaining serial number digits
    while len(imei) < 14:
        imei += str(random.randint(0, 9))

    # Calculate the check digit with the Luhn algorithm
    imei += imei_calc_check_digit(imei)
    return imei