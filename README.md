# Viva Real - Web-Scraping
Extract properties information on [Viva Real](https://www.vivareal.com.br/venda/ceara/fortaleza/) - Education Purpose Only

# Requirements
* [Selenium](https://selenium-python.readthedocs.io/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Pandas](https://pandas.pydata.org/)
* [Chromedriver](https://chromedriver.chromium.org/downloads)

# Information Extracted
Property: Address, Neighborhood, Area, Rooms, Bathrooms, Parking spaces and Price. 

The data is extracted and saved in a CSV file, and all the pages are downloaded and saved in *SavedPages* folder. 

# How to use
1) Install all necessary libraries in *Requirements*. 

2) Download the compatible [Chromedriver](https://chromedriver.chromium.org/downloads) version to your system. 

3) Get the link of the **first page result** (from Viva Real) to sweep through the selected pages and then change the line code maintaining the same pattern:

```python
...
# Get Link and Change page number - Edit if necessary !
    link = 'https://www.vivareal.com.br/venda/ceara/fortaleza/?pagina='+str(page)+'#onde=BR-Ceara-NULL-Fortaleza&tipos=apartamento_residencial'
...
```

4) CSV File: **VivaRealData.csv**

5) Pages Downloaded: **SavedPages** folder

# Screenshot
![vivaReal-web](https://user-images.githubusercontent.com/56649205/72991260-71cd6700-3dd0-11ea-9b7a-f1097ecc445b.PNG)
