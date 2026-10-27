import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HimnosProyecto.settings")
import django
django.setup()

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from apiHimnos.models import Himnos, ParrafoCoros, Parrafos

userInput: int

def main() -> None:
    options: FirefoxOptions = FirefoxOptions()
    options.add_argument('--headless')
    driver: Firefox = Firefox(options=options)
    driver.get('https://sendangosta.wordpress.com/himnos-pentecostales/')
    elementosTabla: WebElement = driver.find_element(by=By.TAG_NAME, value='table')
    elementos: list[WebElement] = elementosTabla.find_elements(by=By.TAG_NAME, value='a')

    links: list[str] = []

    for item in elementos:
        link = item.get_attribute(name='href')
        if link:
            links.append(link)

    for link in links:
        driver.get(link)
        titulo: str | None = driver.find_element(by=By.CLASS_NAME, value='entry-title').text

        if titulo is None:
            continue

        entryContent: WebElement = driver.find_element(by=By.CLASS_NAME, value='entry-content')
        parrafos: list[WebElement] = entryContent.find_elements(by=By.TAG_NAME, value='p')

        titulo = titulo.replace('–', '-').replace('  ', ' ')
        numero, titulo = titulo.split('-')

        numero = numero[6: len(numero)].strip()
        titulo = titulo.strip()

        print("|", numero, "|", titulo, "|")

        if int(numero) < userInput:
            continue

        himno: Himnos = Himnos(numero=numero, titulo=titulo)
        himno.save()

        for index, item in enumerate(parrafos):
            try:
                _ = item.find_element(by=By.TAG_NAME, value='a')
                _ = item.find_element(by=By.TAG_NAME, value='strong')
            except NoSuchElementException:
                parrafoSingular: str | None = item.text

                if parrafoSingular:
                    if parrafoSingular[0:4].lower() == "coro":
                        parrafoSingular = parrafoSingular[5: len(parrafoSingular)]
                        coro = ParrafoCoros(parrafo=parrafoSingular, numero_parrafo=index + 1, himno_id_fk=himno)
                        coro.save()

                    else:
                        parrafo = Parrafos(parrafo=parrafoSingular, numero_parrafo=index + 1, himno_id_fk=himno)
                        parrafo.save()

        print("Himno", titulo, "Guardado")


if __name__ == '__main__':
    userInput = int(input("DESDE QUE NUMERO: "))
    main()
