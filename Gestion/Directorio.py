from pathlib import Path
import pandas as pd
from datetime import datetime


class ComponenteDirectorio:
    def __init__(self):
        self.__root = Path.cwd()
        self.__ruta_chromedriver = self.__root.joinpath('chromedriver.exe')
        self.__link_chromedriver = 'https://chromedriver.chromium.org/downloads'

        self.__input_dir = self.__root.joinpath('Input')
        self.__input_file = self.__input_dir.joinpath('INPUT.txt')

        self.__pdf = self.__root.joinpath('PDFs')

        self.__cliente_dir = Path()

        self.__data = []
        self.__fecha = self.__get_fecha()

    def get_nombre_chromedriver(self):
        return self.__ruta_chromedriver.name

    def get_link_chromedriver(self):
        return self.__link_chromedriver

    def get_descarga_dir(self):
        return self.__cliente_dir

    def set_descarga_dir(self, nombre_cliente):
        self.__cliente_dir = self.__pdf.joinpath(nombre_cliente).joinpath(self.__fecha)

    def __set_data(self, row):
        self.__data.append(row)

    def get_data(self):
        return self.__data

    def __crear_carpeta(self, nombre_clientes):
        for nombre in nombre_clientes:
            self.set_descarga_dir(nombre)
            cliente = self.get_descarga_dir()
            if not cliente.exists():
                cliente.mkdir(parents=True, exist_ok=True)
            else:
                ComponenteDirectorio.__eliminar_pdfs(cliente)

    def validar_existencia_archivos(self):
        if not self.__ruta_chromedriver.is_file():
            print("\nEl archivo '{}' se debe encontrar en el directorio.".format(self.__ruta_chromedriver.name))
            return False

        if not self.__input_dir.is_dir():
            print("\nLa carpeta con el nombre de '{}' se debe encontrar en el directorio.".
                  format(self.__input_dir.name))
            return False

        if not self.__pdf.is_dir():
            print("\nLa carpeta con el nombre de '{}' se debe encontrar en el directorio.".
                  format(self.__pdf.name))
            return False

        if not self.__input_file.is_file():
            print("\nEl archivo con el nombre de '{}' se debe encontrar en la carpeta {}.".
                  format(self.__input_file.name, self.__input_file.parent.name))
            return False

        return True

    def inicializar_dato_clientes(self):
        try:
            dt = pd.read_csv(self.__input_file, sep='|', dtype=str)
            nombre_clientes = dt["CLIENTE"].tolist()
        except Exception as ex:
            print(ex)
        else:
            self.__crear_carpeta(nombre_clientes)

            for idx, rows in dt.iterrows():
                r = {'RUC': rows['RUC'], 'PASS': rows['PASS'], 'CLIENTE': rows['CLIENTE']}
                self.__set_data(r)

    @staticmethod
    def __eliminar_pdfs(ruta_descarga):
        for pdf in ruta_descarga.iterdir():
            pdf.unlink()

    @staticmethod
    def __get_fecha():
        now = datetime.now()
        mes = str(now.date().month)
        if mes == '01':
            mes = 'ENE'
        elif mes == '02':
            mes = 'FEB'
        elif mes == '03':
            mes = 'MAR'
        elif mes == '04':
            mes = 'ABR'
        elif mes == '05':
            mes = 'MAY'
        elif mes == '06':
            mes = 'JUN'
        elif mes == '07':
            mes = 'JUL'
        elif mes == '08':
            mes = 'AGO'
        elif mes == '09':
            mes = 'SET'
        elif mes == '10':
            mes = 'OCT'
        elif mes == '11':
            mes = 'NOV'
        else:
            mes = 'DIC'

        return Path(str(now.date().year)).joinpath(mes)
