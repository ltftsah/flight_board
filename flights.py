from bs4 import BeautifulSoup as bs
from pyflightdata import FlightData
from datetime import datetime, timezone
import time


def flights():
    while True:
        f = FlightData()
        airport = "DUB"
        arrival_list = f.get_airport_arrivals(airport, 1, 10)
        departures_list = f.get_airport_departures(airport, 1, 38)

        doc = open("template.html")
        soup = bs(doc)

        #iterate through current arriving flights and save data to dict
        #and place in correct location in table
        x = 1
        for flights in arrival_list:
            arrival_dict = {}

            #save flight data to dict
            arrival_dict["flightNumber"] = flights["flight"]["identification"]["number"]["default"]
            airline = flights["flight"]["airline"]["name"]
            if len(airline) > 23:
                temp = airline[0:22]
                airline = "{0:<22}".format(temp)
            arrival_dict["airline"] = airline
            arrival_dict["terminal"] = flights["flight"]["airport"]["destination"]["info"]["terminal"]

            estArrivalTime = flights["flight"]["time"]["estimated"]["arrival"]
            if estArrivalTime != 'None':
                utc_time = datetime.fromtimestamp(int(estArrivalTime), timezone.utc)
                local_time = utc_time.astimezone()
                estArrivalTime = (local_time.strftime("%H:%M"))
            arrival_dict["estArrivalTime"] = estArrivalTime

            arrivalTime = flights["flight"]["time"]["scheduled"]["arrival"]
            utc_time = datetime.fromtimestamp(int(arrivalTime), timezone.utc)
            local_time = utc_time.astimezone()
            arrivalTime = (local_time.strftime("%H:%M"))
            arrival_dict["arrivalTime"] = arrivalTime

            origin = flights["flight"]["airport"]["origin"]["name"]
            if len(origin) > 35:
                temp = origin[0:34]
                origin = "{0:<34}".format(temp)
            arrival_dict["origin"] = origin

            #place flight data into table
            for tele in soup.find_all("td"):
                telep = tele.find_parent("tr")
                table = tele.find_parent("table")
                if table["id"] == "arrivals":
                    if telep["id"] == str(x):
                        tele.string = arrival_dict[tele["id"]]
            x += 1

        #iterate through current departing flights and save data to dict
        #and place in correct location in table
        x = 1
        for flights in departures_list:
            departure_dict = {}

            #save flight data to dict
            departure_dict["flightNumber"] = flights["flight"]["identification"]["number"]["default"]
            airline= flights["flight"]["airline"]["name"]
            if len(airline) > 23:
                temp = airline[0:22]
                airline = "{0:<22}".format(temp)
            departure_dict["airline"] = airline
            departure_dict["terminal"] = flights["flight"]["airport"]["origin"]["info"]["terminal"]

            estDepartureTime = flights["flight"]["time"]["estimated"]["departure"]
            if estDepartureTime != 'None':
                utc_time = datetime.fromtimestamp(int(estDepartureTime), timezone.utc)
                local_time = utc_time.astimezone()
                estDepartureTime = (local_time.strftime("%H:%M"))
            departure_dict["estDepartureTime"] = estDepartureTime

            departureTime = flights["flight"]["time"]["scheduled"]["departure"]
            utc_time = datetime.fromtimestamp(int(departureTime), timezone.utc)
            local_time = utc_time.astimezone()
            departureTime = (local_time.strftime("%H:%M"))
            departure_dict["departureTime"] = departureTime

            destination = flights["flight"]["airport"]["destination"]["name"]
            if len(destination) > 35:
                temp = destination[0:34]
                destination = "{0:<34}".format(temp)
            departure_dict["destination"] = destination

            #place flight data into table
            for tele in soup.find_all("td"):
                telep = tele.find_parent("tr")
                table = tele.find_parent("table")
                if table["id"] == "departures":
                    if telep["id"] == str(x):
                        tele.string = departure_dict[tele["id"]]
            x += 1

        #write changes to html file
        doc.close()
        html = soup.prettify("utf-8")
        with open("index.html", "wb") as file:
            file.write(html)

        time.sleep(180)

if __name__ == "__main__":
    flights()