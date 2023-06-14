import requests
import pandas as pd
import os

username = input("Enter your username: ")

ar = requests.get("http://myanimelist.net/animelist/" + username + "/load.json?offset=0&status=7")
anime_request = ar.json()

mr = requests.get("http://myanimelist.net/mangalist/" + username + "/load.json?offset=0&status=7")
manga_request = mr.json()

anime_template = "ID;Name;English Name;Score;Status;Type;Release;Watched Episodes;All Episodes;URL\n"
csv_anime = "anime_export.csv"
anime_file = open(csv_anime, "a")
anime_file.write(anime_template)

manga_template = "ID;Name;English Name;Score;Status;Type;Release;Read Chapters;Read Volumes;All Chapters;All Volumes;URL\n"
csv_manga = "manga_export.csv"
manga_file = open(csv_manga, "a")
manga_file.write(manga_template)

template = "ID;Name;English Name;Score;Status;Type;Release;URL" + "\n"
csv = "export.csv"
file = open(csv, "a")
file.write(template)


for i in anime_request:
    anime_status = i["status"]
    if anime_status == 2:
        anime_status = "Completed"
    elif anime_status == 3:
        anime_status = "On Hold"
    anime_id = i["anime_id"]
    anime_name = i["anime_title"]
    anime_eng_name = i["anime_title_eng"]
    if anime_eng_name == "":
        anime_eng_name = "?"
    anime_score = i["anime_score_val"]
    if anime_score == 0:
        anime_score = "?"
    episodes = i["num_watched_episodes"]
    total_episodes = i["anime_num_episodes"]
    if total_episodes == 0:
        total_episodes = "?"
    anime_type = i["anime_media_type_string"]
    anime_release = i["anime_start_date_string"]
    anime_url = "https://myanimelist.net/anime/" + str(anime_id) + "/"
    
    csv_list = [str(anime_id), anime_name, anime_eng_name, str(anime_score), anime_status, anime_type, str(anime_release), anime_url + "\n"]
    string = ";".join(csv_list)
    file.write(string)
    anime_list = [str(anime_id), anime_name, anime_eng_name, str(anime_score), anime_status, anime_type, str(anime_release), str(episodes), str(total_episodes), anime_url + "\n"]
    anime_string = ";".join(anime_list)
    anime_file.write(anime_string)


for i in manga_request:
    manga_status = i["status"]
    if manga_status == 2:
        manga_status = "Completed"
    elif manga_status == 3:
        manga_status = "On Hold"
    manga_id = i["manga_id"]
    manga_name = i["manga_title"]
    manga_eng_name = i["manga_english"]
    if manga_eng_name == "":
        manga_eng_name = "?"
    manga_score = i["manga_score_val"]
    if manga_score == 0:
        manga_score = "?"
    chapters = i["num_read_chapters"]
    volumes = i["num_read_volumes"]
    total_chapters = i["manga_num_chapters"]
    if total_chapters == 0:
        total_chapters = "?"
    total_volumes = i["manga_num_volumes"]
    if total_volumes == 0:
        total_volumes = "?"
    manga_type = i["manga_media_type_string"]
    manga_release = i["manga_start_date_string"]
    manga_url = "https://myanimelist.net/manga/" + str(manga_id) + "/"
    
    csv_list = [str(manga_id), manga_name, manga_eng_name, str(manga_score), manga_status, manga_type, str(manga_release), manga_url + "\n"]
    string = ";".join(csv_list)
    file.write(string)
    manga_list = [str(manga_id), manga_name, manga_eng_name, str(manga_score), manga_status, manga_type, str(manga_release), str(chapters), str(volumes), str(total_chapters), str(total_volumes), manga_url + "\n"]
    manga_string = ";".join(manga_list)
    manga_file.write(manga_string)


file.close()
anime_file.close()
manga_file.close()

anime_read = pd.read_csv(csv_anime, delimiter=";", decimal=".")
manga_read = pd.read_csv(csv_manga, delimiter=";", decimal=".")
read = pd.read_csv(csv, delimiter=";", decimal=".")
resultExcelFile = pd.ExcelWriter("export.xlsx")
anime_read.to_excel(resultExcelFile, index=False, sheet_name="anime")
manga_read.to_excel(resultExcelFile, index=False, sheet_name="manga")
read.to_excel(resultExcelFile, index=False, sheet_name="merge")
resultExcelFile.close()

os.remove(csv_anime)
os.remove(csv_manga)
os.remove(csv)
