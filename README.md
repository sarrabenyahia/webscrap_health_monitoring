# ATC DDD Web Scraping

This project demonstrates web scraping of the ATC DDD Index website using the `WHOCCAtcDddIndex` class. It retrieves data for different levels of the ATC classification and saves the results into separate Excel files. Additionally, it provides an example of concatenating these Excel files into a single file.

## Prerequisites

- Python 3
- Pandas library (`pip install pandas`)
- BeautifulSoup library (`pip install beautifulsoup4`)
- httpx library (`pip install httpx`)

## Usage

1. Clone the repository:

````bash
git clone https://github.com/sarrabenyahia/ATC-DDD-Web-Scraping.git
cd webscrap_health_monitoring
````

2. Install the required dependencies:
````
pip install -r requirements.txt
````

3. Run the script:

````
cd bs4
python act_ddd_script.py
````

The script will retrieve data for different levels of the ATC classification and save the results into separate Excel files (demo_atc_l1.xlsx, demo_atc_l2.xlsx, demo_atc_l3.xlsx, demo_atc_l4.xlsx, demo_atc_l5.xlsx). It will also concatenate these files into a single Excel file named concatenated_atc_data.xlsx.

## File Descriptions
- whocc.py: Contains the WHOCCAtcDddIndex class that performs the web scraping and data retrieval.
- act_ddd_script.py: The main script that utilizes the WHOCCAtcDddIndex class to scrape the data and save it to Excel files.
- demo_atc_l1.xlsx: Excel file containing data for the Level 1 of the ATC classification.
- demo_atc_l2.xlsx: Excel file containing data for the Level 2 of the ATC classification.
- demo_atc_l3.xlsx: Excel file containing data for the Level 3 of the ATC classification.
- demo_atc_l4.xlsx: Excel file containing data for the Level 4 of the ATC classification.
- demo_atc_l5.xlsx: Excel file containing data for the Level 5 of the ATC classification.
- concatenated_atc_data.xlsx: Excel file that is created by concatenating the Level 1 to Level 5 Excel files.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to modify and adapt the script according to your requirements.

## Acknowledgements
Special thanks to the World Health Organization Collaborating Centre for Drug Statistics Methodology (WHOCC) for providing the ATC DDD Index data.

## Note
Web scraping should be used responsibly and in accordance with the website's terms of service. Always be mindful of not overloading the target website with too many requests.


