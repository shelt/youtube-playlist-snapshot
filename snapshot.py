import os,sys
import requests
from xml.etree import ElementTree as etree

AP = "{http://www.w3.org/2005/Atom}" # Atom prefix

def snapshot(ID):
    path = "https://gdata.youtube.com/feeds/api/playlists/" + ID
    response = requests.get(path)
    
    if response.text == "Playlist not found":
        sys.exit("Error: Playlist not found")
    elif response.text == "User authentication required.":
        sys.exit("Error: Playlist is private. API Auth to come!")
    
    # GET CURRENT VIDEOS
    cur_videos = {}
    startindex = 1
    while True:
        response = requests.get(path + "?start-index=" + str(startindex))
        root = etree.fromstring(response.text)
        entries = root.findall(AP+"entry")
        if len(entries) == 0:
            break

        for entry in entries:
            id    = entry.find(AP+"id").text
            title = entry.find(AP+"title").text
            cur_videos[id] = title
        startindex += 25
        
    # CREATE/PARSE DATAFILE
    if not os.path.isfile("plists.xml"): # Datafile doesn't exist
        playlists = etree.Element("playlists")
    else:
        playlists = etree.parse("plists.xml").getroot()
    
    # GET/CREATE PLAYLIST
    plist = playlists.find(ID)
    if plist == None: # Playlist not present
        plist = etree.SubElement(playlists, ID)
        
    # CHECK FOR DELETED VIDEOS
    for video in plist:
        if video.attrib["id"] not in cur_videos:
            video.attrib["deleted"] = "true"
            print("DELETED: " + video.text)
    # ADD NEW VIDEOS
    for id,title in cur_videos.items():
        if plist.find("video[@id='"+id+"']") == None: # video not already present
            etree.SubElement(plist, "video", attrib={"id":id, "deleted":"false"}).text = title
        
    # WRITE DATA TO FILE
    tree = etree.ElementTree(playlists)
    open("plists.xml", 'w').close()
    tree.write("plists.xml")
        
    
        
        
        
def main():
    ids = input("Playlist ID(s): ")
    if ids == "":
        try:
            for plist in etree.parse("plists.xml").getroot().getchildren():
                snapshot(plist.tag)
                
        except TodoError:
            sys.exit("Error: No playlist IDs entered and no history found.")
            
    else:
        for id in ids.split():
            snapshot(id)
    print("Completed.")
    
main()