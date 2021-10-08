from Gestion.Driver import ComponenteDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from PIL import Image
from re import search
from time import sleep
import base64
import requests
import json


class ComponenteClaro:
    def __init__(self, directorio):
        self.__directorio = directorio

    def ejecutar_clientes(self):
        try:
            clientes = self.__directorio.get_data()
            for cliente in clientes:
                print("***************** ", cliente, " *****************")
                self.__extraer_info_web(cliente)

        except Exception as ex:
            print(ex)

    def __extraer_info_web(self, cliente):
        # Directorio del cliente para descargar los pdfs
        self.__directorio.set_descarga_dir(cliente['CLIENTE'])

        driver = ComponenteDriver.get_driver(self.__directorio)

        try:
            driver.get('https://mi.claro.com.pe/wps/portal/miclaro/landing2/!ut/p/z1/'
                       'hY7LDoIwEEW_hQVbZpTaqDtMCI8ohOADuzFgasEAJVDh9yXqxsTH7O7ccyYDDBJgddoXIlWFrNNyzEdGT27k2O6'
                       'KYID2boFRHFISTNBEn8LhH8DGGr-MhaPPHghF13G9GDehGVG0tnvHswlBnNIX8OOGD0yUMnu-a9WZORfAWn7hLW-'
                       'NWzuuc6WabqmjjsMwGEJKUXLjLCsdPym57BQk7yQ0VYLXWdmvLU27A22zk4A!/dz/d5/L2dBISEvZ0FBIS9nQSEh/')

            # Esperar la visibilidad de la imagen del catpcha
            WebDriverWait(driver, 70).until(ec.visibility_of_element_located((By.XPATH, "//*[@id='captcha_image']")))

            # Validar el formulario
            WebDriverWait(driver, 70).until(ec.presence_of_element_located((By.XPATH, "//*[@id='formLogin']")))

            # Seleccionar la opcion RUC en el desplegable
            driver.find_element_by_xpath("//*[@id='formLogin']/div[2]/div").click()
            driver.find_element_by_xpath("//*[@id='documentoCaja']/li[3]").click()

            driver.find_element_by_id("nroDoc").send_keys(cliente['RUC'])
            driver.find_element_by_id("Password").send_keys(cliente['PASS'])

            # sleep(30)
            captcha = ComponenteClaro.__get_captcha(driver)
            driver.find_element_by_xpath("//*[@id='captchaId']").send_keys(captcha)
            driver.find_element_by_id("btnIngresar").click()
        except Exception as ex:
            print(ex)
        else:  # Dentro de la pagina de claro

            # Verificar sidebar y clic en boton de facturacion
            WebDriverWait(driver, 30).until(
                ec.presence_of_element_located((By.XPATH, "//*[@id='menu-lateral']/div")))
            WebDriverWait(driver, 30).until(
                ec.presence_of_element_located((By.XPATH, "//*[@id='menu-lateral']/div/div[2]")))

            WebDriverWait(driver, 30).until(
                ec.presence_of_element_located(
                    (By.XPATH,
                     "/html/body/div[1]/div[2]/div[1]/div/section/div[2]/htmlwrapper/div[2]/app-root/"
                     "div[1]/div[8]/div/div[2]/ul/li[4]/div/a/img")))

            driver.find_element_by_xpath("//*[@id='Pagfacturacion']/a").click()

            ComponenteClaro.__descargar_pdf(driver)
        finally:
            driver.close()

    @staticmethod
    def __descargar_pdf(driver):
        # Verificar carga de datos en la tabla
        WebDriverWait(driver, 30).until(
            ec.presence_of_element_located((By.XPATH, "//*[@id='paginaFacturacion']"
                                                      "/section/div[2]/div/div[3]/div/div/div[1]/div[2]")))
        try:
            # Verificar la existencia de items en la tabla
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "//*[@id='paginaFacturacion']"
                                                          "/section/div[2]/div/div[3]/div/div/div[1]/div[2]/div[1]")))
        except:
            print("NO EXISTE ITEMS A DESCARGAR")
        else:
            row = 1
            items = driver.find_elements_by_class_name('item')
            for item in items:  # Iterar la tabla
                if search('Vence.*\n', item.text):  # Descargar los documentos que contenga el 'Vence'
                    vencimiento = search('Vence.*\n', item.text).group()
                    sleep(1)
                    try:
                        # Clic PDF
                        driver.find_element_by_xpath("//*[@id='paginaFacturacion']/section/div[2]/div/div[3]/div/div/"
                                                     "div[1]/div[2]/div[" + str(row) + "]/div/div[5]/span").click()

                        ComponenteClaro.__verificar_pdf_no_descargado(driver)
                    except Exception as ex:
                        print(vencimiento.replace('\n', ''), ": ", ex)
                    else:
                        print(vencimiento.replace('\n', ''), ": OK!")

                row = row + 1

    @staticmethod
    def __verificar_pdf_no_descargado(driver):
        mensaje = ''
        esperando_carga_pagina = True
        while esperando_carga_pagina:
            try:
                WebDriverWait(driver, 2).until(
                    ec.presence_of_element_located((By.XPATH, '//*[@id="paginaFacturacion"]/app-loading-general/div')))
            except:
                esperando_carga_pagina = False

        # PDF NO ENCONTRADO
        try:
            modal = WebDriverWait(driver, 1).until(
                ec.presence_of_element_located((By.XPATH,
                                                '//*[@id="menu-superior"]/div[3]/app-facturacion/'
                                                'app-modal-doc-no-encontrado/div/div/div')))
            mensaje = search('.*\n', modal.text).group()
            modal.find_element_by_xpath(
                '//*[@id="menu-superior"]/div[3]/app-facturacion/'
                'app-modal-doc-no-encontrado/div/div/div/button').click()
            error_pdf = True
        except:
            error_pdf = False

        if not error_pdf:  # Si ya abrio la
            # PDF NO GENERADO
            try:
                # Ventana donde el mensaje muestra que aparecera a las 48 horas
                modal = WebDriverWait(driver, 1).until(
                    ec.presence_of_element_located((By.XPATH,
                                                    '//*[@id="menu-superior"]/div[3]/'
                                                    'app-facturacion/app-modal-error-doc/div/div/div')))
                mensaje = search('.*\n', modal.text).group()
                mensaje = mensaje + ". Tardara 48 horas en realizarlo."
                modal.find_element_by_xpath(
                    '//*[@id="menu-superior"]/div[3]/app-facturacion/app-modal-error-doc/div/div/div/button').click()
                error_pdf = True
            except:
                error_pdf = False

        if error_pdf:
            raise Exception(mensaje.strip().replace("\n", ''))

    @staticmethod
    def __get_captcha(driver):
        try:
            with open('secret.json', mode="r") as f:  # Obtener el API KEY del 2captcha
                secret = json.loads(f.read())
        except Exception as ex:
            print(ex)
        else:
            # Obtener la imagen del catpcha
            driver.save_screenshot("screenshot.png")
            img = Image.open('screenshot.png')
            img_recortada = img.crop((910, 388, 1030, 465))  # Coordenadas para cortar el screen de la pantalla
            img_recortada.save("recorte.png")

            with open("recorte.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())  # Codificar la imagen recortada

            # ENVIANDO IMAGEN A LA API PARA OBTENER EL CODIGO DEL SERVIDOR
            params_id = {"key": secret['KEY'],
                         "method": "base64",
                         "body": encoded_string,
                         "json": 1}

            response = requests.post("https://2captcha.com/in.php", data=params_id)
            response_code = response.json()

            if response_code['status'] == 1:
                # print("Esperando 15 sec. para desencriptar el captcha\n")
                sleep(15)

                # CONSULTADO PARA OBTENER EL TEXTO DE LA IMAGEN
                params_token = {"key": secret['KEY'],
                                "action": "get",
                                "id": response_code["request"],
                                "json": 1}

                response = requests.get("https://2captcha.com/res.php", params=params_token)
                response_captcha = response.json()

                if response_captcha["status"] == 1:
                    return response_captcha["request"]  # Enviar el texto del captcha

                else:
                    raise Exception(response_captcha["request"])

            else:
                raise Exception(response_code["request"])
