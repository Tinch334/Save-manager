import constants as c

import PySimpleGUI as sg
import os
import yaml
import shutil

from yaml.loader import SafeLoader
from dataclasses import dataclass
from typing import List, Dict, Any, TypeVar


#Generic type for type hints.
T = TypeVar("T")


#Set colour theme and text justification.
sg.theme('GreenTan')
sg.set_options(text_justification='left')  


class SaveManager:
    def __init__(self):
        self.config = None
        self.layout2 = [[sg.Text('Machine Learning Command Line Parameters', font=('Helvetica', 16))],      
                        [sg.Text('Passes', size=(15, 1)), sg.Spin(values=[i for i in range(1, 1000)], initial_value=20, size=(6, 1)),      
                         sg.Text('Steps', size=(18, 1)), sg.Spin(values=[i for i in range(1, 1000)], initial_value=20, size=(6, 1))],      
                        [sg.Text('ooa', size=(15, 1)), sg.In(default_text='6', size=(10, 1)), sg.Text('nn', size=(15, 1)),      
                         sg.In(default_text='10', size=(10, 1))],      
                        [sg.Text('q', size=(15, 1)), sg.Input(default_text='ff', size=(10, 1)), sg.Text('ngram', size=(15, 1)),      
                         sg.In(default_text='5', size=(10, 1))],      
                        [sg.Text('l', size=(15, 1)), sg.In(default_text='0.4', size=(10, 1)), sg.Text('Layers', size=(15, 1)),      
                         sg.Drop(values=('BatchNorm', 'other'), auto_size_text=True)],      
                        [sg.Text('_'  * 100, size=(65, 1))],      
                        [sg.Text('Flags', font=('Helvetica', 15), justification='left')],      
                        [sg.Checkbox('Normalize', size=(12, 1), default=True), sg.Checkbox('Verbose', size=(20, 1))],      
                        [sg.Checkbox('Cluster', size=(12, 1)), sg.Checkbox('Flush Output', size=(20, 1), default=True)],      
                        [sg.Checkbox('Write Results', size=(12, 1)), sg.Checkbox('Keep Intermediate Data', size=(20, 1))],      
                        [sg.Text('_'  * 100, size=(65, 1))],      
                        [sg.Text('Loss Functions', font=('Helvetica', 15), justification='left')],      
                        [sg.Radio('Cross-Entropy', 'loss', size=(12, 1)), sg.Radio('Logistic', 'loss', default=True, size=(12, 1))],      
                        [sg.Radio('Hinge', 'loss', size=(12, 1)), sg.Radio('Huber', 'loss', size=(12, 1))],      
                        [sg.Radio('Kullerback', 'loss', size=(12, 1)), sg.Radio('MAE(L1)', 'loss', size=(12, 1))],      
                        [sg.Radio('MSE(L2)', 'loss', size=(12, 1)), sg.Radio('MB(L0)', 'loss', size=(12, 1))],      
                        [sg.Submit(), sg.Cancel()]]

        self.layout = [
        #Displays the current save file path and allows for it to be changed.
        [sg.Text("Save file path", font = ("Helvetica", 12)),
        sg.Input(readonly = True, size = (50, 1), key = c.SAVEFILE_PATH_KEY),
        sg.Button("Change path", key = c.CHANGE_SAVEFILE_PATH_KEY)],

        #Centred line divider.
        [sg.Push(), sg.Text('_'  * c.DIVIDER_WIDTH, auto_size_text = True, ), sg.Push()],

        #Allows the user to save and load quicksaves.
        [sg.Text("Quicksaves", font = ("Helvetica", 12)),
        sg.Button("Save", key = c.QUICKSAVE_KEY),
        sg.Button("Load last", key = c.LOAD_LAST_QUICKSAVE_KEY),
        sg.Button("Choose quicksave to load", key = c.CHOOSE_QUICKSAVE_LOAD_KEY)]]

        self._initial_checks()


    def _initial_checks(self) -> None:
        #Checks that the config file exists, otherwise creates it.
        if not os.path.exists(c.CONFIG_PATH):
            self._create_config_file()

        #Get config file.
        self.config = self.get_config_file()

        #Checks if the save file path is present in the configuration file.
        if not self.config[c.PATH_VAR_NAME]:
            if not self.get_save_path():
                exit()

        #Checks if the necessary directories exist, if they don't creates them.
        for directory in c.NEEDED_DIRS:
            if not os.path.exists(directory):
                os.mkdir(directory)


    #Creates a config file and stores it in the config path.
    def _create_config_file(self) -> None:
        #We create a dictionary that can then be dumped to the config file.
        config = {
            c.PATH_VAR_NAME: "",
            c.QUICKSAVE_COUNT_VAR_NAME: 3,
            c.AUTOSAVE_COUNT_VAR_NAME: 3,
            c.AUTOSAVE_INTERVAL_VAR_NAME: 2
        }

        with open(c.CONFIG_PATH, "w") as config_file:
            yaml.dump(config, config_file, sort_keys = False)


    #Gets a valid path for the save.
    def get_save_path(self) -> bool:
        path = ""

        #Ask for filenames until we get a valid one or the user presses "cancel".
        while not os.path.exists(path):
            path = sg.popup_get_file("Please enter the path to your save file")

            #This means the "Cancel" button was pressed.
            if path == None:
               return False

        #Once a valid path has been entered update the configuration.
        self.update_config_file(c.PATH_VAR_NAME, path)

        return True


    #Gets the configuration file, note that this function assumes the file exists.
    def get_config_file(self) -> None:
        #Open the configuration file.
        with open(c.CONFIG_PATH) as config_file:
            #We use the "SafeLoader" to avoid leaving a security hole that could be exploited.
            return yaml.load(config_file, Loader = SafeLoader)


    #Updates the given configuration field with the given value. This updates both the class's configuration and the configuration file.
    def update_config_file(self, field: str, value: Any) -> None:
        #Update the corresponding field and dump the changes to the file.
        self.config[field] = value

        with open(c.CONFIG_PATH, "w") as config_file:
            yaml.dump(self.config, config_file, sort_keys = False)


    #Returns a dictionary where the filename is the key and the value is the full path.
    def get_quicksaves(self) -> Dict[str, str]:
        #Stores all quick-saves, the key is the filename and the value it's full path.
        quicksaves = {}

        #The loop gets all the files in the directory, then it saves the ones that are files to the dictionary.
        for file in os.listdir(c.QUICKSAVE_DIR_NAME):
            full_path = os.path.join(c.QUICKSAVE_DIR_NAME, file) 

            if os.path.isfile(full_path):
                quicksaves[file] = full_path

        return quicksaves


    #Creates a simple popup with a list of elements to choose from, it can return one of the elements or "None".
    def popup_list_choice(self, title: str, text: str, select_text:str, list_elems: List[T]) -> T | None:
        layout = [
        [sg.Text(text, font = ("Helvetica", 12))],
        [sg.Listbox(values = list_elems, size = (25, 5), key = "-FILE_LIST-")],
        [sg.Button(select_text, key = "-LOAD-"), sg.Push(), sg.Button("Cancel", key = "-CANCEL-")]]

        return_value = None

        window = sg.Window(title, layout)

        while True:
            event, values = window.read()

            if event == "-CANCEL-" or event == sg.WINDOW_CLOSED:
                break
            #If the load button was pressed, check if there's a list element to return.
            elif event =="-LOAD-":
                if values and values["-FILE_LIST-"]:
                    return_value = values["-FILE_LIST-"][0]

                break

        window.close()

        return return_value


    def manager_loop(self) -> None:
        window = sg.Window("Save manager", self.layout)

        while True:
            event, values = window.read()#timeout=100
            print(event, values)

            #Update save file path.
            window[c.SAVEFILE_PATH_KEY].update(self.config[c.PATH_VAR_NAME])

            match event:
                case sg.WIN_CLOSED:
                    break

                case c.CHANGE_SAVEFILE_PATH_KEY:
                    self.get_save_path()

                case c.QUICKSAVE_KEY:
                    #We get a list of all the keys in the quick-save dictionary, meaning the full paths, and then sort them by the date in which
                    #they were last modified.
                    quicksave_paths = list(self.get_quicksaves().values())
                    quicksave_paths = sorted(quicksave_paths, key=os.path.getmtime)

                    #We get the difference between the maximum number of quick-saves and the current number.
                    file_count_difference = self.config[c.QUICKSAVE_COUNT_VAR_NAME] - len(quicksave_paths)

                    if file_count_difference > 0:
                        #We determine the name of the new quick-save. 
                        new_quicksave = f"quicksave_{self.config[c.QUICKSAVE_COUNT_VAR_NAME] - file_count_difference + 1}"
                        shutil.copy2(self.config[c.PATH_VAR_NAME], os.path.join(c.QUICKSAVE_DIR_NAME, new_quicksave))
                    else:
                        #Otherwise we already have the maximum amount of quick-saves.
                        shutil.copy2(self.config[c.PATH_VAR_NAME], quicksave_paths[0])
                        

                case c.LOAD_LAST_QUICKSAVE_KEY:
                    #We get a list of all the keys in the quick-save dictionary, meaning the full paths, and then sort them by the date in which
                    #they were last modified. Note that the list is reversed to put the most recently modified element at the beginning.
                    quicksave_paths = list(self.get_quicksaves().values())
                    quicksave_paths = sorted(quicksave_paths, key=os.path.getmtime)
                    quicksave_paths.reverse()

                    #We take the most recent file, that is to say quick-save, and copy it to location specified by the configuration file.
                    shutil.copy2(quicksave_paths[0], self.config[c.PATH_VAR_NAME])

                case c.CHOOSE_QUICKSAVE_LOAD_KEY:
                    quicksave_dict = self.get_quicksaves()
                    chosen_quicksave = self.popup_list_choice("Load quicksave", "Choose a quicksave", "Load", list(quicksave_dict.keys()))

                    #If a quick-save was chosen copy it to location specified by the configuration file.
                    if chosen_quicksave != None:
                        shutil.copy2(quicksave_dict[chosen_quicksave], self.config[c.PATH_VAR_NAME])
                    
        window.close()


save_manager = SaveManager()
save_manager.manager_loop()