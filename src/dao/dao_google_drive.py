import pandas as pd
import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

DATA_DIR = "data/"
TEMP_DATA_DIR = DATA_DIR + "temp/"

def load_data(dataset_shareable_link, sep):
    google_drive_file_id = get_google_drive_file_id_from_shareable_link(dataset_shareable_link)
    data = load_csv_from_google_drive_file_id(google_drive_file_id, sep)
    return data

def get_google_drive_file_id_from_shareable_link(shareable_link):
    return shareable_link.split("google.com/file/d/")[1].split("/view")[0]

def remove_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)

def create_dir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

def load_csv_from_google_drive_file_id(google_drive_file_id, sep, dtype):
    csv_filepath = TEMP_DATA_DIR + '_temp.csv'
    create_dir(DATA_DIR)
    create_dir(TEMP_DATA_DIR)

    downloaded = drive.CreateFile({'id' : google_drive_file_id})
    downloaded.GetContentFile(csv_filepath)
    csv_file = pd.read_csv(csv_filepath, sep=sep, dtype=dtype)
    remove_file(csv_filepath)
    return csv_file


