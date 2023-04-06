""" WEB SCRAPER FOR COFFEE SHOPS, MAINLY FROM ALLMENUS.COM
   reference: https://www.pluralsight.com/guides/web-scraping-with-beautiful-soup """
import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd


def menu_scraper(url, file_name):
    """Function that takes in a url and file name"""
  # GETS inputted URL to parse HTML content

    content = requests.get(url, timeout=10)
    soup = BeautifulSoup(content.text, 'html.parser')
    location = soup.find('a', class_='menu-address').text.strip()
    rows = soup.find_all('span', class_=['item-title', 'item-price'])
    # Open the CSV file for writing
    with open(file_name, mode='w', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Item', 'Price', 'Location'])
    # Loop through each pair of item and price elements and write into CSV file
        for i in range(0, len(rows), 2):
            item = rows[i].text.strip()
            price = rows[i+1].text.strip()
            writer.writerow([item, price, location])

    return location


# Define a list of coffee shop URLs and corresponding file names
shop_urls = {
    'https://www.allmenus.com/il/champaign/839482-espresso-royale/menu/': 'espresso_royale_menu.csv',
    'https://www.allmenus.com/il/urbana/760257-caffe-bene/menu/': 'cafe_bene_menu.csv',
    'https://www.allmenus.com/il/champaign/254661-cafe-kopi/menu/': 'cafe_kopi_menu.csv',
    'https://www.allmenus.com/il/champaign/757433-brewlab-coffee/menu/': 'brew_lab_menu.csv'
}


def append_shop_to_csv(file_name, shop, location):
    """Function to append shop name and location next to every row in CSV file"""
   #  location = file_name.split('_')[1].split('.')[0]
    csv_input = pd.read_csv(file_name, on_bad_lines='skip')
    csv_input['Shop'] = shop
    csv_input['Location'] = location
    csv_input.to_csv(file_name, index=False)


# Loop through each shop URL and scrape the menu, then append shop and location information to CSV
for url, file_name in shop_urls.items():
    location = menu_scraper(url, file_name)
    # Getting "Cafe to Come Drink" out of the file_name "cafe_to_come_drink.csv". Previously got "Cafe".
    shop_name = file_name.split("_")[0].title()
    shop_name = ' '.join([s.capitalize() for s in file_name.split("_")[0:-1]]) 
    append_shop_to_csv(file_name, shop_name, location)

# Define a list of CSV file names to merge
csv_files = ['espresso_royale_menu.csv', 'cafe_bene_menu.csv',
             'cafe_kopi_menu.csv', 'brew_lab_menu.csv']

# Loop through each CSV file and read into a DataFrame, then concatenate into a single DataFrame
dfs = []
for file_name in csv_files:
    df = pd.read_csv(file_name)
    dfs.append(df)

merged_df = pd.concat(dfs)

# Drop 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in merged_df.columns:
    merged_df = merged_df.drop(columns=['Unnamed: 0'])

# File modifications
merged_df['Price'] = merged_df['Price'].str.replace("+", "", regex=False)

# Write the merged dataframe to a new CSV file
merged_df.to_csv('champaign_coffee_menus.csv', index=False)
