import csv
import datetime
import random
import numpy as np
from faker import Faker
from util import *

QUANTIDADE_REGISTROS = 10000
PROB_FRAUDULENTO = 0.2
SEED = 77

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
    'ip',
    'busca_email_nome',
    'busca_email_sobrenome',
    'busca_email_ip',
    'busca_email_telefone',
    'busca_email_endereco',
    'busca_ip_telefone',
    'busca_ip_nome',
    'busca_telefone_nome'
]

PROB_CPF_VAZIO = 1 - 0.2
PROB_PRODUTO_VAZIO = 1 - 0.2
PROB_PHONE_VAZIO = 1 - 0.6
# SE PRODUTO N VAZIO --> TER CPF OBRIGATORIO
PROB_ENDERECO_VAZIO = 1 - 0.6
PROB_FRAUDE_MESMO_CPF = 0.2
PROB_FRAUDE_MESMO_IMEI = 0.3
PROB_FRAUDE_MESMO_IP = 0.3
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
    IPS_FRAUDULENDOS = []

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
        ip = fake.ipv4_public()

        defaul_range = 40
        defaul_range_top = defaul_range + 20
        range_limit = 100

        busca_email_nome = random.choice(range(defaul_range, range_limit))
        busca_email_sobrenome = random.choice(range(defaul_range, range_limit))
        busca_email_ip = random.choice(range(defaul_range, range_limit))
        busca_email_telefone = random.choice(range(defaul_range, range_limit))
        busca_email_endereco = random.choice(range(defaul_range, range_limit))
        busca_ip_telefone = random.choice(range(defaul_range, range_limit))
        busca_ip_nome = random.choice(range(defaul_range, range_limit))
        busca_telefone_nome = random.choice(range(defaul_range, range_limit))

        if is_fraude:
            CPF_FRAUDULENTOS.append(cpf)
            IMEI_FRAUDULENTOS.append(imei)
            IPS_FRAUDULENDOS.append(ip)

            busca_email_nome = random.choice(range(defaul_range_top))
            busca_email_sobrenome = random.choice(range(defaul_range_top))
            busca_email_ip = random.choice(range(defaul_range_top))
            busca_email_telefone = random.choice(range(defaul_range_top))
            busca_email_endereco = random.choice(range(defaul_range_top))
            busca_ip_telefone = random.choice(range(defaul_range_top))
            busca_ip_nome = random.choice(range(defaul_range_top))
            busca_telefone_nome = random.choice(range(defaul_range_top))

        #
        data = [
            usuario_i,
            is_fraude,
            nome,
            sobrenome,
            email,
            gera_vazio(cpf, PROB_CPF_VAZIO),
            gera_vazio(phone, PROB_PHONE_VAZIO),
            street,
            neighborhood,
            city,
            state,
            cep,
            fake.date_between_dates(datetime.date(1960, 1, 1), datetime.date(2012, 1, 1)),
            produto,
            fake.boolean(chance_of_getting_true=5),
            fake.boolean(chance_of_getting_true=5),
            fake.user_agent(),
            imei,
            ip,
            busca_email_nome,
            busca_email_sobrenome,
            busca_email_ip,
            busca_email_telefone,
            busca_email_endereco,
            busca_ip_telefone,
            busca_ip_nome,
            busca_telefone_nome
        ]
        usuarios.append(data)
    #
    CPF_FRAUDULENTOS = list(set(CPF_FRAUDULENTOS))
    IMEI_FRAUDULENTOS = list(set(IMEI_FRAUDULENTOS))
    IPS_FRAUDULENDOS = list(set(IPS_FRAUDULENDOS))

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
                usuarios[i][17] = IMEI_FRAUDULENTOS[qual_imei]
                print(IMEI_FRAUDULENTOS[qual_imei])
            #
            if (gera_prob(PROB_FRAUDE_MESMO_IP)):
                qual_ip = np.random.randint(len(IPS_FRAUDULENDOS) - 1)
                usuarios[i][18] = IPS_FRAUDULENDOS[qual_ip]
    #    

    # escreve no arquivo
    for u in usuarios:
        writer.writerow(u)
    #
    f.close()


if __name__ == '__main__':
    generate_fake_data()
    print("Dados gerados!")