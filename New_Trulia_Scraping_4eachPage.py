from bs4 import BeautifulSoup as soup
from urllib2 import urlopen as uReq
from urlparse import urljoin
import pandas as pd
from compiler.ast import flatten
import time
import glob
import os

#get property links for each page 
def get_house_link():
    page_links = []
    house_url = []
    containers_url = page_soup.findAll("a", {"class": "tileLink phm"})
    for link in containers_url:
        page_links.append(link['href'])
    base_url = 'https://www.trulia.com'

    for path in page_links:
        house_url.append(urljoin(base_url, path))
    return house_url


def extract_links(url):
    uClient = uReq(url)
    page_html = uClient.read()
    page_soup =  soup(page_html, 'html.parser')
    links = get_house_link()
    return links

def get_lat_long(url):
	lat_long = []
	uClient = uReq(url)
    page_html = uClient.read()
    page_soup =  soup(page_html, 'html.parser')
	latitute = [item['content'] for item in page_soup.findAll('meta',{'itemprop':"latitude"})]
    longitude = [item['content'] for item in page_soup.findAll('meta',{'itemprop':"longitude"})]
    lat_long.append(latitute)
    lat_long.append(longitude)
    lat_long_df = pd.DataFrame(lat_long)
    lat_long_df.to_csv('lat_long_df_Chi.csv')
    return lat_long


### all_chicago_links is a big list that contain all the property link in Chicago

#go through each page and extract important information
"""
e.g. get property price, number of baths & beds,
"""
# hh_url = 'https://www.trulia.com/property/3270184952-5217-W-Gladys-Ave-Chicago-IL-60644'

def get_hh_info(hh_url):
	hh_df =pd.DataFrame({'Current_Price' : [], 'Address' : [], 'Neighbourhood' : [],'Last_sold_date' : [], 'Last_Price':[],'Other_info':[],'House_details' : []})
	all_hh_info = []
	uClient = uReq(hh_url)
	page_html = uClient.read()
	page_soup =  soup(page_html, 'html.parser')
	pageinfo = page_soup.findAll("ul", {"class": "listInline mbn pdpFeatureList"})
	houseinfo = pageinfo[0].text.split('\n\n\n')
	text_content = [info.strip() for info in houseinfo if info !='']
	items = [item.split('\n') for item in text_content]
	strings = [string.split(',') for caption in items for string in caption]
	strings_ = [''.join(eles) if len(eles) >1 else eles for eles in strings]
        house_details = flatten(strings_)
	price = house_soup.select('span.h2.typeEmphasize')[0].text
	price1 = price.strip()
	address = house_soup.select('span.h2.typeEmphasize.pan.man.defaultLineHeight')[0].text
	address1 = address.strip()
	neighbourhood = house_soup.select('span.h6.typeWeightNormal.pts.typeLowlight.miniHidden.xxsHidden')[0].text
	neighbourhood1 = neighbourhood.strip()
	last_sold_date1 = house_soup.select('td.noWrap')[0].text
	his_price = house_soup.select('td.noWrap')[2].text
	his_price1 = price.strip()
	others = house_soup.select('ul.listInlineBulleted.man.pts')[0].text
	others =  others.split('\n')
	app_info1 = [other for other in others if other != '']
	all_hh_info.append(price1)
	all_hh_info.append(address1)
	all_hh_info.append(neighbourhood1)
	all_hh_info.append(last_sold_date1)
	all_hh_info.append(his_price1)
	all_hh_info.append(app_info1)
	all_hh_info.append(house_details)
	if len(all_hh_info) == len(hh_df.columns):
                hh_df.loc[len(hh_df.index)] = all_hh_info 
	columns = ['Current_Price', 'Address', 'Neighbourhood', 'Last_sold_date', 'Last_Price', 'Other_info', 'House_details']
	hh_df = pd.DataFrame(all_hh_info).T
	hh_df = hh_df[columns]
	return hh_df

#loop through and get all the liks for 300+pages 
url = 'https://www.trulia.com/IL/Chicago/'
all_chicago_links = []
all_lat_log = []
for page in range(1, 335):
    url_x = url + "%s_p"%str(page)
    links = extract_links(url_x)
    all_chicago_links.extend(links)
    all_lat_log.extend(get_lat_long(url_x))

    print "%s th page links extraction is done"%page
all_chicago_links_file = open('all_chicago_links.txt', 'w')
for item in 

for hh_url in all_chicago_links:
	hh_info = get_hh_info(hh_url)
	dt = time.strftime("%Y-%m-%d") + "_" + time.strftime("%H%M%S")
    file_name = str(dt) + ".csv"
    hh_info.to_csv('tmp/' +str(i)+ '_'+ file_name, index = False)

files = glob.glob('tmp/*.csv')
df_Chicago = pd.concat([pd.read_csv(f, index_col=False) for f in files], join = 'outer')
df_Chicago.to_csv("Chicago_hh_info_all.csv")
# os.system("rm tmp/*.csv")


"""
#first house
test = containers_houseinfo[0]
price = test.select('span.cardPrice.h5.man.pan.typeEmphasize.noWrap.typeTruncate')[0].text
beds = test.select('li')[1].text
baths = test.select('li')[2].text
sqft = test.select('li')[3].text
address = test.select('div.h6.typeWeightNormal.typeTruncate.typeLowlight.mvn')[0].text
neighbourhood=test.select('div.cardFooter.man.ptn.pbs')[0].text
price = test.select('span.cardPrice.h5.man.pan.typeEmphasize.noWrap.typeTruncate')[0].text
"""
