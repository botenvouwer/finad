import re
from typing import Union

import pandas as pd

from os import listdir
from os.path import isfile, join
from pathlib import *

from fin.AccountPerYear import AccountsPerYear, AccountPerYear


def load_knab(data_path: Union[Path, str]):
    fin_data = AccountsPerYear()
    data_path = Path(data_path)

    fin_headers = ['date', 'year', 'month', 'credit_or_debet', 'amount', 'credit', 'debet', 'i_number', 'i_name', 'e_number', 'e_name', 'internal_or_external', 'e_type', 'e_official_name', 'description', 'payment_type']
    labels = {
        'NL25KNAB0604860706': 'pri_inkomen',
        'NL60KNAB0604871716': 'pri_boodschappen',
        'NL54KNAB0604873182': 'pri_fun',
        'NL55KNAB0604872291': 'pri_overig',
        'NL08KNAB0604887493': 'pri_abbo',
        '57347285': 'pri_stack',
        '57441905': 'pri_stack_kaakoperatie',
        'NL02KNAB0407458360': 'huis_inkomen_en_lasten',
        'NL45KNAB0407464085': 'huis_klussen',
        'NL13KNAB0407465243': 'huis_huishoudelijk',
        '57857884': 'huis_spaar',
        'NL55INGB0798628839': 'huis_hypotheek',
        'NL06RABO0154599808': 'pri_oud',
        '57673844': 'pri_stack_oud',
        '60010259': 'pri_stack_oud2',
        '58841463': 'pri_stack_cadeautjes',
    }

    csv_paths = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    for i, cvs_path in enumerate(csv_paths):

        path = data_path / cvs_path
        account_number, account_type, year = parse_csv_knab(cvs_path)

        label = labels[account_number]

        s = label.split('_')
        account_name, account_category = (s.pop(0), '_'.join(s))

        df = pd.read_csv(path, skiprows=1, sep=';', decimal=',')
        df['Bedrag'] = df['Bedrag'].astype(float)

        df['Transactiedatum'] = pd.to_datetime(df['Transactiedatum'], dayfirst=True)
        df['Year'] = df['Transactiedatum'].dt.year
        df['Month'] = df['Transactiedatum'].dt.month

        def transform(c):
            c['Credit'] = c['Bedrag'] if c['CreditDebet'] == 'C' else 0
            c['Debet'] = c['Bedrag'] if c['CreditDebet'] == 'D' else 0
            c['RekeningnummerNaam'] = labels[c['Rekeningnummer']] if c['Rekeningnummer'] in labels else '?'
            c['TegenrekeningnummerNaam'] = labels[c['Tegenrekeningnummer']] if c['Tegenrekeningnummer'] in labels else c['Tegenrekeninghouder']
            c['InternalExternal'] = 'I' if c['Tegenrekeningnummer'] in labels else 'E'
            c['e_type'] = ('P' if c['Tegenrekeningnummer'].startswith('NL') else 'S') if c['InternalExternal'] == 'I' else None

            return c

        df = df.apply(transform, axis=1)
        df = df[['Transactiedatum', 'Year', 'Month', 'CreditDebet', 'Bedrag', 'Credit', 'Debet', 'Rekeningnummer', 'RekeningnummerNaam', 'Tegenrekeningnummer', 'TegenrekeningnummerNaam', 'InternalExternal', 'e_type', 'Tegenrekeninghouder', 'Omschrijving', 'Betaalwijze']]
        df = df.set_axis(fin_headers, axis=1)

        account_info = AccountPerYear(path, df, account_name, account_category, account_number, account_type, year)

        fin_data.add_account(account_info)

    return fin_data


def parse_csv_knab(file_name):
    file_name = re.sub('\+', ' ', file_name)
    file_name = re.sub(' +', ' ', file_name)
    s = file_name.split(' ')
    # (account_number, account_type, year)
    return (s[3], s[2], s[5][0:4])
