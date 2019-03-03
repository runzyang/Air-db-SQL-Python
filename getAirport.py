import requests
import re
from lxml import etree
import pymysql


def get_element(xpath, s):
    for i in s.xpath(xpath):
        return i.text

def get_airport(code, n):

    url = 'https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_'+code
    r = requests.get(url).text
    s = etree.HTML(r)
    n = str(n)

    airport_code = '//*[@id="mw-content-text"]/div/table/tbody/tr[' + n + ']/td[1]'

    airport_name = '//*[@id="mw-content-text"]/div/table/tbody/tr['+ n +']/td[3]/a'
    airport_name_nolink = '//*[@id="mw-content-text"]/div/table/tbody/tr['+n+']/td[3]/text()'

    airport_location = '//*[@id="mw-content-text"]/div/table/tbody/tr['+ n +']/td[4]/a[1]'

    airport_state = '//*[@id="mw-content-text"]/div/table/tbody/tr['+ n +']/td[4]/a[2]'
    airport_state_nolink = '//*[@id="mw-content-text"]/div/table/tbody/tr['+n+']/td[4]/text()'

    airport_country_linked = '//*[@id="mw-content-text"]/div/table/tbody/tr['+n+']/td[4]/a[3]'
    airport_country_nolink = '//*[@id="mw-content-text"]/div/table/tbody/tr['+ n +']/td[4]/text()[2]'

    airport_location_onepart = '//*[@id="mw-content-text"]/div/table/tbody/tr['+n+']/td[4]/a'

    print(get_element(airport_code, s))
    try:
        st = s.xpath(airport_state_nolink)[0].replace("'","")
        st = st.replace(", ","")
        st = st.replace("(","")
        st = st.replace(")","")
        st = st.replace(" ","")
        if re.search('[a-zA-Z]', st) == None:
            st = None
    except IndexError:
        st = None

    try:
        i = s.xpath(airport_country_nolink)[0].replace("'","")
        i = i.replace(", ","")
        i = i.replace("(","")
        i = i.replace(")","")
        i = i.replace(" ","")
        if re.search('[a-zA-Z]', i) == None:
            i = None
    except IndexError:
        i = None

    try:
        na = s.xpath(airport_name_nolink)[0].replace("'","")
        na = na.replace(", ","")
        na = na.replace("(","")
        na = na.replace(")","")
        if re.search('[a-zA-Z]', na) == None:
            na = None
    except IndexError:
        na = None


    if get_element(airport_code, s) == None:
        return


    else:


        Acode = get_element(airport_code, s)
        if (get_element(airport_name, s) == None):
            Aname = na
        else:
            Aname = get_element(airport_name, s)

        Acity = get_element(airport_location, s)


        if (i == None and get_element(airport_country_linked, s) == None and get_element(airport_state,s) == None and st == None and get_element(airport_location_onepart, s) == None):
            return
        elif (get_element(airport_location_onepart, s) != None):
            Acity = get_element(airport_location_onepart, s)
            Acountry = get_element(airport_location_onepart, s)

        else:
            if (i == None and get_element(airport_country_linked, s) == None):
                Acountry = get_element(airport_state,s)
                if get_element(airport_state,s) == None:
                    Acountry = st

            elif i == None or i == '':
                Acountry = get_element(airport_country_linked, s)

            elif get_element(airport_country_linked, s) == None:
                Acountry = i


        try:
            sqlquery = "INSERT INTO Airport (Name, Code, City, Country) VALUES ('" + Aname + "' , '" + Acode + "' , '" + Acity + "' , '" + Acountry + "')"
            cursor.execute(sqlquery)

            db.commit()
            print(Aname + "--" + Acode + "--" + Acity + "--" + Acountry)
        except Exception as e:
            print(e)

            return





        #print(get_element(airport_country_linked, s), i, get_element(airport_code, s), get_element(airport_state, s), get_element(airport_location, s), get_element(airport_name, s))




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

for i in [chr(x) for x in range(ord('a'), ord('z')+1)]:
    for b in range(750):
        get_airport(i.upper(), b)


#for b in range(700):

    #get_airport('', b)

#get_airport('Q', 11)

cursor.close()
db.close()

#'//*[@id="mw-content-text"]/div/table/tbody/tr[170]/td[3]/a'+'BGP'
