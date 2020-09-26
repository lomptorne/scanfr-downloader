import requests
import shutil
import sys
import os

from pathlib import Path, PureWindowsPath



def main():
    
    counter = 1
    path = os.getcwd()
    detrompino = 0 
    checker = False
    breaker = 0
    
    raw_url = str(input("Enter first page image URL: "))
    separator = raw_url.count("/")
    base_url = raw_url.rsplit("/", 1)[0]

    manga = raw_url.split("/", separator)[5]
    manga = manga.replace("-", " ").title()
    chapter = raw_url.split("/", separator)[7]

    raw_page = raw_url.rsplit("/", 1)[1]
    extension = "." + raw_page.split(".", 1)[1]
    numberino = raw_page.split(".", 1)[0]
    
    if "00" in str(numberino) : 
        detrompino = "00"
    if detrompino != 0 : 
        full_url = base_url + "/" + detrompino + str(counter) + extension
        checker = True
    else :
        detrompino = "0"
        full_url = base_url + "/" + detrompino + str(counter) + extension

    while(True): 

        full_url = base_url + "/" + detrompino + str(counter) + extension
        
        if counter >= 10 and checker == True :
            detrompino = "0"
            full_url = base_url + "/" + detrompino + str(counter) + extension
        if counter >= 10 and checker == False :
            detrompino = ""
            full_url = base_url + "/" + detrompino + str(counter) + extension
        if counter >= 100 and checker == True :
            detrompino = ""
            full_url = base_url + "/" + detrompino + str(counter) + extension

        r = requests.get(full_url, stream=True)

        if r.status_code == 200 :

            if counter == 1 : 
                dir_name = Path("{}/Mangas/{}/{}".format(path, manga, chapter))
            if os.name == 'nt':
                dir_name = PureWindowsPath(dir_name)
            try:
                os.makedirs(dir_name)
                os.chdir(dir_name)
            except OSError:
                os.chdir(dir_name)
            r.raw.decode_content = True
            with open("{}{}".format(str((counter - breaker)), extension),'wb') as f:
                print("Downloading Image : {}".format(str((counter - breaker))))
                shutil.copyfileobj(r.raw, f)

            counter += 1

        else:
            counter += 1
            breaker += 1
            if breaker >= 5 :
                print("Done !")
                break
    




if __name__ == "__main__" :
    main()