#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 13:01:49 2023

@author: troyladka
"""

from bs4 import BeautifulSoup
import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import re

#url = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label%3Adigital_humanities&btnG='
#page_count = 0
users_info_master_list=[]
field_categories = ['digital_humanities', 'network_science', 'computational_social_science', 'social_networks', 'modeling_and_simulation']
 
for field in field_categories:
    url = 'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors=label%3A'+field+'&btnG='
    page_count = 0
    while page_count < 100:
    
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280x800")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        if page_count == 0:
            driver_path = '/path/to/chromedriver'
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(url)
            driver.implicitly_wait(10)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            
            next_page_link = soup.findAll('button')[2]['onclick'].split('\\')[7][3:]
            next_page_url = 'https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:digital_humanities&after_author='+next_page_link+'&astart='+str(page_count)
        
        while page_count > 1:
            driver_path = '/path/to/chromedriver'
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(next_page_url)
            driver.implicitly_wait(10)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            next_page_link = soup.findAll('button')[2]['onclick'].split('\\')[7][3:]
            next_page_url = 'https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:digital_humanities&after_author='+next_page_link+'&astart='+str(page_count)
            break
        
        divs = soup.findAll('div', class_='gsc_1usr')
        
        names = [item.find('h3', class_='gs_ai_name').text for item in divs]
        researcher_ids_links = [item.find('a', href=True)['href'] for item in divs]
        researcher_ids = [item.find('a', href=True)['href'].split('=')[2] for item in divs]
        
        fields_tags = [item.findAll('a', class_='gs_ai_one_int') for item in divs]
        fields=[]
        for tags in fields_tags:
            temp=[]
            for tag in tags:
                temp.append(tag.text)
            while len(temp) < 5:
                temp.append('')
            fields.append(temp)
            
        
        full_page_citation_stats = []
        for link in researcher_ids_links:
            driver.get('https://scholar.google.com'+link)
            driver.implicitly_wait(10)
            html_user = driver.page_source
            user_soup = BeautifulSoup(html_user, 'lxml')
        
            years_tags = user_soup.findAll('span', class_='gsc_g_t')
            years = [int(item.text) for item in years_tags]
            citation_per_year_tags = user_soup.findAll('span', class_='gsc_g_al')
            citation_per_year = [int(item.text) for item in citation_per_year_tags]
            citations_dict = dict(zip(years, citation_per_year))
        
            citations_dict_full = {year: '' for year in range(1991,2014)}
            
        
            for key in citations_dict_full.keys():
                if key in citations_dict.keys():
                    citations_dict_full[key] = citations_dict[key]
        
            full_page_citation_stats.append(citations_dict_full)
        
       
        for i in range(10):
            temp_list=[names[i], researcher_ids[i]]
            temp_list.extend(fields[i])
            temp_list.extend(full_page_citation_stats[i].values())
            users_info_master_list.append(temp_list)
        
        
        page_count+=10
    
final_data = []
for inner_list in users_info_master_list:
    if inner_list not in final_data:
        final_data.append(inner_list)
        
with open('my_data.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(['Name', 'UserID', 'Area_Of_Expertise_1', 'Area_Of_Expertise_2', 'Area_Of_Expertise_3', 'Area_Of_Expertise_4', 'Area_Of_Expertise_5', '1991', '1992', '1993','1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013'])
    for row in final_data:
        writer.writerow(row)

    


    
        
        







