import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm


def create_database():
    """
    Download top 5000 words from Wiktionary and save to db folder
    """
    freq_lists = ["1-1000", '1001-2000', '2001-3000', '3001-4000', '4001-5000']
    base_url = "https://en.wiktionary.org/wiki/Appendix:Russian_Frequency_lists/"

    freq_dfs = []

    print("Creating database from Wiktionary")

    for URL_end in tqdm(freq_lists):
        page = requests.get(base_url + URL_end)
        soup = BeautifulSoup(page.content, 'html.parser')
        with open(f"./db/table_{URL_end}_content.txt", "w", encoding='utf-8') as file:
            file.write(soup.prettify())

        data = []
        table = soup.find('table', attrs={'class': 'wikitable'})
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols])  # Get rid of empty values using if cols

        freq_dfs.append(pd.DataFrame(data))

    df = pd.concat(freq_dfs)

    df.columns = df.iloc[0].values
    df = df.drop(index=0, axis=0).reset_index(drop=True)

    df.to_pickle("./db/combined_table.pkl")

    print("Successfully created database from Wiktionary")


if __name__ == "__main__":
    create_database()
