import json
import os
import re
from difflib import SequenceMatcher
from glob import glob
from os.path import join, splitext, basename
from pprint import pprint
from time import sleep

import dateutil.parser as dparser
from google.auth import exceptions
from googleapiclient import errors
from googleapiclient.discovery import build

import constants
import utils

youtube = None
try:
    youtube = build(
        serviceName=constants.API_SERVICE_NAME,
        version=constants.API_VERSION,
        developerKey=constants.YOUTUBE_API_KEY
    )
except exceptions.DefaultCredentialsError:
    utils.cprint(constants.COLORS.BRIGHT_RED, "['API']['YOUTUBE_API_KEY'] needs to be set in config.ini \n "
                                              "https://docs.python.org/3.7/library/configparser.html#quick-start")
    exit(-1)
except errors.HttpError:
    utils.cprint(constants.COLORS.BRIGHT_RED,
                 "['API']['YOUTUBE_API_KEY'] in config.ini returned a Bad Request. This means it's invalid or you "
                 "have internet problems.")
    exit(-2)

for filepath in glob(join(constants.SCRAPING_FOLDER, "*.*")):
    filename = splitext(basename(filepath))[0]
    extension = splitext(basename(filepath))[1]

    print("Pocessing", '"' + filename + '"', "...")
    regexMatches = re.search(constants.REGEXES.VIDEO_ID, filename)
    if regexMatches[2]:
        video_title = regexMatches[1]
        video_id = regexMatches[2]
    else:
        video_title = filename
        video_id = ""

    utils.cprint(constants.COLORS.BRIGHT_BLUE, "Video title:", '"' + video_title + '"', "...")
    utils.cprint(constants.COLORS.BRIGHT_BLUE, "Video id:", '"' + video_id + '"', "...")

    hashed_video_title = re.sub(constants.REGEXES.ALPHANUM_FILTER, "", video_title).lower()

    try:
        search_response = youtube.search().list(
            q=(video_id if video_id else filename),
            type='video',
            part='id,snippet',
            maxResults=constants.MAX_RESULTS
        ).execute()
    except errors.HttpError as err:
        # utils.cprint(constants.COLORS.BRIGHT_RED, err.content.message)
        bob = json.decoder.JSONDecoder()
        utils.cprint(constants.COLORS.BRIGHT_RED, err)
        exit(-3)

    highest_score = 0
    highest_score_search_result_title = ""
    highest_score_search_result_date = ""
    highest_score_search_id = ""
    for search_result in search_response.get('items', []):
        # pprint(search_result)
        search_result_title = search_result['snippet']['title']
        search_result_id = search_result['id']['videoId']
        search_result_date = search_result['snippet']['publishedAt']
        utils.cprint(constants.COLORS.BRIGHT_YELLOW, "Scraped Video Title:", search_result_title)

        pprint(search_result_id)

        if search_result_id == video_id:
            print("Found video id match!")
            highest_score = 1.0
            highest_score_search_result_date = search_result_date
            break

        hashed_search_result_title = re.sub(constants.REGEXES.ALPHANUM_FILTER, "", search_result_title).lower()

        score = SequenceMatcher(None, hashed_video_title, hashed_search_result_title).ratio()

        if score > highest_score:
            highest_score = score
            highest_score_search_result_title = search_result_title
            highest_score_search_result_date = search_result_date
            highest_score_search_id = search_result['id']['videoId']

    if highest_score > 0:
        utils.cprint(constants.COLORS.BRIGHT_GREEN, "Closest scraped video title:", highest_score_search_result_title)
        print("Score:", highest_score)
        print("Video id:", highest_score_search_id)

        if highest_score < constants.AUTO_IGNORING_MAX_SCORE:
            utils.cprint(constants.COLORS.BRIGHT_CYAN, "Skipping video, cannot find good match")
        elif highest_score >= constants.AUTO_RENAMING_MIN_SCORE or utils.query_yes_no("Is this the correct video?"):
            course_date = dparser.parse(highest_score_search_result_date).strftime("%Y-%m-%d %H-%M-%S ")
            new_folder_name = os.path.join(constants.SCRAPING_FOLDER, course_date + filename + extension)
            print(new_folder_name)
            old_folder_name = os.path.join(constants.SCRAPING_FOLDER, filename + extension)
            os.rename(old_folder_name, new_folder_name)
    else:
        utils.cprint(constants.COLORS.BRIGHT_RED, "No video results could be scraped")

    print("---------------------------------------")
    sleep(constants.API_DELAY_BETWEEN_REQUESTS)
