import os
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime
import shutil

home_folder = os.getenv('HOME')
saves_local_str = ".config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves/"
saves_cloud_str = "OurRimworldGame/saves"

saves_local = Path(os.path.join(home_folder, saves_local_str))
saves_cloud = Path(os.path.join(home_folder, saves_cloud_str))

def get_latest_modified_file(folder_path: Path) -> Tuple[Optional[Path], Optional[datetime]]:
    """
    https://stackoverflow.com/questions/237079/how-do-i-get-file-creation-and-modification-date-times
    Determines the latest modified file in the specified folder.

    Args:
        folder_path (Path): The path to the folder to search.

    Returns:
        Optional[Tuple[Path, datetime]]: A tuple containing the path of the latest modified file
        and its modification date, or None if the folder is empty or does not exist.
    """
    if not folder_path.exists():
        print(f"The folder {folder_path} does not exist.")
        return None, None

    latest_file = None
    latest_mod_time = None

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            mod_time = os.path.getmtime(file_path)
            mod_date = datetime.fromtimestamp(mod_time)

            if latest_mod_time is None or mod_date > latest_mod_time:
                latest_file = file_path
                latest_mod_time = mod_date

    if latest_file is None:
        print(f"The folder {folder_path} is empty.")
        return None, None

    return latest_file, latest_mod_time


file_local, date_local = get_latest_modified_file(saves_local)
file_cloud, date_cloud = get_latest_modified_file(saves_cloud)

# https://stackoverflow.com/questions/123198/how-to-copy-files
if not file_local or not file_cloud:
    print("Failure")
elif date_local == date_cloud:
	print("Saves up to date!")
elif date_local > date_cloud:
	print("Backing up local save to cloud...")
	shutil.copy2(file_local, saves_cloud)
else:
	print("Adding cloud save to locals...")
	shutil.copy2(file_cloud, saves_local)
