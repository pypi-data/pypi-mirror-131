import requests
import os
import re
import asyncio

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_path_and_filename(full_path):
    path = "/".join(full_path.split("/")[:-1])
    filename = full_path.split("/")[-1]
    return path,filename

class Authoring():
    """
    Class for handling the process of creating files and establishing the autosaving process
    """
    def __init__(self,server_url):
        self.server_url = server_url
        # To be assigned when authentication is done
        self.source_folder = None
        self.release_folder = None
        self.alias = None
        self.token = None
        self.file_records = {}
        self.assignment = None
        self.headers = {}

    def auth(self, access_token):

        headers = {'Authorization' : f'Bearer {access_token}'}

        response = requests.get(self.server_url + "/API/auth", headers=headers)

        if response.status_code == 200:
            self.headers = headers
            self.token   = access_token
            self.assignment = response.json()
            self.alias = self.assignment["a_alias"]

            self.source_folder = os.getcwd() + "/source/" + self.alias
            self.release_folder = os.getcwd() + "/release/" + self.alias

            # Create these folders if does not exit:
            if not os.path.exists(self.source_folder):
                os.makedirs(self.source_folder)
            if not os.path.exists(self.release_folder):
                os.makedirs(self.release_folder)

            print("Assignment Loaded:",self.assignment["a_name"])
        else:
            print(response.content)
            raise Exception(response.content)


    def get_files(self):
        response = requests.get(self.server_url + "/API/list_files", headers=self.headers)

        if response.status_code == 200:
            files = response.json()
            for file in files:
                if file["private"]:
                    folder = self.source_folder
                else:
                    folder = self.release_folder

                self.download_file(file["file"], folder)
        else:
            print(response.content)
            raise Exception(response.content)


    def download_file(self, file_id, location, filename=False):

        # Make sure that the folder is available
        if not os.path.exists(location):
            os.makedirs(location)

        response = requests.get(self.server_url + "/API/get_file/"+str(file_id), headers=self.headers)

        if response.status_code == 200:
            if not filename:
                # Find the filename from the headers
                d = response.headers['content-disposition']
                filename = re.findall("filename=(.+)", d)[0]

            open(location + "/" + filename, 'wb').write(response.content)
            self.file_records[location + "/" + filename] = file_id
        else:
            print(response.content)
            #raise Exception(response.content)

    def autosave(self):
        global observer

        event_handler_source = AutoSaveEventHandler(self,self.source_folder,private=1)
        event_handler_release = AutoSaveEventHandler(self, self.release_folder, private=0)
        observer = Observer()

        observer.schedule(event_handler_source, self.source_folder, recursive=True)
        observer.schedule(event_handler_release, self.release_folder, recursive=True)
        observer.start()

        loop = asyncio.get_event_loop()
        loop.create_task(self.async_autosaving())


    async def async_autosaving(self):
        global observer
        await asyncio.sleep(1)
        minutes = 0
        while True:
            await asyncio.sleep(60);
            minutes += 1
            if minutes % 10 == 0:
                print(" ", sep="", end="")


    def show_links(self):
        try:
            from IPython.display import display, Javascript, HTML, IFrame
        except ImportError:
            print("Unable to load IPython")
            return False

        display(HTML(f"""<a id="btn_source_folder" target="_blank" href="../tree/source/{self.alias}" class="btn">Open Assignment Folder</a><br>
        <a id="btn_source_folder" target="_blank" href="../tree/release/{self.alias}" class="btn">Open Student´s version Folder</a><br>
        <a id="btn_nbgrader target="_blank" href="../formgrader" class="btn">Open nbgrader</a>"""))


    def upload_file(self, file, directory, private=1):
        """Uploads new file to the nbpickup server"""
        # Skip files starting the name with dot
        if file[0] == "."  or "-checkpoint" in file[0]:
            return False
        files = {"file": open(directory+"/"+file, "rb")}
        values = {"filename":file,
                  "path":directory,
                  "assignment":self.assignment["a_id"],
                  "private":private,
                  }
        response = requests.post(self.server_url + "/API/upload_file", files=files, data=values, headers=self.headers)
        if response.status_code == 200:
            file_id = response.content
            self.file_records[directory + "/" + file] = file_id

        else:
            print(response.status_code,response.content)

    def update_file(self, file, directory):
        """Updates existing file on the nbpickup server"""
        # Skip files starting the name with dot
        if file[0] == "." or "-checkpoint" in file[0]:
            return False
        files = {"file": open(directory + "/" + file, "rb")}
        values = {"filename": file,
                  "path": directory}

        # Check if the file is already in our know directory
        if directory + "/" + file not in self.file_records:
            return self.upload_file(file,directory)

        file_id = self.file_records[directory + "/" + file]
        response = requests.post(self.server_url + f"/API/update_file/{file_id}", files=files, data=values, headers=self.headers)
        if response.status_code == 200:
            pass # Nice, updated

        else:
            print(response.status_code,response.content)

    def move_file(self, old_location, new_location):
        """Function to handle file movements. Mainly for bookkeeping purposes."""
        directory, filename = get_path_and_filename(new_location)
        if old_location not in self.file_records:
            return self.upload_file(filename,directory)
        else:
            self.file_records[new_location] = self.file_records[old_location]
            return self.update_file(filename, directory)


class AutoSaveEventHandler(FileSystemEventHandler):
    """Captures and deals with autosaving of nbpickup files"""

    def __init__(self, nbpickup, folder, private = 1):
        super().__init__()

        self.nbpickup = nbpickup
        self.private = private
        self.folder = folder

    def on_moved(self, event):
        """Handles both rename and move events"""
        super().on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        print("Moved %s: from %s to %s", what, event.src_path,
                         event.dest_path)
        if not event.is_directory:
            self.nbpickup.move_file(what,event.dest_path)


    def on_created(self, event):
        super().on_created(event)

        what = 'directory' if event.is_directory else 'file'

        print("Created %s: %s", what, event.src_path)
        if not event.is_directory:
            path = "/".join(event.src_path.split("/")[:-1])
            filename = event.src_path.split("/")[-1]
            self.nbpickup.upload_file(filename, path, self.private)

    def on_deleted(self, event):
        super().on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        print("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        super().on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        print("Modified %s: %s", what, event.src_path)
        if not event.is_directory:
            path = "/".join(event.src_path.split("/")[:-1])
            filename = event.src_path.split("/")[-1]
            self.nbpickup.update_file(filename,path)