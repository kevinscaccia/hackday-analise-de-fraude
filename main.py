import csv
import datetime
import random
import numpy as np
from faker import Faker
from util import *

QUANTIDADE_REGISTROS = 100
PROB_FRAUDULENTO = 0.2
SEED = 77


def generate_fake_data():
    np.random.seed(SEED)
    Faker.seed(0)
    fake = Faker(['pt_BR'])
    f = open('hack_day_dataset.csv', 'w', encoding='UTF8')
    writer = csv.writer(f)
    #writer.writerow(header)


    for usuario_i in range(QUANTIDADE_REGISTROS):
        # diz se esse usuário é fraudulento ou não
        is_fraude = gera_prob(PROB_FRAUDULENTO)

        # gera nome
        nome, sobrenome, email = gera_nome_e_email(fake, is_fraude)
        print(nome, sobrenome, email)
        data = [
            nome,
            sobrenome,
            email,
            # fake.ssn(),
            # fake.cellphone_number(),
            # fake.street_name(),
            # fake.bairro(),
            # fake.city(),
            # fake.estado_nome(),
            # fake.address(),
            # fake.postcode(),
            # fake.date_between_dates(datetime.date(1960, 1, 1), datetime.date(2012, 1, 1)),
            # random.choice(produtos),
            # fake.boolean(chance_of_getting_true=5),
            # fake.boolean(chance_of_getting_true=5),
            # fake.user_agent()
            ]
        writer.writerow(data)
      
    f.close()


if __name__ == '__main__':
    generate_fake_data()


