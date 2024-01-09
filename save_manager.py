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


#Gets the configuration file, note that this function assumes the file exists.
def get_config_file() -> None:
    #Open the configuration file.
    with open(constants.CONFIG_PATH) as config_file:
        #We use the "SafeLoader" to avoid leaving a security hole that could be exploited.
        return yaml.load(config_file, Loader = SafeLoader)


def create_config_file() -> None:
    config = {
        constants.PATH_VAR_NAME: "",
        constants.QUICKSAVE_COUNT_VAR_NAME: 3,
        constants.AUTOSAVE_COUNT_VAR_NAME: 3,
        constants.AUTOSAVE_INTERVAL_VAR_NAME: 2
    }

    with open(constants.CONFIG_PATH, "w") as config_file:
        yaml.dump(config, config_file, sort_keys = False)


#Checks that the configuration file exists, if not it creates it.
def check_config_file():
    if not os.path.exists(constants.CONFIG_PATH):
        create_config_file()
        

#Checks if the save file path is present in the configuration file.
def check_save_path() -> bool:
    config_file = get_config_file()
    print(config_file)

    if not config_file[constants.PATH_VAR_NAME]:
        path = ""

        #Ask for filenames until we get a valid one or the user presses "cancel".
        while not os.path.exists(path):
            path = sg.popup_get_file("Please enter the path to your save file")

            if path == None:
                return False

    return True


check_config_file()
#If the user didn't provide a valid path for the save file exit before starting the manager.
if not check_save_path():
    exit()

"""while True:
   event, values = window.read()

   if event == sg.WIN_CLOSED:
        break

    window = sg.Window('Machine Learning Front End', layout, font=("Helvetica", 12))"""