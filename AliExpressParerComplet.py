from selenium import webdriver
from bs4 import BeautifulSoup as BS
import csv


title_link = "SearchProductFeed_Link__link__sf54s SearchProductFeed_Link__darkGrey__sf54s SearchProductFeed_Link" \
            "__size12__sf54s SearchProductFeed_Link__display-block__sf54s SearchProductFeed_Link__noWrap__sf54s"
rating_link = "SearchProductFeed_Link__link__sf54s SearchProductFeed_Link__grey__sf54s SearchProductFeed_Link" \
              "__size12__sf54s"
price_link = "SearchProductFeed_Price__titleWrapper__p1hme"
by_box = "SearchProductFeed_GalleryCard__card__1dnly SearchProductFeed_Preview__card__3zxie SearchProductFeed_Search" \
         "ProductFeed__galleryCard__d2dft"

all_pages = "ali-kit_Base__base__1odrub ali-kit_Base__default__1odrub ali-kit_Label__label__1n9sab ali-kit_Label" \
            "__size-s__1n9sab SearchPagination_SearchPagination__label__16999"
seller_link = "SearchProductFeed_GalleryCard__footer__1dnly"
image_link = "SearchProductFeed_Preview__img__3zxie"
link_to_cell = "SearchProductFeed_Link__link__sf54s SearchProductFeed_Link__darkGrey__sf54s SearchProductFeed_Link__size12__sf54s SearchProductFeed_Link__display-block__sf54s SearchProductFeed_Link__noWrap__sf54s"

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
     executable_path=r"C:\Users\а\PycharmProjects\selenium\chromedriver.exe",
     options=options
)


def get_items(page, query):
    URL = f"https://aliexpress.ru/wholesale?CatId=&isTmall=n&isFreeShip=n&isFavorite=n&g=y&page={page}&SearchText="
    search_with_query = query
    completeURL = URL + search_with_query
    driver.get(completeURL)
    requiredHtml = driver.page_source
    content = BS(requiredHtml, 'html.parser')
    pages = content.find('span', class_=f"{all_pages}").get_text()
    print(pages)
    items = content.find_all('div', class_=f"{by_box}")
    return items


def get_content(items):
    cards = []
    for item in items:
        cards.append(
            {
                'title': item.find('a', class_=f"{title_link}").get_text(),
                'rating': item.find('a', class_=f"{rating_link}").get_text(),
                'price': item.find('span', class_=f"{price_link}").get_text(),
                'seller': item.find('div', class_=f"{seller_link}").find('a').get('href'),
                'picture': item.find('img', class_=f"{image_link}").get('src'),
                'link': item.find('a', class_=f"{link_to_cell}").get('href')

            }
        )
    return cards


def save_doc(spisok, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название продукта',
                         'Рейтинг продукта',
                         'Цена продукта',
                         'Ссылка на продавца',
                         'Ссылка на изображение',
                         'Ссылка на товар'])
        for item in spisok:
            writer.writerow([item['title'],
                             str(" ")+item['rating'],
                             item['price'],
                             item['seller'],
                             item['picture'],
                             item['link']])


def get_activate_parsing():
    query = input("what is find?: ")
    CSV = f'{query}.csv'
    page_number = int(input("Укажите, сколько страниц парсим "))
    page = 1
    spisok = []
    while page <= page_number:
        items = get_items(page, query)
        page += 1
        spisok.extend(get_content(items))
    print(spisok)
    save_doc(spisok, CSV)
    return spisok


get_activate_parsing()
