import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import sqlite3
import os


#establish database connection
#connection = sqlite3.connect('DataEngineer_Jobs.db')
#c = connection.cursor()

#Establish User Inputs
#job_what = input("Enter Job title, Keywords, or Company")
#job_where = input("Enter Job Location")


#establish path for csv saving
save_path = 'C:/Users/jpank/OneDrive/Documents/Data Science/Python Scripts/WebScraper/indeedScrape/IndeedScrapeResults'
file_name = datetime.now().strftime('results-%Y-%m-%d.csv')
completeName = os.path.join(save_path, file_name)

def get_url(position, location):
    """Generate a url from position and location"""
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

def get_record(card):
    """Extract job data from a single record"""
    titleTag = card.h2
    job_title = titleTag.text.strip('new')
    try:
        job_company = card.div.pre.a.text
    except:
        job_company = card.div.pre.span.text
    else:
        pass
    job_location = card.div.pre.div.text
    try:
        job_salary = card.find("span", "salary-snippet").text.strip()
    except:
        job_salary = ''
    job_summary = card.find('div', {'class':'job-snippet'}).text.strip()
    job_postDate = card.find('span', {'class':'date'}).text
    today = datetime.today().strftime('%Y-%m-%d')
    
    record = (job_title, job_company, job_location, job_postDate, today, job_summary, job_salary)
    
    return record


def main(position, location):
    """Run the main program routine"""
    records = []
    url = get_url(position, location)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'slider_container')
    
        for card in cards:
            record = get_record(card)
            records.append(record) 
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
    #c.execute('''INSERT INTO DataEngineer_Jobs VALUES(?,?,?,?,?,?,?)''',(JobTitle, Company, Location, PostDate, ExtractDate, Summary, Salary))
    #code to export to CSV, 
    with open(completeName, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle', 'Company', 'Location', 'PostDate', 'ExtractDate', 'Summary', 'Salary'])
        writer.writerows(records)

main('data engineer', 'Dallas, TX')