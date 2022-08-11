import csv
import datetime
import random

from faker import Faker


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


def generate_fake_data():
    fake = Faker(['pt_BR'])
    Faker.seed(0)
    random.seed(0)

    ceps = get_ceps()
    addresses = get_addresses()

    header = [
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
            phone = fake.msisdn()

            cep = random.choice(ceps)

            data = [
                fake.name(),
                fake.email(),
                fake.ssn(),
                phone,
                addresses[cep]['street'],
                addresses[cep]['neighborhood'],
                addresses[cep]['city'],
                addresses[cep]['state'],
                cep,
                fake.date_between_dates(datetime.date(1960, 1, 1), datetime.date(2012, 1, 1)),
                random.choice(produtos),
                fake.boolean(chance_of_getting_true=5),
                fake.boolean(chance_of_getting_true=5),
                fake.user_agent(),
                get_imei(phone)
            ]

            writer.writerow(data)


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


if __name__ == '__main__':
    generate_fake_data()


