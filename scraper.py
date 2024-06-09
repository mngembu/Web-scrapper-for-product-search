
import csv
from bs4 import BeautifulSoup
import requests
import argparse



def get_url(search_term):
    """Generate a url from search term"""
    template = 'https://www.amazon.com/s?k={}&crid=2LEXIUFP0SED4&sprefix={}%2Caps%2C148&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    
    # add term query to url
    url = template.format(search_term, search_term)
    
    #add page query placeholder
    url += '&page{}'  #this gives a place to insert the next page number (with string formatting)
    
    return url



def extract_record(item):
    """Extract and return data from a single record"""
   
    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    
    try:
        #price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
    
    try:
        #rating & review(rank)
        rating = item.i.text
        review_count = item.find('span', {'class':'a-size-base s-underline-text'}).text
    except AttributeError:
        rating = ''
        review_count = ''
    
    result = (description, price, rating, review_count, url)
    
    return result




def main(search_term):
    """Run main program routine"""
    
    #startup the web driver. Copy your user agent from 'whatismybrowser.com'
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36', 'Accept-Language':'en-US, en;q=0.5'})
    
    records = []
    url = get_url(search_term)
    
    for page in range (1, 21):
        webpage = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
                
    webpage.close()
    
    #save data to csv
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'url'])
        writer.writerows(records)
    
   

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='finds product details')
        parser.add_argument('search_term', metavar='search_term', type=str, help='enter your search term')
        args = parser.parse_args()
        search_term = args.search_term
        
        main(search_term)
        print("Search results saved to csv file")
    
    except KeyboardInterrupt:
        print("Search failed")
        






