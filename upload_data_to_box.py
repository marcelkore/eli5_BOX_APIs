import json
import os
import sys
from typing import Dict, List

from box_utils import get_authenticated_client, upload_file_to_box
from loguru import logger

from helper_data import loguru

# initialize the logger
logger = loguru(logger)

script_name = os.path.basename(sys.argv[0])
# remove the file extension from the file name
script_name = os.path.splitext(script_name)[0]

logger.info(f"script begins")

# path to box config json file
pathToBoxConfigJson = (
    r"/Users/kore/Desktop/WORK/box_blog/config/box_config.json"
)
# path to box sdk config json file
pathToBoxSdkConfigJson = (
    r"/Users/kore/Desktop/WORK/box_blog/config/box_jwt_config.json"
)

# open the config file
with open(pathToBoxConfigJson, "r") as f:
    box_config = json.load(f)

# access json value
ROOT_FOLDER_ID = box_config["ROOT_FOLDER_ID"]

try:
    # get authenticated client
    client = get_authenticated_client(pathToBoxSdkConfigJson)

    logger.info("Received authenticated client successfully")

except Exception as e:
    logger.error("Error in creating client object")
    logger.error(e)
    sys.exit(1)


def main() -> None:
    """upload data to box.
    Args:
        folder_name: the name of the folder to upload the report to
        directory_path: the path to the directory containing the report
        file_format: the format of the file to upload i.e., csv or xlsx or xls or txt

    Output:
        None

    """

    # list object to hold input parameters
    args: List[str] = sys.argv

    # arguments - pass the folder name through the command line
    folder_name: str = args[1]

    # pass the directory path to the script
    directory_path: str = args[2]

    # pass the file format to be uploaded
    file_format: str = args[3]

    # add the folder name to the directory path
    directory_path = os.path.join(directory_path, folder_name)

    # check if directory does not exist

    # check if directory exists
    if not os.path.exists(directory_path):
        logger.info(f"{directory_path} does not exists")
        sys.exit(1)

    try:

        # get a list of all folders in the root folder
        folders: List[Dict] = client.folder(ROOT_FOLDER_ID).get_items(
            limit=1000
        )

        # check if the folder exists in the root folder
        for folder in folders:
            if folder["name"] == folder_name:
                # get the folder id
                folder_id: str = folder["id"]

        # check if expected file format exists
        if os.path.exists(directory_path):
            for file in os.listdir(directory_path):
                if file.endswith(f".{file_format}"):
                    pass
                else:
                    logger.error(f"File format .{format} does not exist")
                    sys.exit(1)

        # upload the file to box
        for file in os.listdir(directory_path):
            if file.endswith(f".{file_format}"):
                # if file ends with expected file format
                # we upload the file to box
                upload_file_to_box(
                    client=client,
                    folder_id=folder_id,
                    directory_path=directory_path,
                    filename=file,
                )

    except Exception as e:
        logger.error("Error uploading the file to box")
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
