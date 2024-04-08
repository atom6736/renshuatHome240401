import requests

from bs4 import BeautifulSoup

# inputArea = input("날씨를 조회하려는 지역을 입력하세요 :")

weatherHtml = requests.get("https://search.naver.com/search.naver?&query=한남동+날씨")
print(weatherHtml.text)

weatherSoup = BeautifulSoup(weatherHtml.text, 'html.parser')
print(weatherSoup)

areaText = weatherSoup.find("h2",{"class":"title"}).text
print(areaText)
areaText = areaText.strip()
# print(f"지역이름 : {areaText}")

todayTempText = weatherSoup.find("div", {"class":"temperature_text"}).text
print(todayTempText)
todayTempText = todayTempText.strip()
print(todayTempText)
todayTempText = todayTempText[5:12].strip()
print(todayTempText)
# print(f"현재온도 : {todayTempText}")

yesterdayTempText = weatherSoup.find("span",{"class":"temperature up"}).text
yesterdayTempText = yesterdayTempText.strip()
print(yesterdayTempText)
# print(f"어제날씨 비교 : {yesterdayTempText}")

todayweatherText = weatherSoup.find("span",{"class":"weather before_slash"}).text
todayweatherText = todayweatherText.strip()
print(todayweatherText)
# print(f"오늘날씨 :{todayweatherText}")

senseTempText = weatherSoup.find("dd", {"class":"desc"}).text
senseTempText = senseTempText.strip()
print(senseTempText)
# print(f"체감온도 : {senseTempText}")







