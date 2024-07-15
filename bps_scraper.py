import pandas as pd
import requests
from datetime import datetime

now = datetime.now()
current_year = now.year
set_year = 2010  # limit from 2010

def get_web(year):
    year = year - 2000 + 100
    url = 'https://www.bps.go.id/api/statistics-table/get-data'
    params = {
        'lang': 'en',
        'id': 'Mjk1IzI=',
        'year': f'{year}'
    }
    headers = {
        'Content-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Keep-Alive': 'timeout=5',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.bps.go.id',
        'Referer': 'https://www.bps.go.id/en/statistics-table/2/Mjk1IzI=/the-average-rice-price-in-level-wholesale-indonesia.html',
        'Sec-Ch-Ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def scrape_bps_prices(start_year, end_year):
    titles = ['Year', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df = pd.DataFrame(columns=titles)

    for year in range(start_year, end_year + 1):
        result = get_web(year)
        data_price = [year]  # Mulai dengan tahun sebagai kolom pertama

        for index, (key, value) in enumerate(result['datacontent'].items()):
            if index >= 12:  # Maksimal 12 bulan
                break
            data_price.append(value)

        # Tambahkan data_price hanya jika panjangnya sesuai atau jika itu tahun terakhir dan panjangnya kurang
        if len(data_price) == len(titles):
            df.loc[len(df)] = data_price
        elif year == current_year and len(data_price) <= len(titles):
            # Isi sisa bulan dengan NaN jika data belum lengkap untuk tahun berjalan
            data_price.extend(['-'] * (len(titles) - len(data_price)))
            df.loc[len(df)] = data_price
        else:
            print(f"Data for year {year} has mismatched columns. Expected {len(titles)}, got {len(data_price)}.")

    df['Year'] = df['Year'].astype(int)
    return df
