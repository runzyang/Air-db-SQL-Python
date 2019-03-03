import requests
from lxml import etree
import pymysql


# Multi threading for next update
# Flight might not available today for url

def getFlight(flight, num):
    url = 'https://www.flightstats.com/v2/flight-tracker/' + flight + '/' + str(num) + '?year=2018&month=12&date=10'
    url_time = 'https://www.flightstats.com/v2/flight-details/' + flight + '/' + str(
        num) + '?year=2018&month=12&date=10'

    r = requests.get(url).text
    s = etree.HTML(r)
    flight_code = '//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div[1]/div[1]/text()'
    flight_company = '//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div[1]/div[2]/text()'
    flight_origin = '//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div[2]/div/div[1]/div/div[1]/a/text()'
    flight_destination = '//*[@id="__next"]/div/section/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div[2]/div/div[3]/div/div[1]/a/text()'

    r_t = requests.get(url_time).text
    s_t = etree.HTML(r_t)
    take_off = '//*[@id="content"]/div/div/main/div/div/section/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/h4/text()'
    landing = '//*[@id="content"]/div/div/main/div/div/section/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[1]/div/h4/text()'
    flight_time = '//*[@id="content"]/div/div/main/div/div/section/div[2]/div[1]/div[1]/div/div[2]/div[4]/div[2]/h4/text()'
    aircraft = '//*[@id="content"]/div/div/main/div/div/section/div[2]/div[1]/div[1]/div/div[2]/div[4]/div[1]/p[2]/text()'

    to = get_element(take_off, s_t)
    lg = get_element(landing, s_t)
    ft = get_element(flight_time, s_t)
    ac = get_element(aircraft, s_t)

    cd = get_element(flight_code, s)
    cp = get_element(flight_company, s)
    fo = get_element(flight_origin, s)
    fd = get_element(flight_destination, s)

    if (cd == None or cp == None or fo == None or fd == None):
        return
    else:
        try:
            cp = cd[:2]
            cd = cd[2:].strip()
            ac = ac.split(" ")
            acCompany = ac[0]
            acCraft = ac[1]

            if ft.find('h') + 1 == len(ft):
                ft = ft + '00'
            ft = ft.replace('h', ':')
            ft = ft.replace(' ', '')
            ft = ft.replace('m', '')

            if checkPlaneModel(acCraft) != True:
                addPlane(acCompany, acCraft)

            sqlquery = "INSERT INTO Flight (FlightNum, FlightCompany, Origin, Destination, TakeOffAt, ArriveAt, FlightTime, CraftCompany, Airplane) VALUES ('" + cd + "' , '" + cp + "' , '" + fo + "' , '" + fd + "' , '" + to + "' , '" + lg + "' , '" + ft + "' , '" + acCompany + "' , '" + acCraft + "')"
            print(sqlquery)
            cursor.execute(sqlquery)

            db.commit()

        except Exception as e:
            print(e)
            db.rollback()

        else:
            print(cp + cd + " added")




def get_element(xpath, s):
    for i in s.xpath(xpath):
        return i


def getFlights(flight, num):
    for i in range(num):
        getFlight(flight, i)


def checkPlaneModel(model):
    query = "SELECT * FROM `airline DB`.Airplane WHERE Model = '" + model + "'"
    cursor.execute(query)
    results = cursor.fetchall()

    for n in results:
        if len(n[1]) > 0:
            return True
        else:
            return False

def addPlane(company, model):
    query = "INSERT INTO `airline DB`.Airplane(Company, Model) VALUES('" + company + "' , '" + model + "')"
    cursor.execute(query)
    db.commit()


db = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='root',
    db='airline DB',
    charset='utf8',
    autocommit=True
)



cursor = db.cursor()

getFlights('UA', )



cursor.close()
db.close()
