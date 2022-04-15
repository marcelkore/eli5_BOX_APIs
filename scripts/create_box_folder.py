import json
import os
import sys
from cmath import log
from typing import Dict, List

from loguru import logger

from box_utils import create_box_folder, get_authenticated_client, loguru

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

    logger.info("Authenticated client successfully")

except Exception as e:
    logger.error("Error in creating client object")
    logger.error(e)
    sys.exit(1)


def main() -> None:
    """This script will create a folder in box if it does not exists.

    These are folders that are required to stage files for both capture
    and report automation processes.

    This script will only be valid as long as the root folder contains
    less than 1000 folders (studies) which seems reasonable at this time.

    Args:
        folder_name (str): name of the folder to be created

    Returns:
        None

    python -m create_box_folder "<folder_name>"
    """

    # list object to hold input parameters
    args: List[str] = sys.argv

    # arguments - pass the folder name through the command line
    folder_name: str = args[1]

    # call box function to create folder in specified ROOT_FOLDER_ID

    create_box_folder(client, ROOT_FOLDER_ID, folder_name)


if __name__ == "__main__":
    main()
