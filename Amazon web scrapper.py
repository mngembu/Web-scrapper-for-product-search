#!/usr/bin/env python
# coding: utf-8

# ## Building a web scrapper that extracts product search results from amazon.com <br> 

# In this notebook, I am building a web scrapper for amazon.com. Given a search term, this scrapper will extract records from all pages in a search result and store them in a csv file. <br>As an example, we will be using "bike lock" as search term.

# ### Installing and importing the packages/libraries

# In[1]:


pip install selenium


# In[2]:


pip install bs4


# In[3]:


import csv
from bs4 import BeautifulSoup
from selenium import webdriver


# In[4]:


# Creating an instance of the webdriver to start it up
driver = webdriver.Chrome("C:/Users/amari/Downloads/chromedriver_win32/chromedriver.exe")


# In[5]:


#navigate to the amazon website

url = 'https://www.amazon.com'
driver.get(url)


# In[6]:


# writing a function that will generate a url based on the search terms provided

def get_url(search_term):
    """Generate a url from search term"""
    template = 'https://www.amazon.com/s?k={}&crid=2LEXIUFP0SED4&sprefix={}%2Caps%2C148&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    return template.format(search_term, search_term)     #since the search term appears twice in the url when tried on amazon.com


# In[7]:


# Creating a url for the bike lock search

url = get_url("bike lock")
print(url)


# In[8]:


driver.get(url)


# ### Extracting the content of the page from the html in the background

# In[9]:


#creating soup object which will parse the html content from the page source
soup = BeautifulSoup(driver.page_source, 'html.parser')


# In[10]:


results = soup.find_all('div', {'data-component-type': 's-search-result'})


# In[11]:


len(results)


# ### Prototyping the extraction of a single record

# In[12]:


item = results[0]


# In[13]:


atag = item.h2.a


# In[14]:


description = atag.text.strip() 
description


# In[15]:


url = 'https://www.amazon.com' + atag.get('href')
url


# In[16]:


# getting the price
price_parent = item.find('span', 'a-price')
price = price_parent.find('span', 'a-offscreen').text


# In[17]:


# getting the ratings. Inspecting the stars shows that ratings are in the i tag

rating = item.i.text


# In[18]:


#getting the reviews

item.find('span', {'class':'a-size-base s-underline-text'}).text


# ### Generalizing the patttern of extraction within a function which can be applied to all the records on a page

# Here I incorporated some error handling. 5 attributes will be extracted from each record, but since some attributes may be missing in some records, AttributeError will need to be accomodated.

# Add error handling: The above code assumes each record contains all 5 attributes, but that's not the case

# In[19]:


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


# In[20]:


# apply the pattern to all records on the page 

records =[]
results = soup.find_all('div', {'data-component-type': 's-search-result'})

for item in results:
    record = extract_record(item)
    if record:   #ie, if record has something in it
        records.append(record)


# In[21]:


# viewing the first record
records[0]


# ### Getting the next page

# On the amazon page, if you click on 'Next' and oberve the url of the next page, you notice a parameter for page number. We can add this page parameter to the url using string formatting. Amazon search gives a maximum of 20 pages

# In[22]:


def get_url(search_term):
    """Generate a url from search term"""
    template = 'https://www.amazon.com/s?k={}&crid=2LEXIUFP0SED4&sprefix={}%2Caps%2C148&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    
    # add term query to url
    url = template.format(search_term, search_term)
    
    #add page query placeholder
    url += '&page{}'  #this gives a place to insert the next page number (with string formatting)
    
    return url


# ### Putting all together

# In[23]:


import csv
from bs4 import BeautifulSoup
from selenium import webdriver


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
    #startup the web driver
    driver = webdriver.Chrome("C:/Users/amari/Downloads/chromedriver_win32/chromedriver.exe")
    
    records = []
    url = get_url(search_term)
    
    for page in range (1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
                
    driver.close()
    
    #save data to csv
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'url'])
        writer.writerows(records)
    


# In[24]:


main('bike lock')


# In[ ]:





# In[ ]:




