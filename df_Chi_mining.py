import pandas as pd
import os
import re
from geopy.geocoders import Nominatim

path = os.getcwd()+ '/'

names = ['Current_Price', 'Address', 'City', 'Last_sold_date', 'Last_sold_price', 'Other_info', 'House_details']
df_chi=pd.read_csv('Chicago_hh_info_all_v3.csv', names = names)

#### get city state and zipcode columns
for row in df_chi.City:
    names = row.split(' ')
    City = names[0][:7]
    State = names[1]
    Zipcode = names[2]
df_chi['City_C'] = City
df_chi['State'] = State
df_chi['Zipcode'] = Zipcode

#regular expressiong to capture the key words in the 

Beds = []
Baths = []
SQFT = []
Lot_Size = []
F_Type = []
for row in df_chi.Other_info:
    m = re.search(r"(\d)\sbeds|(\d)\sbed", row) 
    if m:
        Beds.append(m.group())
    else:
        Beds.append(None)
    b = re.search(r"(\d\.\d\sbath)|(\d\sbaths)|(\d\sbaths)",row)
    if b:
        Baths.append(b.group())
    else:
        Baths.append(None)
    # Here SQFT and Lot_Size might be overlap, in the future if SQFT ==Lot_Size, SQFT is none 
    s = re.search(r"(\d,\d+)\ssqft", row)
    if s:
        SQFT.append(s.group())
    else:
        SQFT.append(None)
    l = re.search(r"(\d,\d+)\ssqft\slot\ssize|(\d\.\d+)\sacres\slot\ssize",row)
    if l:
        Lot_Size.append(l.group())
    else:
        Lot_Size.append(None)
    t = re.search(r"(Multi-Family)|Multi-Family\sHome|Single-Family\sHome|Townhouse|Condo|Unknown", row)
    if t:
        F_Type.append(t.group())
    else:
        F_Type.append(None)
    
df_chi['Beds'] = Beds
df_chi['Baths'] = Baths
df_chi['SQFT'] = SQFT
df_chi['Lot_Size'] =Lot_Size
df_chi['F_Type'] =F_Type

Built_ya = []
Roof = []
for row in df_chi.House_details:
    bu = re.search(r"Built\sIn\s(\d+)",row)
    if bu:
        Built_ya.append(bu.group())
    else:
        Built_ya.append(None)
    r = re.search(r"Roof:(\s\w+\s\w+)|Roof:(\sTar\s&\sGravel)|Roof:(\sShingle\s)|Roof:(\sTile)", row)
    if r:
        Roof.append(r.group())
    else:
        Roof.append(None)
#     print Roof
df_chi['Built_ya'] =Built_ya
df_chi['Roof'] = Roof

###convert the datatype, and get rid of some string

#This column is gonna use for geocoding

New_Address = []
for row in df.Address:
     New_Address.append(re.sub("#\d+[A-Z]\w+|#\d+[A-Z]|#[A-Z]\d+|#\d+|#[A-Z]|", "", row))
df['New_Address'] = New_Address

df['Address_GEO'] = df['New_Address'] + ', ' + df['City'] + ', ' + df['Country']

nom = Nominatim()
##covert Address_GEO column to geo coordination, and it will take awhile
df['Coordinates'] = df['Address_GEO'].apply(nom.geocode)

