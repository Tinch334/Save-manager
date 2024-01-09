import PySimpleGUI as sg
import os
import constants
import yaml
from yaml.loader import SafeLoader


#Set color scheme      
sg.theme('GreenTan')

sg.set_options(text_justification='left')  

layout = [[sg.Text('Machine Learning Command Line Parameters', font=('Helvetica', 16))],      
    [sg.Text('Passes', size=(15, 1)), sg.Spin(values=[i for i in range(1, 1000)], initial_value=20, size=(6, 1)),      
     sg.Text('Steps', size=(18, 1)), sg.Spin(values=[i for i in range(1, 1000)], initial_value=20, size=(6, 1))],      
    [sg.Text('ooa', size=(15, 1)), sg.In(default_text='6', size=(10, 1)), sg.Text('nn', size=(15, 1)),      
     sg.In(default_text='10', size=(10, 1))],      
    [sg.Text('q', size=(15, 1)), sg.In(default_text='ff', size=(10, 1)), sg.Text('ngram', size=(15, 1)),      
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


class SaveManager:
    def __init__(self):
        #Checks that the config file exists, otherwise creates it.
        if not os.path.exists(constants.CONFIG_PATH):
            self.create_config_file()

        #Get config file.
        self.config = self._get_config_file()

        #If no path is set for the save file exit the program.
        if not self.check_save_path():
            exit()        


    def create_config_file(self) -> None:
        config = {
            constants.PATH_VAR_NAME: "",
            constants.QUICKSAVE_COUNT_VAR_NAME: 3,
            constants.AUTOSAVE_COUNT_VAR_NAME: 3,
            constants.AUTOSAVE_INTERVAL_VAR_NAME: 2
        }

        with open(constants.CONFIG_PATH, "w") as config_file:
            yaml.dump(config, config_file, sort_keys = False)


    #Checks if the save file path is present in the configuration file.
    def check_save_path(self) -> bool:
        if not self.config[constants.PATH_VAR_NAME]:
            path = ""

            #Ask for filenames until we get a valid one or the user presses "cancel".
            while not os.path.exists(path):
                path = sg.popup_get_file("Please enter the path to your save file")

                if path == None:
                    return False

            #Once a valid path has been entered update the configuration.
            self._update_config_file(constants.PATH_VAR_NAME, path)

        return True

    #Gets the configuration file, note that this function assumes the file exists.
    def _get_config_file(self) -> None:
        #Open the configuration file.
        with open(constants.CONFIG_PATH) as config_file:
            #We use the "SafeLoader" to avoid leaving a security hole that could be exploited.
            return yaml.load(config_file, Loader = SafeLoader)


    #Updates the given configuration field with the given value. This updates both the class's configuration and the configuration file.
    def _update_config_file(self, field, value) -> None:
        self.config[field] = value

        with open(constants.CONFIG_PATH, "w") as config_file:
            yaml.dump(self.config, config_file, sort_keys = False)



"""while True:
   event, values = window.read()

   if event == sg.WIN_CLOSED:
        break

    window = sg.Window('Machine Learning Front End', layout, font=("Helvetica", 12))"""

save_manager = SaveManager()