#!/usr/bin/env python

"""
DS3Backup 
-------------------------
A simple application to help backup your DS3 data.
Built with Python and Tkinter.
"""

from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from zipfile import ZipFile

def create_gui():
    """
    Creates the application GUI via Tkinter and returns
    the window and text entry boxes as objects.
    """
    """ window settings """
    window = tk.Tk()
    window.title('DS3 Backup')
    window.geometry('500x200')
    window.configure(bg = '#dedede')

    """ from widgets """
    from_label = tk.Label(text = 'DS3 Profile Location', bg = '#dedede')
    from_label.place(x=50, y=10)
    from_entry = tk.Entry(
        width = 60,
        bg = 'white',
    )
    from_entry.place(x=50, y=40)
    from_filedialog_button =  tk.Button(
        text = '...',
        width = 5,
        height = 1,
        bg = "#dedede",
        command = lambda : filedialog_callback(from_entry)
    )
    from_filedialog_button.place(x=425, y=37)

    """ to widgets """
    to_label = tk.Label(text = 'DS3 Backup Location', bg = '#dedede')
    to_label.place(x=50, y=70)
    to_entry = tk.Entry(
        width = 60,
        bg = 'white',
        )
    to_entry.place(x=50, y=100)
    to_filedialog_button =  tk.Button(
        text = '...',
        width = 5,
        height = 1,
        bg = "#dedede",
        command = lambda : filedialog_callback(to_entry)
    )
    to_filedialog_button.place(x=425, y=97)

    """ backup button widget """
    backup_button = tk.Button(
        text='Backup',
        width=25,
        height=1,
        bg='#dedede',
        command = lambda: backup(from_entry.get(), to_entry.get())
    )
    backup_button.place(x=137.5, y=150)

    return window, from_entry, to_entry


def filedialog_callback(entry):
    """
    Executes when a file dialog button is pressed.
    Accepts the appropriate entry, deletes it's contents,
    and replaces it with the selected directory.
    """
    dir_path = tk.filedialog.askdirectory()

    if len(dir_path) > 0:
        entry.delete(0, 'end')
        entry.insert(0, dir_path)


def get_ds3_profile():
    """
    Returns the current path to the DS3 Profile by
    checking the default location. Otherwise,
    returns None.
    """
    appdata = os.environ.get('APPDATA')
    profile = appdata + '\DarkSoulsIII'
    if os.path.isdir(profile):
        for dirname, dirs, files in os.walk(profile):
            for file in files:
                if file.endswith('sl2'):
                    return dirname
    
    return None


def get_all_file_paths(base_dir):
    """
    Returns a list that contains the path of all
    files within a given directory.
    """
    file_paths = []

    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


def get_zip_file_path(to_path):
    """
    Accepts a path to a desired backup location.
    Returns a the path to a time-stamped DS3 zip file.
    """
    datetime_obj = datetime.now()
    timestamp = datetime_obj.strftime('%m%d%Y_%H%M%S')
    
    return to_path + '\\' + timestamp + '_DS3_Backup.zip'


def backup(from_path, to_path):
    """
    Creates a zip file containing all files within the
    given DS3 profile at the given back up location.
    """
    if os.path.isdir(from_path) and os.path.isdir(to_path):
        file_paths = get_all_file_paths(from_path)
        zip_file_name = get_zip_file_path(to_path)

        with ZipFile(zip_file_name, 'w') as zip:
            for file in file_paths:
                zip.write(file)

        messagebox.showinfo("DS3Backup", "Backup Complete!")
    else:
        messagebox.showerror("DS3Backup Error", "Path does not exist.")


if __name__ == "__main__":
    window, from_entry, to_entry = create_gui()
    profile = get_ds3_profile()
    from_entry.insert(0, profile)
    window.mainloop()