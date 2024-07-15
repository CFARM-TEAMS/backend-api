# scraper.py
from datetime import datetime
import calendar
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_date_time(soup, month, year):
    tables = soup.find_all('table')
    if len(tables) < 2:
        return None
    table_date = tables[1]
    address = table_date.find_all('address')
    date_time = [' '.join(data.stripped_strings) for data in address]
    date_time = [f"{year}-{month:02d}-{date}" for date in date_time]
    return date_time

def get_title(soup):
    table_title = soup.find_all('td', class_='table-dark')[1:]
    titles = [title.text.strip() for title in table_title]
    titles.insert(0, 'Date and Time')
    return titles

def data_array_mix(soup):
    rows = soup.find_all('tr')
    data_weather = []
    for arrays in rows[3:9]:
        columns = arrays.find_all('td')
        data_columns = [column.text.strip() for column in columns[1:]]
        data_weather.append(data_columns)
    return data_weather

def insert_data_df(df, data_weather, date_time, titles):
    if df.empty:
        df = pd.DataFrame(columns=titles)
    for i in range(len(date_time)):
        row_data = [date_time[i]] + [data_weather[j][i] for j in range(len(data_weather))]
        df.loc[len(df)] = row_data
    return df

def get_web(year, month, day, retries=3):
    url = 'https://www.weatherapi.com/history/q/bandung-3071671?loc=3071671'
    payload = {
        "__VIEWSTATE": "GcYhxkv0aeCnfiMv5Do6uV/xnCoaRujwMEwdT10lJ5JNQlAa0giVq2iA3YS34QnrWd8J7AyHOrPVkPX1lXTQoz58nKQ9UFohrN+TEJqzNp2W9E+lIAqkfBlMuuSzFLVwBnIZyCKqk+dovhhtre6sZkRcXSeAgHA882qeBuujBWvwccM6vggQslC3V92AgWoCqYOuq6KnlZy1CIzWXmE96xND8R0Lbm3e9lycmSY7g7jIxxqAXVtLO3q6Vm/Kk2GW08nh86v+7o/POb5skhAlPGYeH01HHFCDXhdW/ze4IvQBTtJdsuASnxKjzy8lPOFeeR4NA8rnF1rnMMFImWv0P9Py7wzPAr8izS9hGjyt1egds+Vk1eOof4Abn/HgHMhu5hBqYvHcF/zzwtfM0JWsFEGqPSlb7jNmQ+s6kQbGS9JsfPk9ZiFfiMS6cbYupOlDlNNb+VQC50crl+m/omYOLOJBb/aL7PMKdCef+eh35diArvj9hFATbz18vlZa2E2uxSZL/0lDm4j2vDbjhuwIWLWrNPi9VtbD8M5xuvIvqMlEFedO",
        "__VIEWSTATEGENERATOR": "B345DBAE",
        "ctl00$Search1$txtSearch": "",
        "ctl00$MainContentHolder$txtpastdate": f"{year}-{month:02d}-{day:02d}",
        "ctl00$MainContentHolder$butHistory": "Submit",
        "ctl00$MainContentHolder$hdlat": "-7.44",
        "ctl00$MainContentHolder$hdlon": "111.46"
    }

    for attempt in range(retries):
        try:
            web = requests.post(url, data=payload, timeout=20)
            soup = BeautifulSoup(web.text, 'html.parser')
            if "Bandung Historical Weather" in soup.title.text:
                titles = get_title(soup)
                date_time = get_date_time(soup, month, year)
                data_weather = data_array_mix(soup)
                return titles, date_time, data_weather
        except requests.exceptions.ReadTimeout:
            print(f"Timeout occurred for {year}-{month:02d}-{day:02d}, attempt {attempt + 1}")
            time.sleep(2)  # Wait for a while before retrying
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return None, None, None


def loop_month_day(start_month, start_year, end_month, end_year):
    df = pd.DataFrame()
    responses = []
    try_again = 1

    for year in range(start_year, end_year + 1):
        start_m = start_month if year == start_year else 1
        end_m = end_month if year == end_year else 12
        for month in range(start_m, end_m + 1):
            _, total_day = calendar.monthrange(year, month)
            for day in range(1, total_day + 1):
                titles, date_time, data_weather = get_web(year, month, day)
                if all([titles, date_time, data_weather]):
                    print(f"Success scrape {year}-{month:02d}-{day:02d}")
                    df = insert_data_df(df, data_weather, date_time, titles)
                    responses.append((year, month, day, "Success"))
                else:
                    print(f"Data not available for {year}-{month:02d}-{day:02d}   {try_again}x")
                    try_again += 1
                    if try_again == 2:  # Check if this is the first attempt
                        titles, date_time, data_weather = get_web(year, month, day)
                        if all([titles, date_time, data_weather]):
                            print(f"Success scrape {year}-{month:02d}-{day:02d}")
                            df = insert_data_df(df, data_weather, date_time, titles)
                            responses.append((year, month, day, "Success"))
                        else:
                            print(f"Data not available for {year}-{month:02d}-{day:02d}   {try_again}x.")
                            try_again = 1  # Reset try_again after the second attempt
                            responses.append((year, month, day, "Data not available"))
                    else:
                        print(f"Data not available for {year}-{month:02d}-{day:02d}")
                        try_again = 1  # Reset try_again if not the first attempt
                        responses.append((year, month, day, "Data not available"))
                time.sleep(1)
    return df, responses


def write_log_to_file(log_entries, filename="log.txt"):
    with open(filename, "w") as file:
        for entry in log_entries:
            file.write(entry + "\n")
