# Assignment B
# Name: Ho Phuoc Anh Duc
# ID : 1534049
import requests
from bs4 import BeautifulSoup
import paho.mqtt.client as mqtt
import urllib.request as url
import time
import random

PM10 = None
PM25 = None
broker = "127.0.0.1"
port = 1883
trekking = ""


def get_info(client, url_link, url_key):
    global PM10
    global PM25
    global trekking
    main_content = requests.get(url_link)
    soup = BeautifulSoup(main_content.text, 'lxml')

    location = soup.find('div', class_="h1section").get_text()
    print(location)

    aqi = soup.find('div', class_="aqivalue").get_text()
    print(f'Air Quality: {aqi}')

    temp = soup.find('span', class_="temp").get_text()
    print(f'Temperature: {temp}')

    humidity = soup.find('td', id='cur_h', class_='tdcur').get_text()
    print(f'Humidity: {humidity}')

    tempval = soup.find('td', id="cur_t", class_="tdcur").get_text()
    if 0 < int(tempval) < 25 and 0 < int(aqi) < 70:
        trekking = "it's good for trekking and cycling"
        print(trekking)

    if soup.find('td', id="cur_pm10", class_="tdcur") is not None:
        PM10 = soup.find('td', id="cur_pm10", class_="tdcur").get_text()
        print(f'Current PM10: {PM10}')

    if soup.find('td', id="cur_pm26", class_="tdcur") is not None:
        PM25 = soup.find('td', id="cur_pm25", class_="tdcur").get_text()
        print(f'Current PM2.5: {PM25}')

    print(50 * "*")

    client.publish("duc1/2/", f'{location}\n'
                              f'Air Quality:   {aqi}\n'
                              f'Temperature:   {temp}\n'
                              f'Humidity:      {humidity}\n'
                              f'{trekking}\n'
                              f'Current PM10:  {PM10}\n'
                              f'Current PM2.5: {PM25}\n')

    url.urlopen(
        f"https://api.thingspeak.com/update?api_key={url_key}&field1={aqi}&field2={tempval}&field3={str(PM10)}&field4={humidity}")


def on_publish(client, userdata, result):
    print("data published")
    pass


while True:
    client1 = mqtt.Client("ctrl")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    # ret = client1.publish("duc1/2/", "hello")

    url_link_1 = "https://aqicn.org/city/new-zealand/nelson/tahunanui/nelson-at-blackwood-st/"
    url_key_1 = "U5B0TVGJN4U86N7A"
    get_info(client1, url_link_1, url_key_1)

    url_link_2 = "https://aqicn.org/city/new-zealand/marlborough/blenheim/blenheim-bowling-club/"
    url_key_2 = "MOVYB702Y5TYM95B"
    get_info(client1, url_link_2, url_key_2)

    url_link_3 = "https://aqicn.org/city/new-zealand/tasman/richmond/plunket-aq/"
    url_key_3 = "TIN7EN10BRULAT3W"
    get_info(client1, url_link_3, url_key_3)

    url_link_4 = "https://aqicn.org/city/new-zealand/wellington/willis-st/"
    url_key_4 = "F1V95PE2O4C1MPG2"
    get_info(client1, url_link_4, url_key_4)

    next_time = random.randint(300, 450)
    print(f'next package come in: {next_time} s')
    time.sleep(next_time)
