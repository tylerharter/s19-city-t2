import urllib.request
from bs4 import BeautifulSoup
import re
import sys

file = open(sys.argv[1],"w+");

fulltext = "Incident,Date,Incident Type,Address,Time\n"


for i in range(0,145):

    x = urllib.request.urlopen("https://www.cityofmadison.com/fire/daily-reports?page="+str(i))
    html_doc = x.read().decode('utf-8')
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    for br in soup.find_all("br"):
        br.replace_with(", ")

    times = []

    text = ""
    for link in soup.find_all(class_ = "views-display")[2].find_all(class_="row"):
        if(":" in link.get_text()):
            text += link.get_text().strip()
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
            newtext += '"' + times[int(itemcount)] + '"\n'
            itemcount+=1
    fulltext += newtext
    print ("Page " + str(i) + " downloaded...")

print("Download complete!")
file.write(fulltext)
