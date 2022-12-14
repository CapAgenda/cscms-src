from urllib import response
import feedparser
import requests
import os
import json
import string

allurls = 'https://comicstripblog.com/feed/?paged='

#Create empty list
comiclist = []

# Loop through pages of feeds and add to list the title and url for each comic
i=1
while (i<=3):
    payload = (allurls + str(i))
    fparsed = feedparser.parse(payload)
    for entry in fparsed.entries:
        comic = [entry.title, entry.media_content[1].get('url')]
        comiclist.append(comic)
      
    i=i+1
else:
    print("End of the loop")

#print list
""" print (comiclist) """

#Intialize JSON list
comic_json_list = []

#Set images directory
dir_path = 'public/images'

#function that downloads a file and saves it 
def download_image(location, file_name):
    #send GET request
    response = requests.get(location)
        
    #Write image file
    with open(os.path.join(dir_path, file_name), "wb") as f:
            f.write(response.content)

#function to clean the file name
def clean_file_name(fugly):
    fugly = fugly.translate(str.maketrans('','',string.punctuation))
    fugly = fugly.replace(" ","")
    fugly = fugly.replace("...","")
    cleaned = fugly.encode('ascii', errors='ignore').strip().decode('ascii')
    return cleaned

#function to clean the title
def clean_title_name(fugly_title):
    clean_title = fugly_title.encode('ascii', errors='ignore').strip().decode('ascii')
    return str(clean_title)

#download the files
for item in comiclist:
    location = item[1]
    filename_ugly = item[0]
    # determine and get filetype extension
    h = requests.head(location, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    extension = content_type.split('/')
    #clean title and file name characters
    file_name_title = clean_title_name(filename_ugly)
    file_name_clean = clean_file_name(filename_ugly) 
    #Add extension to file name
    file_name_ext = file_name_clean +'.'+ extension[1]
    # Create the JSON list
    json_list_item = {'Title':str(file_name_title), 'Ref':str('/images/')+str(file_name_ext)}
    comic_json_list.append(json_list_item)
    
    #Run download function  
    download_image(location, str(file_name_ext))

#Set json directory
json_path = 'src/components'    
# Save JSON list to repo
jsonString = json.dumps(comic_json_list,  indent=4)
jsonFile = open(os.path.join(json_path, "comics.json"), "w")
jsonFile.write(jsonString)
jsonFile.close()
