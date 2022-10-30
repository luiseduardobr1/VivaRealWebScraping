import requests, re, time, os, csv
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# Initialize lists
address=[]
neighbor=[]
area=[]
room=[]
bath=[]
park=[]
price=[]
condominium_fee=[]
web_page=[]

# Get the number of pages to extract information
pages_number=int(input('How many pages ? '))
tic = time.time()

# Configure chromedriver
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

# Create a folder to save downloaded HTML pages
dirName = 'SavedPages'
try:
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

# Loop through the website's pages
for page in range(1,pages_number+1):
   
    # Get Link and Change page number - Edit if necessary !
    link = 'https://www.vivareal.com.br/aluguel/ceara/fortaleza/apartamento_residencial/?pagina='+str(page)
    
    driver.get(link)
    time.sleep(2)
    data = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup_complete_source = BeautifulSoup(data.encode('utf-8'), "lxml")
    
    soup = soup_complete_source.find(class_='results-list js-results-list')    
    
    # download page html
    with open('SavedPages//site'+str(page)+'.html', 'w', encoding='utf-16') as outf:
        outf.write(str(soup_complete_source))

    # Web-Scraping
    for line in soup.findAll(class_="property-card__content-link js-card-title"):
        
        # Get Full Address and Neighborhood
        try:
            full_address=line.find(class_="property-card__address-container js-property-card-address js-see-on-map").text.strip()
            address.append(full_address) #Get all address
            if full_address[:3]=='Rua' or full_address[:7]=='Avenida' or full_address[:8]=='Travessa' or full_address[:7]=='Alameda':
                neighbor_first=full_address.strip().find('-')
                neighbor_second=full_address.strip().find(',', neighbor_first)
                if neighbor_second!=-1:
                    neighbor_text=full_address.strip()[neighbor_first+2:neighbor_second]
                    neighbor.append(neighbor_text) #Get all Neighborhood - Correct formatting
                else: # Neighbor can not be found
                    neighbor_text='-'
                    neighbor.append(neighbor_text) #Get all Neighborhood - Correct formatting
            else:
                get_comma=full_address.find(',')
                if get_comma!=-1:
                    neighbor_text=full_address[:get_comma]
                    neighbor.append(neighbor_text) #Get all Neighborhood - Problematic formatting   
                else:
                    get_hif=full_address.find('-')
                    neighbor_text=full_address[:get_hif]
                    neighbor.append(neighbor_text)
                    
            # Get Apto's Area    
            full_area=line.find(class_="property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area").text.strip()
            area.append(full_area)

            # Get Apto's Rooms
            full_room=line.find(class_="property-card__detail-item property-card__detail-room js-property-detail-rooms").text.strip()
            full_room=full_room.replace(' ','')
            full_room=full_room.replace('\n','')
            full_room=full_room.replace('Quartos','')
            full_room=full_room.replace('Quarto','')
            room.append(full_room) #Get apto's rooms

            # Get Apto's Bathrooms
            full_bath=line.find(class_="property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom").text.strip()        
            full_bath=full_bath.replace(' ','')
            full_bath=full_bath.replace('\n','')
            full_bath=full_bath.replace('Banheiros','')
            full_bath=full_bath.replace('Banheiro','')
            bath.append(full_bath) #Get apto's Bathrooms

            # Get Apto's parking lot
            full_park=line.find(class_="property-card__detail-item property-card__detail-garage js-property-detail-garages").text.strip()        
            full_park=full_park.replace(' ','')
            full_park=full_park.replace('\n','')
            full_park=full_park.replace('Vagas','')
            full_park=full_park.replace('Vaga','')
            park.append(full_park) #Get apto's parking lot

            # Get Apto's price
            full_price=line.find(class_="property-card__price js-property-card-prices js-property-card__price-small").text.strip()      
            full_price=full_price.replace(' ','')
            full_price=full_price.replace('\n','')
            full_price=full_price.replace('R$','')
            full_price=full_price.replace('.','')
            full_price=full_price.replace('Apartirde','')
            full_price=full_price.replace('SobConsulta','-')
            price.append(full_price) #Get apto's parking lot

            # Get Apto's condominium_fee
            full_condominium_fee=line.find(class_="js-condo-price")
            if full_condominium_fee:
                full_condominium_fee=full_condominium_fee.text.strip()
                full_condominium_fee=full_condominium_fee.replace(' ','')
                full_condominium_fee=full_condominium_fee.replace('\n','')
                full_condominium_fee=full_condominium_fee.replace('R$','')
                full_condominium_fee=full_condominium_fee.replace('.','')
            else:
                full_condominium_fee = '-'
            condominium_fee.append(full_condominium_fee)

            # Get Viva Real link url
            web_page.append('https://www.vivareal.com.br' + line['href'])

        except:
            continue
            
# Close chromedriver
driver.quit()

# Save as a CSV file
for i in range(0,len(neighbor)):
    combinacao=[address[i],neighbor[i],area[i],room[i],bath[i],park[i],price[i],condominium_fee[i],web_page[i]]
    df=pd.DataFrame(combinacao)
    with open('VivaRealData.csv', 'a', encoding='utf-16', newline='') as f:
        df.transpose().to_csv(f, encoding='iso-8859-1', header=False)

# Execution time
toc = time.time()
get_time=round(toc-tic,3)
print('Finished in ' + str(get_time) + ' seconds')
print(str(len(price))+' results!')
