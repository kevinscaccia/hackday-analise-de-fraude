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
    'sobrenome',
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
    'imei',
    'ip'
]

PROB_CPF_VAZIO = 1 - 0.2
PROB_PRODUTO_VAZIO = 1 - 0.2
PROB_PHONE_VAZIO = 1 - 0.6
# SE PRODUTO N VAZIO --> TER CPF OBRIGATORIO
PROB_ENDERECO_VAZIO = 1 - 0.6
PROB_FRAUDE_MESMO_CPF = 0.2
PROB_FRAUDE_MESMO_IMEI = 0.3
PROB_TEM_CEP = 0.6


def generate_fake_data():
    np.random.seed(SEED)
    Faker.seed(0)
    fake = Faker(['pt_BR'])
    f = open('hack_day_dataset.csv', 'w', encoding='UTF8')
    writer = csv.writer(f)
    writer.writerow(HEADER)

    ceps = get_ceps()
    addresses = get_addresses()
    CPF_FRAUDULENTOS = []
    IMEI_FRAUDULENTOS = []

    usuarios = []

    for usuario_i in range(QUANTIDADE_REGISTROS):
        # diz se esse usuário é fraudulento ou não
        is_fraude = gera_prob(PROB_FRAUDULENTO)
        # print(f"Gerando usuario id{usuario_i}(FRAUDE={is_fraude})")

        produto = gera_vazio(random.choice(PRODUTOS), PROB_PRODUTO_VAZIO)

        # gera nome
        nome, sobrenome, email = gera_nome_e_email(fake, produto, is_fraude)

        phone = fake.msisdn()

        tem_cep = gera_prob(PROB_TEM_CEP)
        if tem_cep:
            cep = random.choice(ceps)
            street = addresses[cep]['street']
            neighborhood = addresses[cep]['neighborhood']
            city = addresses[cep]['city']
            state = addresses[cep]['state']
        else:
            street, neighborhood, city, state, cep = '', '', '', '', ''

        cpf = fake.ssn()
        imei = get_imei(phone)
        if is_fraude:
            CPF_FRAUDULENTOS.append(cpf)
            IMEI_FRAUDULENTOS.append(imei)
        #
        data = [
            usuario_i,
            is_fraude,
            nome,
            sobrenome,
            email,
            gera_vazio(cpf, PROB_CPF_VAZIO),
            gera_vazio(phone, PROB_PHONE_VAZIO),
            street, neighborhood, city, state, cep,
            fake.date_between_dates(datetime.date(1960, 1, 1), datetime.date(2012, 1, 1)),
            produto,
            fake.boolean(chance_of_getting_true=5),
            fake.boolean(chance_of_getting_true=5),
            fake.user_agent(),
            imei,
            fake.ipv4_public()
        ]
        usuarios.append(data)
    #
    CPF_FRAUDULENTOS = list(set(CPF_FRAUDULENTOS))
    IMEI_FRAUDULENTOS = list(set(IMEI_FRAUDULENTOS))

    # todos fraude
    for i in range(len(usuarios)):
        data = usuarios[i]
        if data[1]:
            if (gera_prob(PROB_FRAUDE_MESMO_CPF)):
                qual_cpf = np.random.randint(len(CPF_FRAUDULENTOS) - 1)
                usuarios[i][5] = CPF_FRAUDULENTOS[qual_cpf]
            #
            if (gera_prob(PROB_FRAUDE_MESMO_IMEI)):
                qual_imei = np.random.randint(len(IMEI_FRAUDULENTOS) - 1)
                usuarios[i][-1] = IMEI_FRAUDULENTOS[qual_imei]
                print(f"{i}")
    #    

    # escreve no arquivo
    for u in usuarios:
        writer.writerow(u)
    #
    f.close()


if __name__ == '__main__':
    generate_fake_data()
    print("Dados gerados!")