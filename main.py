from bs4 import BeautifulSoup
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://www.amazon.in/s?k=iphones&crid=YPQNTL63U0XI&sprefix=iphone%2Caps%2C232&ref=nb_sb_noss_2"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.amazon.in/",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br"
}

data = {
    'productName': [],
    'price': []
}

r = requests.get(url, headers=headers , verify=False)
soup = BeautifulSoup(r.text, "html.parser")
productSpans = soup.select("span.a-size-medium.a-color-base.a-text-normal")
priceSpans = soup.select("span.a-price-whole")

for product, price in zip(productSpans, priceSpans):
    data["productName"].append(product.get_text())
    data["price"].append(price.get_text())

df = pd.DataFrame.from_dict(data)
df.to_csv("data.csv", index=False)

df['price'] = df['price'].astype(str)

df['price'] = df['price'].str.replace('₹', '', regex=False).str.replace(',', '', regex=False)

df['price'] = pd.to_numeric(df['price'], errors='coerce')

df.dropna(subset=['price'], inplace=True)

df['price'] = df['price'].astype(float)

plt.figure(figsize=(10,6))
sns.histplot(df['price'], bins=20, kde=True)

plt.title('Price Distribution Of The Products')
plt.xlabel('Price (₹) (X)')
plt.ylabel('Frequency (Y)')

plt.savefig('price_distribution.png')
plt.show()

print(soup.prettify())