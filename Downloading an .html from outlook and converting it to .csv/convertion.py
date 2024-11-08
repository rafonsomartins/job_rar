import pandas as pd
from bs4 import BeautifulSoup
import re

def parse_htm_to_csv(htm_file, csv_file):
    with open(htm_file, 'r', encoding='ISO-8859-1') as file:
        soup = BeautifulSoup(file, 'html.parser')

    data = []
    ignore_words = ['Relatório', 'Utilizador', 'Mandante', '\xa0Total', 'Tipo', '\xa0-', 'OT', 'ZKB', 'ZOF', 'Ordem', 'Colocação']

    # Busca todas as tags <nobr>
    for nobr in soup.find_all('nobr'):
        line_text = nobr.get_text()
        # print(f"line:{line_text}")
        # Verifica se a linha começa com uma das palavras que devemos ignorar
        if any(line_text.startswith(word) for word in ignore_words):
            # print(f"i am in ignore words, line: {line_text}")
            continue
        elif not line_text or line_text.startswith('\xa0'):
            continue
        line_text = line_text.strip().replace('\xa0', ' ')
        # Regex para capturar o número inicial (Cod Doc.), a primeira data, o número de 5 dígitos (Material), e a quantidade
        match = re.match(r'^(\d+)\s.*?(\d{2}\.\d{2}\.\d{4})\s(\d{2}\.\d{2}\.\d{4})\s(?:A\s)?\d{6}\s(\d{5}).*?(\d[\d\.]*,\d+)', line_text)
        if match:
            cod_doc = match.group(1)
            data_doc = match.group(2).replace('.', '/')
            data_Rem = match.group(3).replace('.', '/')
            material = match.group(4)
            quantidade = match.group(5).replace('.', '').replace(',', '.')

            data.append({
                'Cod Doc.': cod_doc,
                'Data': data_doc,
                'Data Rem.': data_Rem,
                'Material': material,
                'Qtd': quantidade
            })

    # Cria um DataFrame com os dados capturados
    df = pd.DataFrame(data, columns=['Cod Doc.', 'Data', 'Data Rem.', 'Material', 'Qtd'])
    df['Qtd'] = df['Qtd'].astype(float)

    # Salva o DataFrame como CSV
    df.to_csv(csv_file, index=False, encoding='utf-8-sig', sep=';', decimal=',')

# Usar a função
parse_htm_to_csv('output_file.htm', 'Conv.csv')
