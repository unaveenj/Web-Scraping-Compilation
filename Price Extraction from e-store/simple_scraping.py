from requests_html import HTMLSession
import pandas as pd
from time import sleep
from tqdm import tqdm

s = HTMLSession() #session object

def get_product_links():
    url = f'https://themes.woocommerce.com/storefront/product-category/clothing/page/'
    links = []
    start_page = 1
    status_code = 200
    while status_code == 200:
        print(f"Extracting link from page: {start_page}")
        new_url = f"{url}{start_page}"
        res = s.get(new_url)
        # using CSS selectors
        products = res.html.find('ul.products li')
        for product in products:
            links.append(product.find('a', first=True).attrs['href'])  # Find a tag for links and append to list
        start_page+=1
        status_code = s.get(f"{url}{start_page}").status_code
    print("End of extractions")
    print("Summary :")
    print(f"Pages Extract: {start_page}\nLinks Extracted:{len(links)}")
    return links

def get_product_details(link):
    r = s.get(link)
    prod_title = r.html.find('h1.product_title.entry-title', first=True).text.strip()
    price = r.html.find('p.price', first=True).text
    category = r.html.find('span.posted_in', first=True).text.strip('Cateogory: ')
    # Additional details for bags only
    try:
        weight = r.html.find('td.woocommerce-product-attributes-item__value', first=True).text.strip()
        dimensions = r.html.find('tr.woocommerce-product-attributes-item.woocommerce-product-attributes-item--dimensions',first=True).text.strip("Dimensions\n") + "m"
    except:
        weight ="None"
        dimensions="None"

    return [prod_title,price,category,weight,dimensions]
def generate_csv_file():
    titles = []
    prices = []
    categories = []
    weights = []
    dimensions = []
    urls = get_product_links()
    size = len(urls)
    for i in tqdm(range(0, size), desc="Getting Products"):
        sleep(.1)
        prod,price,cat,weight,dim = get_product_details(urls[i])
        titles.append(prod)
        prices.append(price)
        categories.append(cat)
        weights.append(weight)
        dimensions.append(dim)

    output = {
        'Product' : titles,
        'Price' : prices,
        'Category' : categories,
        'Weight' : weights,
        'Dimensions': dimensions
    }
    df = pd.DataFrame(output)
    df.to_csv('Tracker.csv')
    print("Data saved to Tracker.csv!")


def main():
    generate_csv_file()

if __name__ == '__main__':
    main()

