# KeyboardCombination 2022

from argparse import ArgumentParser
from xml.etree.ElementTree import parse
from base64 import b64decode
from hashlib import md5
from os import path, mkdir
from time import sleep

#Functions:
def ExtractAssets(x, dir):
    Decoded = b64decode(x.text)
    FileHash = md5(Decoded).hexdigest()
    FileType = ""

    print(f"Extracting {FileHash}...")

    isPng = True if Decoded[1:4] == b'PNG' else False
    isBmp = True if Decoded[0:2] == b'BM' else False
    isJpg = True if Decoded[6:10] == b'JFIF' else False
    isWav = True if Decoded[0:4] == b'RIFF' else False
    isMp3 = True if Decoded[0:3] == b'ID3' else False
    isMid = True if Decoded[0:4] == b'MThd' else False
    
    if isPng:
        FileType = ".png"
    if isBmp:
        FileType = ".bmp"   
    if isJpg:
        FileType = ".jpg"  
    if isWav:
        FileType = ".wav"
    if isMp3:
        FileType = ".mp3"
    if isMid:
        FileType = ".mid" 

    #Write to file:
    with open(f"{dir}/{FileHash}{FileType}", "wb") as f:
        f.write(Decoded)

    print(f"Saved succesfully as {FileHash}{FileType}")

#Parse arguments:
parser = ArgumentParser()
parser.add_argument("file_path")
p = parser.parse_args()

#Open file:
place_file = open(p.file_path, "r")

#Open XML:
try:
    xmlTree = parse(place_file)
except:
    input("Invalid place file!")
    exit()

root = xmlTree.getroot()

#Find every tag of <binary>:
content_elements = root.findall(".//binary")

#Make folder:
if not path.exists("Decoded"):
    #os.mkdir("Decoded")
    mkdir(path.basename(p.file_path) + "_Decoded")
else:
    input("Decoded folder already exists!")

#Go through every tag and save to file:
for x in content_elements:
    ExtractAssets(x, path.basename(p.file_path) + "_Decoded")

print("\nAll assets extracted succesfully, this window will close in 2 seconds.")
sleep(2)