#!/usr/bin/env python
#encoding: utf-8
import re
from collections import defaultdict

# defines the components of a query result from Google.
class GoogleQuery:
    
    def __init__(self, title, snip, link):
        self.title = title
        self.snip = snip
        self.link = link
    
    '''
    returns the title, snip, and link associated with a Google result
    '''
    def __str__(self):
        return ('title: ' + self.title + '\nsnip: ' + self.snip + '\nlink: ' + self.link)

# note that you should not need to use this class. this class defines the possible locations 
# of a landmark. it differs from the location object in that it stores multiple possible location
# objects, while the location object only stores one possible guess for a city location.
class LocationPossibilities:
    
    def __init__(self, cities, country):
        self.cities = cities
        self.country = country

    '''
    returns the list of all the possible cities along with the country which contains the city
    '''
    def __str__(self):
        locations = ''
        for city in self.cities:
            locations += (city + ', ')
        locations = locations[:-2]
        return ('possible cities: ' + locations + '\ncountry: ' + self.country)

# defines the components of a location.
class Location:
    
    def __init__(self, city, country):
        self.city = city
        self.country = country

    '''
    returns the name of the city and country associated with the landmark
    '''
    def __str__(self):
        return ('city: ' + self.city + '\ncountry: ' + self.country)

class Googling:

    # reads in data for a set of results for a single query
    def readInSegment(self, lines):
        queryResults = []
        for i in range(0, len(lines), 3):
            queryResults.append(GoogleQuery(lines[i], lines[i + 1], lines[i + 2]))
        return queryResults
    
    # reads in data from a string rather than a file. assumes the same text file structure as readInData
    def readString(self, infoString):
        queryData = []
        lines = infoString
        startline = 0
        endline = 0
        while startline < len(lines):
            i = startline
            while i < len(lines) and len(lines[i].strip()) > 0: # reads for a query until an empty line or the end of the file
                i += 1
            endline = i
            queryData.append(self.readInSegment(lines[startline:endline]))
            startline = endline + 1 
        return queryData
    
    # reads in the tagged query results output by Google. takes in the name of the file containing the tagged Google results.
    def readInData(self, googleResultsFile):
        queryData = []
        infile = open(googleResultsFile)
        lines = infile.readlines()
        infile.close()
        startline = 0
        endline = 0
        while startline < len(lines):
            i = startline
            while i < len(lines) and len(lines[i].strip()) > 0: # reads for a query until an empty line or the end of the file
                i += 1
            endline = i
            queryData.append(self.readInSegment(lines[startline:endline]))
            startline = endline + 1 
        return queryData
    
    # takes a line and parses out the correct possible locations of the landmark for that line.
    # returns a LocationPossibilities object as well as the associated landmark
    def readGoldEntry(self, line):
        parts = line.split('\t')
        locationParts = parts[2].split(',')
        cities = locationParts[0].split('/')
        return LocationPossibilities(cities, locationParts[1].lower().strip()), parts[1].lower().strip()
    
    # reads in a file containing data about the landmark and where it's located 
    # returns a list of LocationPossibilities object as well as a list of landmarks. takes 
    # in the name of the gold file
    def readInGold(self, goldFile):
        goldData = []
        landmarks = []
        infile = open(goldFile)
        lines = infile.readlines()
        infile.close()
        for line in lines:
            goldEntry, landmark = self.readGoldEntry(line)
            goldData.append(goldEntry)
            landmarks.append(landmark)
        return goldData, landmarks
            
    # in this method, you must return Location object, where the first parameter of the constructor is the city where
    # the landmark is located and the second parameter is the state or the country containing the city. 
    # the return parameter is a Location object. if no good answer is found, returns a GoogleQuery object with
    # empty strings as parameters
    
    # note that the method does not get passed the actual landmark being queried. you do not need this information,
    # as your primary task in this method is to simply extract a guess for the location of the landmark given
    # Google results. you can, however, extract the landmark name from the given queries if you feel that helps.
    def guessLocation(self, data):
        #TODO: use the GoogleQuery object for landmark to generate a tuple of the location
        # of the landmark

        countries = defaultdict(int)
        states = defaultdict(int)
        cities = defaultdict(int)
        location_re = r'<LOCATION>([^<]+)</LOCATION>'

        for d in data:
            snip = d.snip.replace("<em>","").replace("</em>","")

            # search location
            location_result = re.findall(location_re, snip)
            if location_result != None:
                for location in location_result:
                    loc = location.lower()
                    if loc in self.countries:   # countries
                        countries[loc] += 1
                    elif loc in self.states:    # states
                        states[loc] += 1
                    else: # cities
                        cities[loc] += 1

        city = max(cities.items(), key=lambda x:x[1])[0]

        country = ""
        state = ""
        if len(countries) > 0:
            country = max(countries.items(), key=lambda x:x[1])[0]
        if len(states) > 0:
            state = max(states.items(), key=lambda x:x[1])[0]
        if len(countries) == 0:
            country = state
        elif country in ["united states", "america", "u.s.", "u.s.a."]:
            country = state
        return Location(city, country)
    
    # loops through each of the data associated with each query and passes it into the
    # guessLocation method, which returns the guess of the user
    def processQueries(self, queryData):
        #TODO: this todo is optional. this is for anyone who might want to write any initialization code that should only be performed once.
        countries = [
"Afghanistan",
"Albania",
"Algeria",
"America",
"American Samoa",
"Andorra",
"Angola",
"Anguilla",
"Antarctica",
"Antigua and Barbuda",
"Argentina",
"Armenia",
"Aruba",
"Ascension Island",
"Australia",
"Austria",
"Azerbaijan",
"Bahamas",
"Bahrain",
"Bangladesh",
"Barbados",
"Belarus",
"Belgium",
"Belize",
"Benin",
"Bermuda",
"Bhutan",
"Bolivia",
"Bosnia and Herzegovina",
"Botswana",
"Bouvet Island",
"Brazil",
"British Indian Ocean Territory",
"Brunei Darussalam",
"Bulgaria",
"Burkina Faso",
"Burundi",
"Cambodia",
"Cameroon",
"Canada",
"Cape Verde",
"Cayman Islands",
"Central African Republic",
"Chad",
"Chile",
"China",
"Christmas Island",
"Cocos",
"Keeling",
"Colombia",
"Comoros",
"Democratic Republic of the Congo",
"Kinshasa",
"Congo",
"Republic of Brazzaville",
"Cook Islands",
"Costa Rica",
"Ivory Coast",
"Croatia",
"Cuba",
"Cyprus",
"Czech Republic",
"Denmark",
"Djibouti",
"Dominica",
"Dominican Republic",
"East Timor Timor-Leste",
"Ecuador",
"Egypt",
"El Salvador",
"Equatorial Guinea",
"Eritrea",
"Estonia",
"Ethiopia",
"Falkland Islands",
"Faroe Islands",
"Fiji",
"Finland",
"France",
"French Guiana",
"French Metropolitan",
"French Polynesia",
"French Southern Territories",
"Gabon",
"Gambia",
"Georgia",
"Germany",
"Ghana",
"Gibraltar",
"Great Britain",
"Greece",
"Greenland",
"Grenada",
"Guadeloupe",
"Guam",
"Guatemala",
"Guernsey",
"Guinea",
"Guinea-Bissau",
"Guyana",
"Haiti",
"Heard and Mc Donald Islands",
"Holy See",
"Honduras",
"Hong Kong",
"Hungary",
"Iceland",
"India",
"Indonesia",
"Iran",
"Islamic Republic of Iran",
"Iraq",
"Ireland",
"Isle of Man",
"Israel",
"Italy",
"Jamaica",
"Japan",
"Jersey",
"Jordan",
"Kazakhstan",
"Kenya",
"Kiribati",
"Korea",
"North Korea",
"Republic of Korea",
"South Korea",
"Kosovo",
"Kuwait",
"Kyrgyzstan",
"Lao",
"Latvia",
"Lebanon",
"Lesotho",
"Liberia",
"Libya",
"Liechtenstein",
"Lithuania",
"Luxembourg",
"Macau",
"Macedonia",
"Madagascar",
"Malawi",
"Malaysia",
"Maldives",
"Mali",
"Malta",
"Marshall Islands",
"Martinique",
"Mauritania",
"Mauritius",
"Mayotte",
"Mexico",
"Micronesia",
"Moldova",
"Monaco",
"Mongolia",
"Montenegro",
"Montserrat",
"Morocco",
"Mozambique",
"Myanmar",
"Burma",
"Namibia",
"Nauru",
"Nepal",
"Netherlands",
"Netherlands Antilles",
"New Caledonia",
"New Zealand",
"Nicaragua",
"Niger",
"Nigeria",
"Niue",
"Norfolk Island",
"Northern Mariana Islands",
"Norway",
"Oman",
"Pakistan",
"Palau",
"Palestinian National Authority",
"Panama",
"Papua New Guinea",
"Paraguay",
"Peru",
"Philippines",
"Pitcairn Island",
"Poland",
"Portugal",
"Puerto Rico",
"Qatar",
"Reunion Island",
"Romania",
"Russia",
"Russian",
"Russian Federation",
"Rwanda",
"Saint Kitts and Nevis",
"Saint Lucia",
"Saint Vincent and the Grenadines",
"Samoa",
"San Marino",
"Sao Tome and Pr_ncipe",
"Saudi Arabia",
"Senegal",
"Serbia",
"Seychelles",
"Sierra Leone",
"Singapore",
"Slovakia",
"Slovak Republic",
"Slovenia",
"Solomon Islands",
"Somalia",
"South Africa",
"South Georgia and South Sandwich Islands",
"South Sudan",
"Spain",
"Sri Lanka",
"Saint Helena",
"St. Pierre and Miquelon",
"Sudan",
"Suriname",
"Svalbard and Jan Mayen Islands",
"Swaziland",
"Sweden",
"Switzerland",
"Syria",
"Syrian Arab Republic",
"Taiwan",
"Republic of China",
"Tajikistan",
"Tanzania",
"Thailand",
"Tibet",
"Timor-Leste",
"East Timor",
"Togo",
"Tokelau",
"Tonga",
"Trinidad and Tobago",
"Tunisia",
"Turkey",
"Turkmenistan",
"Turks and Caicos Islands",
"Tuvalu",
"Uganda",
"Ukraine",
"United Arab Emirates",
"United Kingdom",
"United States",
"United States of America",
"U.S.A.",
"U.S.",
"U.S. Minor Outlying Islands",
"Uruguay",
"Uzbekistan",
"Vanuatu",
"Vatican City State",
"Holy See",
"Venezuela",
"Vietnam",
"Virgin Islands",
"British",
"Wallis and Futuna Islands",
"Western Sahara",
"Yemen",
"Zaire",
"Zambia",
"Zimbabwe",
]
        states = [
"Alabama",
"Alaska",
"American Samoa",
"Arizona",
"Arkansas",
"California",
"Colorado",
"Connecticut",
"Delaware",
"District of Columbia",
"Florida",
"Georgia",
"Guam",
"Hawaii",
"Idaho",
"Illinois",
"Indiana",
"Iowa",
"Kansas",
"Kentucky",
"Louisiana",
"Maine",
"Maryland",
"Massachusetts",
"Michigan",
"Minnesota",
"Mississippi",
"Missouri",
"Montana",
"Nebraska",
"Nevada",
"New Hampshire",
"New Jersey",
"New Mexico",
"New York",
"North Carolina",
"North Dakota",
"Northern Marianas Islands",
"Ohio",
"Oklahoma",
"Oregon",
"Pennsylvania",
"Puerto Rico",
"Rhode Island",
"South Carolina",
"South Dakota",
"Tennessee",
"Texas",
"Utah",
"Vermont",
"Virginia",
"Virgin Islands",
"Washington",
"West Virginia",
"Wisconsin",
"Wyoming",
        ]
        self.countries = set()
        for country in countries:
            self.countries.add(country.lower())
        self.states = set()
        for state in states:
            self.states.add(state.lower())

        guesses = [''] * len(queryData)
        for i in range(len(queryData)):
            guesses[i] = self.guessLocation(queryData[i])
        return guesses
    
    # prints out the results as described in the handout
    def printResults(self, correctCities, incorrectCities, noguessCities, correctCountries, incorrectCountries, noguessCountries, landmarks, guesses, gold):
        print('LANDMARK\tYOUR GUESSED CITY\tCORRECT CITY/CITIES\tYOUR GUESSED COUNTRY\tCORRECT COUNTRY')
        correctGuesses = set(correctCities).intersection(set(correctCountries))
        noGuesses = set(noguessCities).union(set(noguessCountries))
        incorrectGuesses = set(incorrectCities).union(set(incorrectCountries))
        print('=====CORRECT GUESSES=====')
        for i in correctGuesses:
            print(landmarks[i] + '\t' + guesses[i].city + '\t' + str(gold[i].cities) + '\t' + guesses[i].country + '\t' + gold[i].country)
        print('=====NO GUESSES=====')
        for i in noGuesses:
            print(landmarks[i] + '\t' + guesses[i].city + '\t' + str(gold[i].cities) + '\t' + guesses[i].country + '\t' + gold[i].country)
        print('=====INCORRECT GUESSES=====')
        for i in incorrectGuesses:
            print(landmarks[i] + '\t' + guesses[i].city + '\t' + str(gold[i].cities) + '\t' + guesses[i].country + '\t' + gold[i].country)
        print('=====TOTAL SCORE=====')
        correctTotal = len(correctCities) + len(correctCountries)
        noguessTotal = len(noguessCities) + len(noguessCountries)
        incorrectTotal = len(incorrectCities) + len(incorrectCountries)
        print('correct guesses: ' + str(correctTotal))
        print('no guesses: ' + str(noguessTotal))
        print('incorrect guesses: ' + str(incorrectTotal))
        print('total score: ' + str(correctTotal - incorrectTotal) + ' out of ' + str(correctTotal + noguessTotal + incorrectTotal))
    
    # takes a list of Location objects and prints a list of correct and incorrect answers as well as scores the results
    def scoreAnswers(self, guesses, gold, landmarks):
        correctCities = []
        incorrectCities = []
        noguessCities = []
        correctCountries = []
        incorrectCountries = []
        noguessCountries = []
        for i in range(len(guesses)):
            if guesses[i].city.lower() in gold[i].cities:
                correctCities.append(i)
            elif guesses[i].city == '':
                noguessCities.append(i)
            else:
                incorrectCities.append(i)
            if guesses[i].country.lower() == gold[i].country.lower():
                correctCountries.append(i)
            elif guesses[i].country == '':
                noguessCountries.append(i)
            else:
                incorrectCountries.append(i)
        self.printResults(correctCities, incorrectCities, noguessCities, correctCountries, incorrectCountries, noguessCountries, landmarks, guesses, gold)
    
if __name__ == '__main__':
    googleResultsFile = '../data/googleResults_tagged.txt' # file where Google query results are read
    goldFile = '../data/landmarks.txt' # contains the results 
    googling = Googling()
    queryData = googling.readInData(googleResultsFile)
    goldData, landmarks = googling.readInGold(goldFile)
    guesses = googling.processQueries(queryData)
    googling.scoreAnswers(guesses, goldData, landmarks)
