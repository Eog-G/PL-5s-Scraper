from bs4 import BeautifulSoup
import requests
import random
import shutil
import pandas as pd
from os.path import exists
import time

class Player():

    def __init__(self, forename, surname, number, country, position) -> None:
        
        self.forename = forename
        self.surname = surname
        self.number = number
        self.country = country
        self.position = position
        
        

def get_national_players():

    countries = ['Germany', 'Scotland', 'England', 'France', 'Portugal', 'Brazil', 'Spain', 'Belgium', 'Argentina', 'Italy', 'Netherlands']
    links = ['https://en.wikipedia.org/wiki/' + x + '_national_football_team' for x in countries]

    html_text = requests.get('https://en.wikipedia.org/wiki/netherlands_national_football_team').text

    soup = BeautifulSoup(html_text, 'lxml')

    players = soup.find_all('tr', class_='nat-fs-player')

    for player in players:
        
        forename = player.th.a.text.split()[0]
        try:
            surname = player.th.a.text.split()[1]
            print(F"{forename[0]}. {surname}")
        except:
            print(F"{forename}")

def get_pl_players():

    URLS = []
    pl_players = []

    with open('pl_links.txt') as f:
        for line in f:
            URLS.append(line.strip())

    for link in URLS:

        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'lxml')
        players = soup.find_all('tr', class_='vcard agent')

        for player in players:
            temp = []
           
            cols = player.find_all('td')
            
            for loop,data in enumerate(cols):
                temp.append(data.text)

                if loop == 3:
                    temp.pop(3)
                    forename = data.text
                    split = data.text.find(" ")
                    
                    if split >= 0:
                        forename = data.text[0:split]
                        surname = data.text[split:-1]

                        split = surname.find("(")
                        
                        if split >= 0:
                            surname = surname[0:split-1]
                        
                        temp.append(surname)
                    
                    temp.append(forename)
            
            for i, x in enumerate(temp):
                x = x.replace("\n", "")
                x = x.replace("\xa0", "")
                temp[i] = x

            if len(temp) == 4:
                temp.append(" ")

            number = temp[0]
            position = temp[1]
            country = temp[2]
            surname = temp[3]
            forename = temp[4]

            new_player = Player(forename, surname, number, country, position)

            pl_players.append(new_player)

    return pl_players

def sort_players(pl_players):

    GK = []
    DF = []
    MF = []
    FW = []

    for x in pl_players:
        
        match x.position:
            
            case "GK":
                GK.append(x)
            case "DF":
                DF.append(x)
            case "MF":
                MF.append(x)
            case "FW":
                FW.append(x)
    
    return GK,DF,MF,FW

def generate_5s_team(GK,DF,MF,FW):

    gk = GK[random.randint(0,len(GK)-1)]
    df = DF[random.randint(0,len(DF)-1)]
    mf1 = MF[random.randint(0,len(MF)-1)]
    mf2 = MF[random.randint(0,len(MF)-1)]
    fw = FW[random.randint(0,len(FW)-1)]

    print_centre(F"{fw.forename[0]}{fw.surname}")
    print("")
    print_centre(F"{mf1.forename[0]}{mf1.surname}  {mf2.forename[0]}{mf2.surname}")
    print("")
    print_centre(F"{df.forename[0]}{df.surname}")
    print("")
    print_centre(F"{gk.forename[0]}{gk.surname}")


def print_centre(s):
    print(s.center(shutil.get_terminal_size().columns))

def save_data(pl_players):  
    df = pd.DataFrame([(x.forename, x.surname, x.country, x.number, x.position) for x in pl_players], columns=['Forename', 'Surname', 'Country', 'Number', 'Position'])
    df.to_excel('players.xlsx', sheet_name='players', index=False)

def main():

    start = time.time()

    pl_players = get_pl_players()

    GK, DF, MF, FW = sort_players(pl_players)

    
    generate_5s_team(GK, DF, MF, FW)
    print("\n")
    print_centre("----- VS -----")
    print("\n")
    generate_5s_team(GK, DF, MF, FW)

    end = time.time()

    print(end - start)

    if(not exists("players.xlsx")):
        save_data(pl_players)
        
main()









#SIMPLE HTML EXAMPLE

#with open('home.html', 'r') as html:
#    content = html.read()
#    
#    soup = BeautifulSoup(content, 'lxml')
#    
#    courses_html_tags = soup.find_all('h5')
#    for course in courses_html_tags:
#        continue
#        print(course.text)
#
#    course_cards = soup.find_all('div', class_='card')
#    for course in course_cards:
#        course_name = course.h5.text
#        course_price = course.button.text.split()[-1]
#
#        print(f"{course_name} costs {course_price}")