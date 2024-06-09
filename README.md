# Web Scraper for Product Search on Amazon

Welcome to the Amazon Web Scraper for Product Search! This project is designed to help you search for products on Amazon and retrieve detailed information about them. This can be useful for market research, price comparison, and monitoring product availability.

## Features
- Search for products by keyword.
- Retrieve product details including title, price, rating, number of reviews, and availability.
- Export the scraped data to a CSV file for further analysis.
- Easy-to-use command line interface.
 
## Installation
### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)
- Git

### Clone Repository
     git clone https://github.com/yourusername/web-scraper-for-product-search.git
     cd web-scraper-for-product-search

### Install Dependencies
     pip install -r requirements.txt

## Usage
### Command Line Interface
To use the scraper from the command line, navigate to the project directory and run the following command:

bash
     scraper.py your search term
Replace "your search term" with the product keyword you want to search for.

Example
bash
     Amazon web scraper.py laptop
This will search for laptops on Amazon and display the results in the terminal.

### Output
The scraper will save the results in a CSV file named results.csv in the project directory. The CSV file will contain the following columns:
- Product Description
- Price
- Rating
- Number of Reviews
- Product url

## Project Structure
- Amazon web scraper.py: The main script to run the scraper.
- requirements.txt: A file listing the required Python libraries.
- README.md: This file.

## Dependencies
The project uses the following Python libraries:
- requests: For making HTTP requests to Amazon.
- BeautifulSoup: For parsing HTML and extracting product information.
- pandas: For data manipulation and exporting to CSV.

## Disclaimer
This project is for educational purposes only. Scraping Amazon’s website may violate their terms of service. Use this tool responsibly and at your own risk. Consider using Amazon's official API for accessing product data.

## Contributing
Contributions are welcome! Please create a pull request with a detailed description of the changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.





     
