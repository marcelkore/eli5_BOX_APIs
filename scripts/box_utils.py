import json
import os
import os.path
import smtplib
import sys
from typing import Dict, List

import keyring
import pandas as pd
from boxsdk import Client, JWTAuth
from boxsdk.object.folder import Folder
from loguru import logger


def get_authenticated_client(configPath):
    """Get an authenticated Box client for a JWT service account

    Arguments:
        configPath {str} -- Path to the JSON config file for your Box JWT app

    Returns:
        Client -- A Box client for the JWT service account

    Raises:
        ValueError -- if the configPath is empty or cannot be found.
    """
    if os.path.isfile(configPath) == False:
        raise ValueError(
            f"configPath must be a path to the JSON config file for your Box JWT app"
        )
    auth = JWTAuth.from_settings_file(configPath)
    print("Authenticating...")
    auth.authenticate_instance()
    return Client(auth)


def create_box_folder(
    client: str,
    root_folder_id: str,
    folder_name: str,
) -> None:
    """This function will create a folder in box.

    Args:
         client: the authenticated client
         folder_name: name of the folder to be created

     Output:
         None

    """

    try:
        # get a list of all folders in the root folder
        folders: List[Dict] = client.folder(root_folder_id).get_items(
            limit=1000
        )

        # check if the folder exists in the root folder
        for folder in folders:
            if folder["name"] == folder_name:
                logger.info("Folder already exists in root folder..exiting")
                sys.exit(0)
        else:
            # create the folder in the root folder
            sub_folder = client.folder(root_folder_id).create_subfolder(
                folder_name
            )
            logger.info("Folder created successfully")
            print(f"Folder created successfully: {sub_folder['id']}")
            sys.exit(0)
    except Exception as e:
        logger.error(f"Error in downloading {folder_name} to box")
        logger.error(e)
        sys.exit(1)


def download_file_from_box(
    client: str,
    folder_id: str,
    folder_name: str,
    directory_path: str,
    file_format: str,
) -> None:
    """This function will download a file from box.

    You pass a folder name and a file format to this function
    and it will download all files in the folder with that file format.

    Can be modified to download a specific file from the folder.

    Args:
         client: the authenticated client
         folder_id: the id of the folder to upload the file to in box
         folder_name: name of the folder to upload
         directory_path: the path to the directory containing the file
         file_format: the format of the file to download

     Output:
         None

    """

    # store the folder id
    folder = client.folder(folder_id=folder_id)

    # get a listing of all files in the folder
    items = folder.get_items()

    # add path to file to directory path
    filepath = os.path.join(directory_path)

    try:
        logger.info("beginning download file script")
        for item in items:
            if item.name.endswith(file_format):

                # add item.id to directory path
                download_path = os.path.join(filepath, item.name)

                with open(download_path, "wb") as f:
                    client.file(item.id).download_to(f)
                    f.close()

            logger.info(f"File {item.name} has been downloaded")
    except Exception as e:
        logger.error(f"Error in downloading {folder_name} to box")
        logger.error(e)
        sys.exit(1)

    return None


def upload_file_to_box(
    client: str, folder_id: str, filename: str, directory_path: str
) -> None:
    """This function will upload a file to box.

    If the file already exists in the folder, it will upload a new version of the file.

    Args:
        client: the authenticated client
        folder_id: the id of the folder to upload the file to in box
        filename: name of the file to upload
        directory_path: the path to the directory containing the file

    Output:
        None

    """

    # store the folder id
    folder = client.folder(folder_id=folder_id)

    # get a listing of all files in the folder
    items = folder.get_items()

    # add path to file to directory path
    filepath = os.path.join(directory_path, filename)

    try:
        logger.info("beginning upload")
        for item in items:
            if item.name == filename:
                updated_file = client.file(item.id).update_contents(filepath)
                logger.info(f"File {filename} has been updated")
                return

        # if file is not present, then upload the file
        client.folder(folder_id=folder_id).upload(filepath)
        logger.info(f"File {filename} has been uploaded")
    except Exception as e:
        logger.error(f"Error in uploading {filename} to box")
        logger.error(e)
        sys.exit(1)

    return None


def loguru(logger) -> None:

    """This is the logging function.Call this script to log
    each script on the run folder and the log file will be
    created in the same folder.

    Returns:
        _type_: _description_
    """

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # get the current file name
    script_name = os.path.basename(sys.argv[0])
    # remove the file extension from the file name
    script_name = os.path.splitext(script_name)[0]

    fh = script_name + ".log"

    # add file handler
    logger.add(fh)

    logger.add(
        sys.stderr,
        level="INFO",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    )

    # add a file handler

    return logger


@logger.catch
def send_email(subject, recipients, text):
    """This function sends an email to the recipients.

    Args:
        subject (_type_): _description_
        recipients (_type_): _description_
        text (_type_): _description_

    Returns:
        None
    """

    # hard coded email credentials
    # NOTE: Move them to keyring or a config file
    USERNAME = "<ENTER USERNAME>"
    PASSWORD = keyring.get_password("email", "password")
    HOST = "email-smtp.us-east-1.amazonaws.com"
    FROM = "<ENTER FROM EMAIL>"

    BODY = "\r\n".join(
        (
            f"From: {FROM}",
            f"To: {recipients}",
            f"Subject: {subject}",
            "",
            f"{text}",
        )
    )

    try:
        server = smtplib.SMTP(HOST, 587)
        # start SSL for security

        # set context to use SSL
        context = ssl.create_default_context()

        server.starttls(context=context)  # secure the connection with TLS

        # pass credentials
        server.login(USERNAME, PASSWORD)
        server.sendmail(FROM, [recipients], BODY)
        server.quit()
        logger.info("Success: Email sent!")
    except Exception as e:
        logger.error(e)
        sys.exit(1)
