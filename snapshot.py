import os
import requests
from xml.etree import ElementTree as etree

AP = "{http://www.w3.org/2005/Atom}" # Atom prefix

def process(id):
    path = "https://gdata.youtube.com/feeds/api/playlists/" + id
    response = requests.get(path)
    
    if response.text == "Playlist not found":
        sys.exit("Playlist not found")
    elif response.text == "User authentication required.":
        sys.exit("Playlist is private. API Auth to come!")
    
    # Parsing
    root = etree.fromstring(response.text)
    print("Processing playlist: " + root.find(AP+"title").text)
    
    cur_videos = {}
    for entry in root.findall(AP+"entry"):
        link  = entry.findall(AP+"link")[2].attrib['href'] # todo
        title = entry.find(AP+"title").text
        cur_videos[link] = title
    
    # CREATE/PARSE DATAFILE
    
    if not os.path.isfile("plists.xml"): # Datafile doesn't exist
        playlists = etree.Element("playlists")
    else:
        # PARSE DATAFILE
        playlists = etree.parse("plists.xml").getroot()
    
    # GET/CREATE PLAYLIST
    plist = playlists.find(id)
    if not plist: # Playlist not present
        plist = etree.SubElement(playlists, id)
        
        
    # CHECK FOR DELETED VIDEOS
    for video in plist:
        if video.attrib["link"] not in cur_videos:
            video.attrib["deleted"] = "true"
            print("DELETED: " + video.text)
    # ADD NEW VIDEOS
    for link,title in cur_videos.items():
        if not plist.find("video[@link='"+link+"']"): # video not already present       NOT WORKING - TODO
            print("HSH")
            etree.SubElement(plist, "video", attrib={"link":link, "deleted":"false"}).text = title
        
    # WRITE DATA TO FILE
    tree = etree.ElementTree(playlists)
    open("plists.xml", 'w').close()
    tree.write("plists.xml")
        
    
        
        
        
def main():
    print("Playlist ID: ",)
    #id = input()
    id = "PLeVHlcjtKzgSFDnvbqvuPJI8cW_xWZQd1"
    
    process(id)
    
main()