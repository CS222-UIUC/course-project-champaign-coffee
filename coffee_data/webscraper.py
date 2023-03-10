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
    rows = soup.find_all('span', class_=['item-title', 'item-price'])
    # Open the CSV file for writing
    with open(file_name, mode='w', newline='', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Item', 'Price'])
    # Loop through each pair of item and price elements and write into CSV file
        for i in range(0, len(rows), 2):
            item = rows[i].text.strip()
            price = rows[i+1].text.strip()
            writer.writerow([item, price])

# Web Scraping Coffee Menus from: Espresso Royale, Cafe Bene, Cafe Kopi, and Brew Lab
menu_scraper('https://www.allmenus.com/il/champaign/839482-espresso-royale/menu/',
'espresso_royale_menu.csv')
menu_scraper('https://www.allmenus.com/il/urbana/760257-caffe-bene/menu/',
'cafe_bene_menu.csv')
menu_scraper('https://www.allmenus.com/il/champaign/254661-cafe-kopi/menu/',
 'cafe_kopi_menu.csv')
menu_scraper('https://www.allmenus.com/il/champaign/757433-brewlab-coffee/menu/',
 'brew_lab_menu.csv')


def append_shop_to_csv(file_name, shop):
    """Function to append shop name next to every row in CSV file"""
    csv_input = pd.read_csv(file_name, on_bad_lines='skip')
    csv_input['Shop'] = shop
    csv_input.to_csv(file_name)

append_shop_to_csv('espresso_royale_menu.csv', 'Espresso Royale')
append_shop_to_csv('cafe_bene_menu.csv', 'Cafe Bene')
append_shop_to_csv('cafe_kopi_menu.csv', 'Cafe Kopi')
append_shop_to_csv('brew_lab_menu.csv', 'Brew Lab')

# Open all 4 menus in order to merge into one
espresso_df = pd.read_csv('espresso_royale_menu.csv')
bene_df = pd.read_csv('cafe_bene_menu.csv')
brew_df = pd.read_csv('brew_lab_menu.csv')
kopi_df = pd.read_csv('cafe_kopi_menu.csv')

# Removing the + next to prices for consistency
espresso_df['Price'] = espresso_df['Price'].str.replace("+", "",regex=False)
bene_df['Price'] = espresso_df['Price'].str.replace("+", "",regex=False)

# Concatenate the 4 dataframes into a single dataframe
merged_df = pd.concat([kopi_df, espresso_df, bene_df, brew_df])

# File modifications
del merged_df['Unnamed: 0']
merged_df['Price'] = espresso_df['Price'].str.replace("$", "",regex=False)

# Write the merged dataframe to a new CSV file
merged_df.to_csv('champaign_coffee_menus.csv', index=False)
