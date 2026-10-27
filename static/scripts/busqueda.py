from typing import Any

from rapidfuzz import fuzz
from unidecode import unidecode


class BusquedaFuzz:
    MAXIMO_RATIO: int = 70
    MAXIMO_RATIO_BIBLIA: int = 70

    def buscarNumero(self, lista_himnos: list[Any], palabra: str) -> list[Any]:
        resultados: list[Any] = []

        for item in lista_himnos:
            palabraFormateada: str = palabra.strip()
            palabraLength: int = len(palabraFormateada)
            numero: str = str(item['numero']).strip()[0: palabraLength]

            if numero == palabraFormateada:
                resultados.append(item)

        return resultados


    def buscarTitulo(self, lista_himnos: list[Any], palabra: str) -> list[Any]:
        resultados: list[Any] = []

        for item in lista_himnos:
            palabraFormateada: str = unidecode(palabra.lower().strip())
            titulo: str = unidecode(item['titulo'].lower().strip())

            partial_ratio: float = fuzz.partial_ratio(titulo, palabraFormateada)

            if partial_ratio >= self.MAXIMO_RATIO:
                resultados.append(item)

        return resultados


    def buscarLetra(self, lista_parrafos: list[str], palabra: str) -> bool:
        for item in lista_parrafos:

            palabraFormateada: str = unidecode(palabra.lower().strip())
            letra: str = unidecode(item[1])

            partial_ratio: float = fuzz.partial_ratio(letra, palabraFormateada)

            if partial_ratio >= self.MAXIMO_RATIO:
                return True

        return False


    def buscarLibros(self, diccionario_libros: dict[int, str], palabra: str) -> list[dict[str, Any]]:
        resultados: list[Any] = []

        for index, item in diccionario_libros.items():
            capituloFormateado: str = unidecode(item.lower().strip())
            palabraFormateada: str = unidecode(palabra.lower().strip())

            partial_ratio: float = fuzz.partial_ratio(capituloFormateado, palabraFormateada)

            if partial_ratio >= self.MAXIMO_RATIO_BIBLIA:
                resultados.append({'index': index, 'nombreLibro': item})


        return resultados
