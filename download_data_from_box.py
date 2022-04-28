import json
import os
import sys
from typing import Dict, List

from loguru import logger

from box_utils import download_file_from_box, get_authenticated_client, loguru

# initialize the logger
logger = loguru(logger)

script_name = os.path.basename(sys.argv[0])

logger.info(f"Starting {script_name} ")

# path to box config json file
pathToBoxConfigJson = (
    r"/Users/kore/Desktop/WORK/eli5_BOX_APIs/config/box_config.json"
)
# path to box sdk config json file
pathToBoxSdkConfigJson = (
    r"/Users/kore/Desktop/WORK/eli5_BOX_APIs/config/box_jwt_config.json"
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
    """download data from box.
    Args:
        folder_name: the name of the folder to upload the report to
        directory_path: the path to the directory contain the folder name
        file_format: the format of the file to upload i.e., csv or xlsx or xls or txt

    Output:
        None

    """

    # list object to hold input parameters
    args: List[str] = sys.argv

    # arguments - folder that will stored the data downloaded from box
    folder_name: str = args[1]

    # pass the directory path to the script
    directory_path: str = args[2]

    # pass the file format of files to be downloaded
    file_format: str = args[3]

    # add the folder name to the directory path
    directory_path = os.path.join(directory_path, folder_name)

    # check if directory does not exist

    # check if directory exists
    if not os.path.exists(directory_path):
        logger.info(f"{directory_path} does not exists")
        sys.exit(1)

    logger.info(f"{directory_path} exists")

    # get a list of all folders in the root folder
    folders: List[Dict] = client.folder(ROOT_FOLDER_ID).get_items(limit=1000)

    logger.info(f"folder id {ROOT_FOLDER_ID}")

    folder_id = ROOT_FOLDER_ID

    try:

        download_file_from_box(
            client=client,
            folder_id=folder_id,
            folder_name=folder_name,
            directory_path=directory_path,
            file_format=file_format,
        )

    except Exception as e:
        logger.error("Error downloading file from box")
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
