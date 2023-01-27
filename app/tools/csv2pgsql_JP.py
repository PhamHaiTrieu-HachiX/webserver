import json
import psycopg2
import pykakasi
import sqlalchemy

import unicodedata
from datetime import datetime

kks = pykakasi.kakasi()

with open("info.json", "r", encoding="utf8") as ff:
    info = ff.read()

info_json = json.loads(info)

host = info_json["hostname"]
port = info_json["port"]
database = info_json["database"]
user = info_json["user"]
pw = info_json["password"]

conn = psycopg2.connect(
    host=host,
    port=port,
    dbname=database,
    user=user,
    password=pw
)
cursor = conn.cursor()
create_table = '''CREATE TABLE IF NOT EXISTS public.bank (\n
                        index SERIAL CONSTRAINT "Bank_pkey" PRIMARY KEY,\n
                        id varchar(25) NOT NULL,\n
                        kata_name text COLLATE pg_catalog."default",\n
                        kanji_name text COLLATE pg_catalog."default",\n
                        hira_name text COLLATE pg_catalog."default",\n
                        romanji_name text COLLATE pg_catalog."default"\n
                    )\n
                    TABLESPACE pg_default;'''
cursor.execute(create_table)

create_table_2 = '''CREATE TABLE IF NOT EXISTS public.branch (\n
                        index SERIAL CONSTRAINT branch_pkey PRIMARY KEY,\n
                        id varchar(25) NOT NULL,\n
                        bank_id varchar(25) NOT NULL,\n
                        kata_name text COLLATE pg_catalog."default",\n
                        kanji_name text COLLATE pg_catalog."default",\n
                        hira_name text COLLATE pg_catalog."default",\n
                        romanji_name text COLLATE pg_catalog."default"\n
                    )\n
                    TABLESPACE pg_default;'''
cursor.execute(create_table_2)
conn.commit()
# print(cursor.fetchall())

with open("./files/ginkositen.txt", 'r', encoding='cp932') as f:
    lines = f.readlines()

bank = 0
branch = 0
for i, line in enumerate(lines):
    new_line = (unicodedata.normalize('NFKC', line))
    data = new_line.split(",")
    bank_id = data[0]
    branch_id = data[1]
    kata_name = data[2].replace(' ', '').strip('"')
    kanji_name = data[3].replace(' ', '').strip('"')
    name_in_jap = kks.convert(kata_name)
    hira_name = name_in_jap[0]['hira']
    romanji_name = name_in_jap[0]['hepburn']
    flag = data[4]
    # data_str = f'{bank_id}, {branch_id}, {kanji_name}, {kata_name}, {flag}'

    if int(flag) == 1:
        bank += 1
        log = f"{datetime.now()}: Insert into bank.\n"
        with open("./logs/insert_bank.log", 'a', encoding='utf8') as ff:
            ff.writelines(log)
        insert_bank = f'INSERT INTO public.bank (id, kata_name, kanji_name, hira_name, romanji_name) VALUES (%s, %s, %s, %s, %s)'
        insert_bank_value = (bank_id, kata_name, kanji_name, hira_name, romanji_name)
        try:
            cursor.execute(insert_bank, insert_bank_value)
            conn.commit()
        except Exception as e:
            conn.commit()
            log = f"{datetime.now()}: {e}\n"
            with open("./logs/insert_bank.log", 'a', encoding='utf8') as ff:
                ff.writelines(log)
    else:
        branch += 1
        log = f"{datetime.now()}: Insert into branch.\n"
        with open("./logs/insert_branch.log", 'a', encoding='utf8') as ff:
            ff.writelines(log)
        insert_branch = f'INSERT INTO public.branch (id, bank_id, kata_name, kanji_name, hira_name, romanji_name) VALUES (%s, %s, %s, %s, %s, %s)'
        insert_branch_value = (branch_id, bank_id, kata_name, kanji_name, hira_name, romanji_name)
        try:
            cursor.execute(insert_branch, insert_branch_value)
            conn.commit()
        except Exception as e:
            conn.commit()
            log = f"{datetime.now()}: {e}\n"
            with open("./logs/insert_branch.log", 'a', encoding='utf8') as ff:
                ff.writelines(log)

conn.commit()

conn.close()

print(f"Bank: {bank}")
print(f"Branch: {branch}")

