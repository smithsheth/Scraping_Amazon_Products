# importing libraries
from bs4 import BeautifulSoup
import requests
import csv

def main(URL,writer):
  
    webpage = requests.get(URL)

    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    outer_div = soup.find_all('div', {"class":"sg-col-inner"})
    for outer in outer_div:
        inner_div=outer.find_all('div', {"class":"sg-col-20-of-24"})
        for product in inner_div:
    
              # retrieving product URL
                try:
                    access_url = product.find('a', {"class":"a-link-normal"})
                    product_url=access_url.get("href")
                    product_url="https://www.amazon.in/"+product_url
                    # try:
                    #     ASIN,Manufacturer=fetch_details(product_url)
                    #     print(ASIN)
                    # except AttributeError:
                    #      print("Error")
                           
                except AttributeError:
                    product_url= "NA"
                print("product URL = ", product_url)
            

                # retrieving product title
                try:
     
                    title = product.find('span', {'class': 'a-size-medium'})
                    title_value = title.string

                    title_string = title_value.strip().replace(',', '')

                except AttributeError:
                    title_string = "NA"
                print("product Title = ", title_string)
            

                # retrieving price
                try:
                    price = product.find('span', {'class': 'a-price-whole'}).string.strip().replace(',', '')
                
                except AttributeError:
                    price = "NA"
                print("product Price = ", price)
    
                 # retrieving rating
                try:
                    rating = product.find('span', {'class': 'a-icon-alt'}).string.strip().replace(',', '')
                except:
                    rating = "NA"
                print("Overall rating = ", rating)
             
                # retrieving reviews
                try:
                    review_count = product.find('span', {'class': 'a-size-base'}).string.strip().replace(',', '')

                except AttributeError:
                    review_count = "NA"
                print("Total reviews = ", review_count)

                #writing all data
                writer.writerow([product_url,title_string,price,rating,review_count])
                
                print("--------Break-----------")
            

def fetch_details(URL):
    webpage = requests.get(URL)
    asin_value=""
    manufacturer=""
    product_description=""
    # Creating the Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    outer_div = soup.find_all('div', {"class":"a-container"})
    for outer in outer_div:
        inner_div = outer.find_all('ul',{"class","a-unordered-list"})
        for inner in inner_div:
            asin_span = inner.find('span', string='ASIN')
            asin_value = asin_span.find_next_sibling('span').text
        for inner in inner_div:
            manufacturer_tr=inner.find('th',string="Manufacturer")
            manufacturer=manufacturer_tr.find_next_sibling('td').text    

    return asin_value,manufacturer     

if __name__ == '__main__':
 #Opening csv file to save data
    with open("out.csv", mode='w',newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Product URL", "Product Title", "Product Price", "Product Rating", "Product Reviews"])

                #pagination
                for i in range(1,20):
                    url="https://www.amazon.in/s?k=bags&page="+str(i)+"&crid=2M096C61O4MLT&qid=1688680233&sprefix=ba%2Caps%2C283&ref=sr_pg_"+str(i)
                    main(url,writer)
