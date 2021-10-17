from bs4 import BeautifulSoup
import requests
from requests import get
import time
import random

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

#адрес списка квартир
url = 'https://www.avito.ru/ekaterinburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?p='
#хранилище комнат
houses = []
#переменная - индекс страницы
count = 1
while count <= 100:
    # сюда записываем юрл страницы и её индекс (разные странинцы)
    url = 'https://www.avito.ru/ekaterinburg/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?p='+str(count)
    # напишем юрл для проверки
    print(url)
    # гет запрос страницы по нашему юрл, в котором учтен индекс страницы
    response = get(url, headers=HEADERS)
    print(response.text)
    # загоняем текст в HTML парсер
    html_soup = BeautifulSoup(response.text, 'html.parser')
    # ищем div блок класса iva-item-content-UnQQ4 чтобы вытащит нужную информацию и заносим в список house_data
    house_data = html_soup.find_all('div', class_="iva-item-content-UnQQ4")
    # если такие блоки есть (списком) , то выполняются команды ниже
    if house_data !=[]:
        # добавляем к массиву houses массив house_data (тем самым дополняя первый массив)
        houses.extend(house_data)
        # создаем случайное число
        value = random.random()
        # усложняем случайное число
        scaled_value = 1 + (value * (9 - 5))
        # выводим случайное число
        print(scaled_value)
        # симулируем рандомную пользовательскую задержку, используя случайное число
        time.sleep(scaled_value)
    # если блоков в house_data нет, то пишем empty и полностью сбрасываем операцию, завершая программу,
    else:
        print('empty')
        break
    # прибавляем страницу после цикла if, чтобы запустить следующую страницу
    count += 1
# выводим количество квартир
print(len(houses))

print(houses[1])
print()
n = int(len(houses)) - 1
# обнуляем переменную count, так как блок поиска всего HTML со всех страниц уже отработал с ней
count = 0
# выводим 5 первых квартир
while count <= 5:
    # переменная инфо берет ячейку массива под индексом count из массива houses [[1(f,r,t)][2][3]]
    # в ячейке массива есть взя информация по каждой квартире
    info = houses[int(count)]
    # достем переменную price-цена методом поиска контейнера с тегом "span" класса "price-price-BQkOZ"
    # ищем именно текстовые символы
    price = info.find('span', {"class": "price-price-BQkOZ"}).text
    # достем переменную title-название(заголовок) методом поиска контейнера с тегом "h3" класса "title-root-j7cja"
    # ищем именно текстовые символы
    title = info.find('h3', {"class": "title-root-j7cja"}).text
    # печатаем название, пробел, цену
    print(title, '', price)
    # прибавляем переменную count
    count += 1

