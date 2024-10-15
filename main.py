from bs4 import BeautifulSoup
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://www.amazon.in/s?k=iphones&crid=YPQNTL63U0XI&sprefix=iphone%2Caps%2C232&ref=nb_sb_noss_2"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
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