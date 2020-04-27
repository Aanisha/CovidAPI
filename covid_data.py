
# importing libraries 
from bs4 import BeautifulSoup as BS 
import requests 
from flask import Flask, jsonify,abort

app = Flask(__name__)
  
  
# method to get the info 
def getinfo(country_name): 
      
    # creating url using country name 
    url = "https://www.worldometers.info/coronavirus/country/" + country_name + "/"
      
    # getting the request from url  
    data = requests.get(url) 
  
    # converting the text  
    soup = BS(data.text, 'html.parser')    
      
    # finding meta info for cases 
    cases = soup.find_all("div", class_ = "maincounter-number") 
      
    # getting total cases number 
    total = cases[0].text 
      
    # filtering it 
    total = total[1 : len(total) - 2] 
       
    # getting recovered cases number 
    recovered = cases[2].text 
      
    # filtering it 
    recovered = recovered[1 : len(recovered) - 1] 
      
      
    # getting death cases number 
    deaths = cases[1].text 
      
    # filtering it 
    deaths = deaths[1 : len(deaths) - 1] 
      
    # saving details in dictionary 
    ans ={'Total Cases' : total, 'Recovered Cases' : recovered, 
                                 'Total Deaths' : deaths} 
      
   
    return ans 
   

@app.route('/covidapi/<string:country_name>', methods=['GET'])
def corona_country(country_name):

    if(country_name=="USA" or country_name=="UnitedStates"):
        country_name="us"
    if(country_name=="UK" or country_name=="United Kingdom"):
        country_name="uk"
    if(country_name=="UAE" or country_name=="United Arab Emirates"):
        country_name="united-arab-emirates"
    ans=getinfo(country_name)
    if(ans['Total Cases']==0):

        abort(404)

    return jsonify(ans)



def get_info(url): 
      
    # getting the request from url  
    data = requests.get(url) 
  
    # converting the text  
    soup = BS(data.text, 'html.parser') 
      
    # finding meta info for total cases 
    total = soup.find("div", class_ = "maincounter-number").text 
      
    # filtering it 
    total = total[1 : len(total) - 2] 
      
    # finding meta info for other numbers 
    other = soup.find_all("span", class_ = "number-table") 
      
    # getting recovered cases number 
    recovered = other[2].text 
      
    # getting death cases number 
    deaths = other[3].text 
      
    # filtering the data 
    deaths = deaths[1:] 
      
    # saving details in dictionary 
    ans ={'Total Cases' : total, 'Recovered Cases' : recovered,  
                                 'Total Deaths' : deaths} 
      
    # returnng the dictionary 
    return ans 
@app.route('/covidapi/all', methods=['GET'])
def corona(): 
# url of the corona virus cases 
    url = "https://www.worldometers.info/coronavirus/"
  
# calling the get_info method 
    ans = get_info(url) 
  
# printing the ans 
    return jsonify(ans)


if __name__ == '__main__':
    app.run(debug=True)



