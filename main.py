import csv
import datetime
import random
# import requests

from faker import Faker
# from gerador_endereco import *

# def getAddress(cep):
#     r = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
#     r.status_code
#     return r.json()

def generate_fake_data():
    fake = Faker(['pt_BR'])
    Faker.seed(0)

    # address = getAddress()

    header = [
        'nome',
        'email',
        'cpf',
        'telefone',
        'rua',
        'bairro',
        'cidade',
        'estado',
        'endereco',
        'cep',
        'data_de_nascimento',
        'produto',
        'restringido',  # está com dados na lista restritiva
        'bloqueado',  # está bloqueado
        # 'user_agent'
    ]

    produtos = [
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

    # open the file in the write mode
    with open('hack_day_dataset.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for _ in range(100):
            data = [
                fake.name(),
                fake.email(),
                fake.ssn(),
                fake.cellphone_number(),
                fake.street_name(),
                fake.bairro(),
                fake.city(),
                fake.estado_nome(),
                fake.address(),
                fake.postcode(),
                fake.date_between_dates(datetime.date(1960, 1, 1), datetime.date(2012, 1, 1)),
                random.choice(produtos),
                fake.boolean(chance_of_getting_true=5),
                fake.boolean(chance_of_getting_true=5),
                # fake.user_agent()
            ]

            writer.writerow(data)


if __name__ == '__main__':
    generate_fake_data()


