import os
import logging
import requests
from notion_client import Client
from notion_client import APIErrorCode, APIResponseError
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE_ID"]
print(f'Configured database: {database_id}')

def get_database_object(database_id=database_id):
    try:
        return notion.databases.query(database_id=database_id)
    except APIResponseError as error:
        if error.code == APIErrorCode.ObjectNotFound:
            logging.error("Database could not be found")
            raise error
        else:
            # Other error handling code
            logging.error(error)
            raise error

def get_image_from_entry(db_entry):
    file = db_entry['properties']['Icon']['files'][0]
    if file['type'] == 'external':
        url = file['external']['url']
    elif file['type'] == 'file':
        url = file['file']['url']
    try:
        return Image.open(requests.get(url, stream=True).raw)
    except Exception as e:
        # Log but continue
        logging.error(f'Encountered error while loading image {url}\n{e}')

def get_name_from_entry(db_entry):
    try:
        return db_entry['properties']['Name']['title'][0]['text']['content']
    except Exception as e:
        # Log but continue
        logging.error(f'Encountered error while getting Name {db_entry["properties"]}\n{e}')

def get_start_from_entry(db_entry):
    try:
        return db_entry['properties']['Start Time (24h)']['rich_text'][0]['text']['content']
    except Exception as e:
        # Log but continue
        logging.error(f'Encountered error while getting start time {db_entry["properties"]}\n{e}')

def get_entries():
    db_obj = get_database_object()
    return list(map(
        lambda entry : {
            "name" : get_name_from_entry(entry),
            "image" : get_image_from_entry(entry),
            "start" : get_start_from_entry(entry)
        }, db_obj['results']
    ))


if __name__ == "__main__":
    print(get_entries())
