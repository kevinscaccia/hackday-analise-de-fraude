import csv
import datetime
import random
import numpy as np
from faker import Faker
from util import *

QUANTIDADE_REGISTROS = 100
PROB_FRAUDULENTO = 0.2
SEED = 77

PRODUTOS = [
        'Globoplay + canais ao vivo e Telecine',
        'Starzplay',
        'Deezer Premium',
        'Cartola PRO',
        'Globoplay',
        'Globoplay + canais ao vivo e Premiere',
        'Disney +',
        'Premiere',
        'Globoplay e discovery +',
        'discovery +',
        'Globo Mais',
        'Globoplay e Disney +',
        'Combate',
        'Globoplay e Premiere',
        'Giga Gloob',
        'Globoplay + canais ao vivo',
        'Globoplay e Telecine',
        'Globoplay e Starzplay',
        'Globoplay + canais ao vivo e Disney +'
    ]
HEADER = [
    'id',
    'fraude',
    'nome',
    'email',
    'cpf',
    'telefone',
    'rua',
    'bairro',
    'cidade',
    'estado',
    'cep',
    'data_de_nascimento',
    'produto',
    'restringido',  # está com dados na lista restritiva
    'bloqueado',  # está bloqueado
    'user_agent',
    'imei'
    ]

def generate_fake_data():
    np.random.seed(SEED)
    Faker.seed(0)
    fake = Faker(['pt_BR'])
    f = open('hack_day_dataset.csv', 'w', encoding='UTF8')
    writer = csv.writer(f)
    writer.writerow(HEADER)
    
    ceps = get_ceps()
    addresses = get_addresses()

    
    for usuario_i in range(QUANTIDADE_REGISTROS):
        # diz se esse usuário é fraudulento ou não
        is_fraude = gera_prob(PROB_FRAUDULENTO)
        print(f"Gerando usuario id{usuario_i}(FRAUDE={is_fraude})")
        # gera nome
        nome, sobrenome, email = gera_nome_e_email(fake, is_fraude)
        print(nome, sobrenome, email)
        phone = fake.msisdn()
        cep = random.choice(ceps)
        data = [
            usuario_i,
            is_fraude,
            nome,
            sobrenome,
            email,
            fake.ssn(),
            phone,
            addresses[cep]['street'],
            addresses[cep]['neighborhood'],
            addresses[cep]['city'],
            addresses[cep]['state'],
            cep,
            fake.date_between_dates(datetime.date(1960, 1, 1), datetime.date(2012, 1, 1)),
            random.choice(PRODUTOS),
            fake.boolean(chance_of_getting_true=5),
            fake.boolean(chance_of_getting_true=5),
            fake.user_agent(),
            get_imei(phone)
        ]
        writer.writerow(data)
      
    f.close()


if __name__ == '__main__':
    generate_fake_data()
    print("Dados gerados!")