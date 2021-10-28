from pathlib import Path
import pandas as pd
import datetime


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
        self.__anio = datetime.datetime.now().date().year

    def get_nombre_chromedriver(self):
        return self.__ruta_chromedriver.name

    def get_link_chromedriver(self):
        return self.__link_chromedriver

    def get_descarga_dir(self):
        return self.__cliente_dir

    def set_descarga_dir(self, nombre_cliente):
        self.__cliente_dir = self.__pdf.joinpath(nombre_cliente, str(self.__anio))

    def __set_data(self, row):
        self.__data.append(row)

    def get_data(self):
        return self.__data

    def __crear_carpeta(self, nombre_clientes):
        for nombre in nombre_clientes:
            self.set_descarga_dir(nombre)
            cliente = self.get_descarga_dir()
            cliente.mkdir(parents=True, exist_ok=True)

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
