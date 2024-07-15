import requests

def get_web(file_name):
    url = 'https://fred.stlouisfed.org/graph/fredgraph.csv'
    params = {
        'bgcolor': '%23e1e9f0',
        'chart_type': 'line',
        'drp': '0',
        'fo': 'open%20sans',
        'graph_bgcolor': '%23ffffff',
        'height': '450',
        'mode': 'fred',
        'recession_bars': 'off',
        'txtcolor': '%23444444',
        'ts': '12',
        'tts': '12',
        'width': '718',
        'nt': '0',
        'thu': '0',
        'trc': '0',
        'show_legend': 'yes',
        'show_axis_titles': 'yes',
        'show_tooltip': 'yes',
        'id': file_name,  # ID of the series, e.g., 'PMAIZMTUSDM'
        'scale': 'left',
        'cosd': '1990-01-01',
        'coed': '2024-04-01',
        'line_color': '%234572a7',
        'link_values': 'false',
        'line_style': 'solid',
        'mark_type': 'none',
        'mw': '3',
        'lw': '2',
        'ost': '-99999',
        'oet': '99999',
        'mma': '0',
        'fml': 'a',
        'fq': 'Monthly',
        'fam': 'avg',
        'fgst': 'lin',
        'fgsnd': '2020-02-01',
        'line_index': '1',
        'transformation': 'lin',
        'vintage_date': '2024-05-20',
        'revision_date': '2024-05-20',
        'nd': '1990-01-01'
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
        'Referer': 'https://fred.stlouisfed.org/series/' + file_name,
        'Sec-Ch-Ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.text
    else:
        return None
