from selenium import webdriver
from pathlib import Path
from time import sleep
import sys


class ComponenteDriver:
    @staticmethod
    def get_driver(directorio):
        nombre_driver = directorio.get_nombre_chromedriver()

        options = webdriver.ChromeOptions()

        prefs = {"download.prompt_for_download": False,
                 "plugins.always_open_pdf_externally": True,
                 "profile.default_content_setting_values.automatic_downloads": 1,
                 'download.default_directory': str(directorio.get_descarga_dir().parent),
                 "credentials_enable_service": False,
                 "profile.password_manager_enabled": False}

        options.add_experimental_option("prefs", prefs)

        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)

        try:
            driver = webdriver.Chrome(options=options, executable_path=str(Path.cwd() / nombre_driver))
        except:
            print("\nEl driver de chrome no es compatible con su navegador. \nSe recomienda descargar su version "
                  "mas reciente en el siguiente link {}".format(directorio.get_link_chromedriver()))
            sleep(120)
            sys.exit(0)

        return driver
