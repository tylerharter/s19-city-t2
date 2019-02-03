import urllib.request
from bs4 import BeautifulSoup
import re
import sys




file = open(sys.argv[1],"w+");

fulltext = "Incident,Date,Incident Type,Address,Updated\n"


for i in range(100,101):

    x = urllib.request.urlopen("https://www.cityofmadison.com/fire/daily-reports?page="+str(i))
    html_doc = x.read().decode('utf-8')
    
    soup = BeautifulSoup(html_doc, 'html.parser')
    
    for br in soup.find_all("br"):
        br.replace_with(", ")

    text = ""
    for link in soup.find_all(class_ = "view-content")[2].find_all(class_="row"):
        text += link.get_text();

   # lines = (line.strip() for line in text.splitlines())
   # chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
    
    text = text.strip()
   
    newtext = ""
    itemcount = 1
    for a in text.split("\n"):
        for arg in a.split(":  "):
            arg = arg.strip()
            if arg != "Incident" and arg != "Date" and arg != "Updated" and arg != "Incident Type" and arg != "Address":
                arg  = arg.replace("\"","'").replace("“","'")
                if itemcount % 5 != 0:   
                    newtext += '"' + arg + '",'
                else:
                    newtext += '"' + arg + '"\n'
                itemcount += 1;
    newtext += '""\n'
    fulltext += newtext
    print ("Page " + str(i) + " downloaded...")

print("Download complete!")
print(fulltext)
file.write(fulltext)
