import json
import csv
from bs4 import BeautifulSoup
import requests
import codecs


def collect_data():
    # url = 'https://health-diet.ru/table_calorie/'
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    # req = requests.get(url, headers=headers)
    # src = req.text

    # with codecs.open('index.html', 'w','utf-8') as file:
    #     file.write(src)

    # with codecs.open('index.html', 'r', 'utf-8') as file:
    #     src = file.read()

    # soup = BeautifulSoup(src, 'lxml')

    # links = soup.find_all(class_ = 'mzr-tc-group-item-href')

    # all_categories_dict = {}
    # for item in links:
    #     item_href = 'https://health-diet.ru' + item['href']
    #     item_text = item.text

    #     all_categories_dict[item_text] = item_href
    #     # print(f'{item_text} : {item_href}')

    # with codecs.open('all_categories_dict.json','w','utf-8') as file:
    #     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

    with codecs.open('all_categories_dict.json', 'r', 'utf-8') as file:
        all_categories = json.load(file)

    iteration_count = int(len(all_categories)) - 1
    count = 0
    print(f'Всего итераций {iteration_count}')
    for category_name, category_href in all_categories.items():

        rep = [' ', ',', '-']
        for el in rep:
            if el in category_name:
                category_name = category_name.replace(el, '_')

        req = requests.get(url=category_href, headers=headers)
        src = req.text

        with codecs.open(f'data/{count}_{category_name}.html', 'w', 'utf-8') as file:
            file.write(src)

        with codecs.open(f'data/{count}_{category_name}.html', 'r', 'utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        # Собираем заголовки таблицы

        alert_block = soup.find(class_='uk-alert-danger') #  Проверка на наличие таблицы по запросу
        if alert_block is not None:
            continue

        table_head = soup.find_all('th')
        product = table_head[0].text
        calories = table_head[1].text
        proteins = table_head[2].text
        fats = table_head[3].text
        carbohydrates = table_head[4].text
        # print((product, calories, proteins, fats, carbohydrates))
        with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            # (product, calories, proteins, fats, carbohydrates)
            writer.writerow(
                (product,
                 calories,
                 proteins,
                 fats,
                 carbohydrates)
            )

        products_data = soup.find(
            class_='mzr-tc-group-table').find('tbody').find_all('tr')

        products_info = []

        for item in products_data:
            products_data = item.find_all('td')

            title = products_data[0].find('a').text
            calories = products_data[1].text
            proteins = products_data[2].text
            fats = products_data[3].text
            carbohydrates = products_data[4].text

            products_info.append(
                {
                    "Title": title,
                    "Calories": calories,
                    'Proteins': proteins,
                    'Fats': fats,
                    'Carbohydrates': carbohydrates
                }
            )

            with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                # (product, calories, proteins, fats, carbohydrates)
                writer.writerow(
                    (title,
                     calories,
                     proteins,
                     fats,
                     carbohydrates)
                )

        with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
            json.dump(products_info, file, indent=4, ensure_ascii=False)

        count += 1
        print(f'### Итерация {count}. {category_name} записан...')
        iteration_count = iteration_count - 1
        if iteration_count == 0:
            print('Работа завершена!')
            break
        print(f'Осталось итераций: {iteration_count}')


def main():
    collect_data()


if __name__ == '__main__':
    main()
