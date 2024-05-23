import logging
import os
import shutil
import ssl
import urllib.request
from ftplib import FTP
from io import BytesIO

import pandas as pd
import requests

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

server = os.getenv("FTP_SERVER")
username = os.getenv("FTP_USERNAME")
password = os.getenv("FTP_PASSWORD")

# Disable certificate verification
context = ssl._create_unverified_context()


def download_file(url, filename):
    with urllib.request.urlopen(url, context=context) as response:
        with open(filename, "wb") as f:
            shutil.copyfileobj(response, f)


def get_file(download_url):
    """
    Download an Excel file from a given URL and return it as a Pandas DataFrame.

    Parameters:
        download_url (str): The URL from which to download the file.

    Returns:
        pandas.DataFrame: The Excel file contents as a Pandas DataFrame.
    """
    filename = download_url.split("/")[-1]
    download_file(download_url, filename)
    df = pd.read_excel(filename)
    os.remove(filename)
    return df


def get_file_data(url):
    """Downloads an image from a URL and returns it as a BytesIO object.

    Args:
        url (str): The URL of the image to download.

    Returns:
        BytesIO: The data as a BytesIO object.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=30)
        # Check if the request was successful
        response.raise_for_status()
        # Return the content of the response (image data) as BytesIO object
        return BytesIO(response.content)
    except Exception as e:
        logging.error("An error occurred while downloading the file:", exc_info=True)
        return None


def upload_to_ftp(file_data, remote_directory, filename):
    """
    Uploads a file to an FTP server.

    Parameters:
        file_data (BytesIO): File data to be uploaded
        remote_directory (str): Directory on the FTP server to upload the file to
        filename (str): Name of the file to be uploaded

    Raises:
        ValueError: If any of the required parameters are not set
    """
    if not server or not username or not password:
        raise ValueError("Server, username, and password must be set to upload a file")

    with FTP(server) as ftp:
        ftp.login(username, password)
        ftp.cwd(remote_directory)
        with open(filename, "wb") as f:
            ftp.storbinary("STOR {}".format(filename), file_data)
        print(
            "Image uploaded successfully to '{}'/{}".format(remote_directory, filename)
        )


def list_ftp_files(ftp_server, ftp_username, ftp_password, remote_directory="/"):
    """
    Lists the files in a remote FTP directory.

    Parameters:
        ftp_server (str): The FTP server hostname or IP address.
        ftp_username (str): The username to use when connecting to the FTP server.
        ftp_password (str): The password to use when connecting to the FTP server.
        remote_directory (str, optional): The remote directory to list files in. Defaults to "/".
    """
    # Connect to the FTP server
    with FTP(ftp_server) as ftp:
        ftp.login(ftp_username, ftp_password)
        ftp.cwd(remote_directory)

        # Get list of files in the directory
        files = ftp.nlst()

        # Print the list of files
        print("Files in directory '{}':".format(remote_directory))

        for file in files:
            print(file)
