from Gestion.Directorio import ComponenteDirectorio
from Gestion.Claro import ComponenteClaro
import msvcrt


if __name__ == '__main__':

    directorio = ComponenteDirectorio()

    if directorio.validar_existencia_archivos():
        directorio.inicializar_dato_clientes()

        claro = ComponenteClaro(directorio)
        claro.ejecutar_clientes()

    msvcrt.getch()
