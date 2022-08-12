import gzip
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import seaborn as sns
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import datetime
from PIL import Image
import requests

sns.set(style='darkgrid')

st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    # Carregando o modelo caso utilizar o gzip para compactar o arquivo.
    @st.cache(allow_output_mutation=True)
    def load_modelo():
        zip = gzip.GzipFile('rf_model.pkl', 'rb')
        rf_model = pickle.load(zip)
        return rf_model

    @st.cache(allow_output_mutation=True)
    def load_ceps():
        with open('ceps.txt') as f:
            lines = f.readlines()
        return lines

    rf_model = load_modelo()
    lines = load_ceps()

    st.header('Formulário de Cadastro')
    st.subheader('Digite seus dados para comprar um produto GLOBO')

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    def remote_css(url):
        st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

    def icon(icon_name):
        st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

    # local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    # Aqui começamos a colocar os campos de cadastro!

    produtos = ('Globoplay + canais ao vivo e Telecine',
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
        'Globoplay + canais ao vivo e Disney +')

    produto = st.selectbox(
        'Qual produto deseja?', index=0, key='produto', options=list(range(len(produtos))),
        format_func=lambda x: produtos[x]
    )

    print(produto)
    col, col_ = st.columns(2)
    NomeCompleto = col.text_input("", "Digite Seu nome completo")
    email = col_.text_input("", "Digite Seu nome email")
    col1, col2 = st.columns(2)
    telefone = col1.text_input("", "Digite Seu nome Telefone")
    cpf = col2.text_input("", "Digite Seu nome CPF")

    data1, age1 = st.columns([5, 1])
    d = data1.date_input(
        "Qual sua data de nascimento?",
        datetime.date(1993, 1, 19))
    dias = datetime.datetime.now() - datetime.datetime.fromordinal(d.toordinal())
    duration_in_s = dias.total_seconds()
    age = int(divmod(duration_in_s, 31536000)[0])
    dob = datetime.datetime.fromordinal(d.toordinal()).strftime("%d/%m/%Y")
    idade = age1.success(age)
    icon("search CEP")

    search, ok, tam = st.columns([5, 1, 2])
    # menu_tipo_procura = ok.button("ok")
    selected = search.text_input("", "Digite seu CEP")

    if selected == "Digite seu CEP":
        st.write('Esperando...')
        icon("search")
    else:
        lines = [s for s in lines if selected.lower() in s.lower()]

        ceps = [int(i.split('\t')[0]) for i in lines]
        cep = tam.selectbox(
            'selecione CEP', index=0, key='cep', options=list(range(len(lines))),
            format_func=lambda x: ceps[x]
        )

        num_cep = ceps[cep]
        listagem_endereco = lines[cep].split('\t')
        listagem_cidade_estado = str(listagem_endereco[1]).strip()
        cidade = listagem_cidade_estado.split('/')[0]
        estado = listagem_cidade_estado.split('/')[1]
        bairoRua = ' '.join(listagem_endereco[2:])

        cidade = st.success(cidade)
        bairro_rua = st.success(bairoRua)



        st.markdown('')
        st.markdown('')

        if st.button('CADASTRAR'):
            st.write('GloboID Score: ', {'nome': NomeCompleto,
                                         'data_de_nascimento': dob,
                                         'email': email,
                                         'telefone': telefone,
                                         'cpf': cpf,
                                         'cep': num_cep,
                                         'estado': estado,
                                         'cidade': lines[cep].split('\t')[1].split('/')[0],
                                         'bairro': bairoRua,
                                         'rua': bairoRua,
                                         'produto': produtos[produto],
                                         'restringido': True,
                                         'bloqueado': True,
                                         'user_agent': 'Mozilla/5.0 (Windows; U; Windows CE) AppleWebKit/533.35.4 (KHTML, like Gecko) Version/4.0 Safari/533.35.4',
                                         'imei': 1516546465})

            import requests
            import json

            url = "http://localhost:5000/score"

            payload = json.dumps({'nome': NomeCompleto,
                                         'data_de_nascimento': dob,
                                         'email': email,
                                         'telefone': telefone,
                                         'cpf': cpf,
                                         'cep': num_cep,
                                         'estado': estado,
                                         'cidade': lines[cep].split('\t')[1].split('/')[0],
                                         'bairro': bairoRua,
                                         'rua': bairoRua,
                                         'produto': produtos[produto],
                                         'restringido': True,
                                         'bloqueado': True,
                                         # 'user_agent': 'Mozilla/5.0 (Windows; U; Windows CE) AppleWebKit/533.35.4 (KHTML, like Gecko) Version/4.0 Safari/533.35.4',
                                         'imei': 1516546465})
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)
            # request.headers.get('User-Agent')

if __name__ == '__main__':
    main()