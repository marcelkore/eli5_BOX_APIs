## BOX Python APIs - eli5 Part 2
### Date: 2022-04-27
####  Description: This is the second part of a two part blog that reviews how to interact with BOX APIs.<br>

<br>

In part two of this series, we will be reviewing how to interact with the box app we created. This box app uses server-side [JWT Authentication](https://developer.box.com/guides/authentication/jwt/). One of the <br>
first main dependencies for this to work will be the boxsdk package. Install it using the option below. <br>

```
pip install "boxsdk[jwt]"
```

There are different way of setting this up depending on your needs. What I have here is a simple way to get started quickly and easily. <br>

I have a script with the following functions that I use to interact with the box app.

* get_authenticated_client
* create_box_folder
* download_file_from_box
* upload_file_to_box
* a logging function
* a send email function

### **Get Authenticated Client**


<pre>
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
        logger.info("Authenticating...")
        auth.authenticate_instance()
        return Client(auth)
</pre>

The configPath is the path to the JSON config file for your Box JWT app. This is the file that you downloaded from the box developer portal. <br>
It looks something like this


<pre>
    {
    "boxAppSettings": {
        "clientID": "redacted",
        "clientSecret": "redacted",
        "appAuth": {
        "publicKeyID": "8lqwmtf1",
        "privateKey": "-----BEGIN ENCRYPTED PRIVATE KEY----------END ENCRYPTED PRIVATE KEY-----\n",
        "passphrase": "redacted"
        }
    },
    "enterpriseID": "redacted"
    }
</pre>
Pass the path to this file to get an authenticated client.

### **Create Box Folder**

After getting an authenticated client, you have the keys to the city so to speak. One of my first use cases was to create a folder in box <br>
when none was present. I had a data pipeline that was run daily and the setup required a folder to be created for each run in box. We were <br>
using BOX for staging the files before moving them to the client final destination. <br>

For this to work, you have to identify the ID of the root folder you want to interact with. This is the ID of the folder that you want to create <br>
the folder in.

![Box Root Folder](https://koremarcelblog.blob.core.windows.net/box-blog/box-root-folder.png)

The box app/service account we reviewed in part one should be provided access to the folder as a pre-requisite. This is the box app that you <br>
created in part 1 of this blog.


<pre>
    def create_box_folder(
        client: str,
        root_folder_id: str,
        folder_name: str,
    ) -> None:
        """This function will create a folder in box if it is not present.

        Args:
            client:str - the authenticated client
            root_folder_id:str - the ID of the root folder you want to interact with
            folder_name:str -  name of the folder to be created in BOX

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
</pre>

### **Download File From Box**

The other natural requirement is how to download files from BOX. The funtion below will download a file from BOX. <br>

<pre>
    def download_file_from_box(
        client: str,
        folder_id: str,
        folder_name: str,
        directory_path: str,
        file_format: str,
    ) -> None:
        """This function will download a file from box.

        Can be modified to download a specific file from the folder.

        Args:
            client: the authenticated client
            folder_id: the id of the folder to download a file from
            folder_name: name of the box folder to download the file from
            directory_path: the path to the directory containing the file
            file_format: the format of the file to download

        Output:
            None

        Note:
            The script as is will download only files created on the same day as the script is run.
            This can be modified to download all files in the folder or any other download requirements.

        """

        logger.info("beginning download")

        # store the folder id
        folder = client.folder(folder_id=folder_id)

        # get a listing of all files in the folder
        items = folder.get_items()

        # add path to file to directory path
        filepath = os.path.join(directory_path, folder_name)

        try:
            logger.info("beginning download file script")
            for item in items:
                if item.name.endswith(file_format):
                    # get item date modified
                    file_info = client.file(item.id).get()

                    # get file modified date
                    file_modified_date = file_info["modified_at"]

                    # convert string to YYMMDD format
                    file_modified_date = pd.to_datetime(file_modified_date)

                    # get current date time
                    current_date_time = pd.Timestamp.now()

                    # convert string to YYMMDD format
                    current_date_time = pd.to_datetime(current_date_time)

                    # extract YYMMDD from file modified date
                    file_modified_date = file_modified_date.strftime("%y%m%d")
                    current_date_time = current_date_time.strftime("%y%m%d")

                    logger.info(f"file modified date: {file_modified_date}")
                    logger.info(f"current date time: {current_date_time}")

                    if current_date_time == file_modified_date:
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

</pre>


### **Upload File To Box**

The last function will be uploading a file to BOX. Again this uses the same pattern where you pass an authenticated client, folder id and directory path. <br>

<pre>
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

</pre>

This marks the end of this post. You can find the code for this script in the [GitHub repository]() and examples of how to use <br>
the script in your code.

Please feel free to leave any comments or suggestions.

Thanks!
