from pathlib import Path
import os


# Gets the home directory
def get_home_directory():
    if (Path.exists(Path.home())):
        return Path.home()
    return Path()


# Gets the desktop directory
def get_desktop_directory():
    string_home_directory_path = str(get_home_directory())
    string_desktop_path = string_home_directory_path + r'\Desktop'

    if(Path.exists(Path(string_desktop_path))):
        return Path(string_desktop_path)
    return Path()


# Clean desktop by removing shortcuts, documents and images
def clean_desktop(extensions, path_of_desktop_shortcut_folder):
    extensions_list = extensions.split(" ")
    if('*' in extensions_list):
        list_of_folders = get_desktop_directory().glob('*')
        for folder in list_of_folders:
            if(folder.is_dir() and not ('Cleaning Folder' in folder.name)):
                relative_path_from_desktop = folder.relative_to(get_desktop_directory())
                os.rename(src=f'{folder}', dst=f'{str(path_of_desktop_shortcut_folder)}\{relative_path_from_desktop}')
    else: 
        for extension in extensions_list:
            desktop_directory_path = get_desktop_directory()
            shortcut_files_generator = desktop_directory_path.glob(extension)
            try:
                for shortcut_file in shortcut_files_generator:
                    relative_path_from_desktop_shortcut_file = shortcut_file.relative_to(
                        get_desktop_directory())
                    os.rename(
                        src=f'{shortcut_file}', dst=f'{str(path_of_desktop_shortcut_folder)}\{relative_path_from_desktop_shortcut_file}')
            except ValueError:
                pass


# Create new folders with respect to cleaning folder
def create_new_folders_wrt_cleaning_folder(cleaning_folder_path, types, extensions):
    dictionary_mapping_of_folders_and_extensions = {}
    for type_of_folder, type_of_extension in zip(types, extensions):
        dictionary_mapping_of_folders_and_extensions[type_of_extension] = Path(str(cleaning_folder_path) + f'\{type_of_folder}')
    return dictionary_mapping_of_folders_and_extensions


# Main code of execution
string_home_directory_path = str(get_home_directory())

string_desktop_path = str(get_desktop_directory())

path_desktop_cleaning_folder = Path(string_desktop_path + r'\Cleaning Folder')
types_of_folders = ['Documents', 'Pictures', 'Shortcuts', 'Folders', 'Music and Videos']


extension_for_documents = str('*.txt *.pdf *.doc *.docx *.xls *.xlsx *.pptx *.csv *.rar *.zip')
extension_for_pictures = str('*.png *.jpg *.jpeg')
extension_for_shortcuts = str('*.lnk *.exe')
extension_for_folders = str('*')
extension_for_music_and_videos = str('*.mp3 *.mp4')

extensions_list = []
extensions_list.extend([extension_for_documents, extension_for_pictures, 
extension_for_shortcuts, extension_for_folders, extension_for_music_and_videos])

dict_mapping_of_folders_and_extensions = create_new_folders_wrt_cleaning_folder(path_desktop_cleaning_folder, types_of_folders, extensions_list)

if (not path_desktop_cleaning_folder.exists()):
    path_desktop_cleaning_folder.mkdir()

for value in dict_mapping_of_folders_and_extensions.values():
    if(not value.exists()):
        value.mkdir()

for key, value in dict_mapping_of_folders_and_extensions.items():
    clean_desktop(key, value)
