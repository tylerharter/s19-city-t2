import urllib.request
from bs4 import BeautifulSoup
import re
import sys
from datetime import datetime

file = open(sys.argv[1],"w+");

fulltext = "Incident,Date,Incident Type,Address,Longitude,Latitude,Time,Response\n"


for i in range(0,147):

    x = urllib.request.urlopen("https://www.cityofmadison.com/fire/daily-reports?page="+str(i))
    html_doc = x.read().decode('utf-8')

    soup = BeautifulSoup(html_doc, 'html.parser')

    for br in soup.find_all("br"):
        br.replace_with(", ")

    times = []
    length = []
    longs = []
    lats = []

    text = ""
    for link in soup.find_all(class_ = "views-display")[2].find_all(class_="row"):
        if(":" in link.get_text()):
            text += link.get_text().strip()
        next_article = link.find("a")
        if next_article != None:
            next = next_article.get("href")
            print("    " + next)
            next_html = urllib.request.urlopen("https://www.cityofmadison.com"+next).read().decode('utf-8')

            next_soup = BeautifulSoup(next_html, 'html.parser')
            try:
                s1 = next_soup.find_all(property="dc:date")[0]["content"][11:19]
                s2 = next_soup.find_all(property="dc:date")[1]["content"][11:19]
                FMT = '%H:%M:%S'
                tdelta = str(datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT))
                length.append(tdelta)
            except IndexError:
                length.append("0")

            longs.append(next_html[next_html.find('"longitude":"')+13:].partition('"')[0])
            lats.append(next_html[next_html.find('"latitude":"')+12:].partition('"')[0])
        if(link.find(property="dc:date") != None):
            times.append(link.find(property="dc:date")["content"])
        text += "\n"

   # lines = (line.strip() for line in text.splitlines())
   # chunks = (phrase.strip() for line in lines for phrase in line.split(" "))

    text = text.strip()

    newtext = ""
    itemcount = 0
    for a in text.split("\n"):
        args = a.split(": ");
        args[1] = args[1].replace("\"","'").replace("“","'").strip()
        if args[0].strip() != "Updated":
            newtext += '"' + args[1] + '",'
        if args[0].strip() == "Address":
            newtext += '"' + longs[int(itemcount)] + '",'
            newtext += '"' + lats[int(itemcount)] + '",'
            newtext += '"' + times[int(itemcount)] + '",'
            newtext += '"' + length[int(itemcount)] + '"\n'
            itemcount+=1
    fulltext += newtext
    print ("Page " + str(i) + " downloaded...")
    file.write(fulltext)
    fulltext = ""

print("Download complete!")
