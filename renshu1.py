import sys
import threading

import requests
from bs4 import BeautifulSoup

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt  # 윈도우를 항상 화면에 뛰어두기 위해 필요한 요소 import

form_class = uic.loadUiType("ui/weatherUi_atHome.ui")[0]

class WeatherApp(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("날씨 검색 프로그램")
        self.setWindowIcon(QIcon('img/weather_icon.png'))
        self.statusBar().showMessage("WEATHER SEARCH APP VER1.0")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.weather_search()

        self.search_btn.clicked.connect(self.weather_search)
        self.search_btn.clicked.connect(self.reflashTimer)
        self.area_input.returnPressed.connect(self.weather_search)
        self.area_input.returnPressed.connect(self.reflashTimer)

    def weather_search(self):
        inputArea = self.area_input.text()

        weatherHtml = requests.get(f"https://search.naver.com/search.naver?where=nexearch&query={inputArea}날씨")
        # print(weatherHtml.text)

        weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')


        try:
        # 날씨지역
            areaText = weatherSoup.find("h2",{'class':'title'}).text
            areaText = areaText.strip()
            print(areaText)

            # 기온표시
            todayTempText = weatherSoup.find("div",{'class':'temperature_text'}).text
            todayTempText = todayTempText.strip()
            print(todayTempText)
            todayTempText = todayTempText[5:12].strip()
            print(todayTempText)

            # 어제와의 비교
            yesterdayTempText = weatherSoup.find('span',{'class':'temperature'}).text
            yesterdayTempText = yesterdayTempText.strip()
            print(yesterdayTempText)

            # 날씨
            todayWeatherText = weatherSoup.find('span', {'class':'weather before_slash'}).text
            todayWeatherText = todayWeatherText.strip()
            print(todayWeatherText)

            # 체감온도
            senseTempText = weatherSoup.find('dd', {'class':'desc'}).text
            senseTempText = senseTempText.strip()
            print(senseTempText)

            # 미세먼지
            todayInfoText = weatherSoup.select('ul.today_chart_list>li')
            dust1Info = todayInfoText[0].find('span',{'class':'txt'}).text
            dust1Info = dust1Info.strip()
            print(dust1Info)

            # 초미세먼지
            dust2Info = todayInfoText[1].find('span',{'class':'txt'}).text
            dust2Info.strip()
            print(dust2Info)

            # 크롤링한 날씨 정보 텍스트를 준비된 UI에 출력하기
            self.area_title.setText(areaText)
            self.setWeatherImage(todayWeatherText)
            self.now_temper.setText(todayTempText)
            self.yester_temper.setText(yesterdayTempText)
            self.sense_temper.setText(senseTempText)
            self.dust1_info.setText(dust1Info)
            self.dust2_info.setText(dust2Info)

        except:
            try:
                areaText = weatherSoup.find("h2", {'class': 'title'}).text
                areaText = areaText.strip()
                todayTempAllText = weatherSoup.find('div',{'class':'temperature_text'}).text
                todayTempAllText = todayTempAllText.strip()
                print(todayTempAllText)

                # todayTempText = todayTempAllText[6:9].strip()  # 해외 도시 현재 온도
                todayTempText = weatherSoup.select("div.temperature_text>strong")[0].text
                todayTempText = todayTempText[5:]
                # todayWeatherText = todayTempAllText[10:12].strip()  # 해외 도시 날씨 텍스트
                todayWeatherText = weatherSoup.select("div.temperature_text>p.summary")[0].text
                # todayWeatherText = todayWeatherText[:3].strip()
                self.setWeatherImage(todayWeatherText)  # 날씨 이미지 출력 함수 호출
                # senseTempText = todayTempAllText[18:].strip()  # 해외 도시 체감 온도
                senseTempText = weatherSoup.select("p.summary>span.text>em")[0].text

                self.area_title.setText(areaText)
                self.now_temper.setText(todayTempText)
                self.sense_temper.setText(senseTempText)

                self.yester_temper.setText("")  # 해외도시 어제와 날씨 비교 정보 없음 빈공간 출력
                self.dust1_info.setText("-")
                self.dust2_info.setText("-")

            except:
                self.area_title.setText("입력 지역명 오류!!")
                self.setWeatherImage("")  # 날씨 이미지 출력 함수 호출
                self.now_temper.setText("")
                self.yester_temper.setText(f"{inputArea} 지역은 존재하지 않습니다.")
                self.sense_temper.setText("-")
                self.dust1_info.setText("-")
                self.dust2_info.setText("-")

    def setWeatherImage(self, weatherText):
        if weatherText =='맑음':
            weatherImage = QPixmap('img/sun.png')
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText =='구름많음':
            weatherImage = QPixmap('img/cloud.png')
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif "화창" in weatherText:  # 화창이 포함된 날씨들은 모두 해 이미지가 출력
            weatherImage = QPixmap("img/sun.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText == "흐림":
            weatherImage = QPixmap("img/cloud.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif "흐림" in weatherText:  # 흐림이 포함된 날씨는 모두 구름 이미지가 출력
            weatherImage = QPixmap("img/cloud.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText == "비":
            weatherImage = QPixmap("img/rain.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText == "소나기":
            weatherImage = QPixmap("img/rain.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
        elif weatherText == "눈":
            weatherImage = QPixmap("img/snow.png")  # 이미지 불러와서 저장하기
            self.weather_img.setPixmap(QPixmap(weatherImage))
        else:
            self.weather_img.setText(weatherText)

    def reflashTimer(self):
        self.weather_search()
        threading.Timer(60, self.reflashTimer).start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = WeatherApp()
    win.show()
    sys.exit(app.exec_())


