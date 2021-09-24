#!/usr/bin/env python3

import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import date
from time import sleep
from os.path import exists
import argparse

from webdriver_manager.driver import Driver

'''
-----------------------------------------------------------------------------------------------------
Here is a script for automatically scraping and preparing TryHackMe rooms Write-Up files in Markdown.
It creates a directory with the room's name and then a README.md file filled with the tasks and 
questions.
Author :    Maxime Beauchamp AKA Octomany
Date :      13 September 2021
-----------------------------------------------------------------------------------------------------
'''

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

parser = argparse.ArgumentParser(description='Automatic THM Write-Up README file creator.')
parser.add_argument('RoomName', action='store', type=str, help='Specify the room name (Taken from URL)')
arg = parser.parse_args()

# Installation of the Chrome Driver if needed
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

# Maximize the browser
driver.maximize_window()

# Room name
RoomName = arg.RoomName

# Load the Rooms page
driver.get("https://tryhackme.com/room/"+RoomName)
# Wait for the page to load
sleep(2)

# Check if the room is valid
search_text = "If this is an error on our behalf. Please contact us."

if (search_text in driver.page_source):
    print("Error : This room seems non-existant or unreachable. Please Try Again")
    input("Press any key to exit...")
    exit()

""" # Create the new directory
if not os.path.isdir(RoomName):
    print('The directory is not present. Creating a new one..')
    os.mkdir(RoomName)
else:
    print('The directory is present.') """



# Open the README.md file for writing
ReadMeFile = 'README.md'

# Check if there's a README.md file already existing
file_exists = exists(ReadMeFile)

if file_exists == True:
    while True:
        Ans = input("A README.md file already exists. Overwrite it? (Y/n) : ")
        if Ans == ("y") or Ans == ("Y"):
            break
        elif Ans == ("n") or Ans == ("N"):
            print("Renaming the file to Scraper_README.md...")
            ReadMeFile = RoomName+'_README.md'
            break
        else:
            print("Invalid Answer... Y or N")

# Open the Readme File
f = open(ReadMeFile, 'w')

# Get the room informations
Title = driver.find_element_by_id("title").text
Description = driver.find_element_by_id("description").text

# Add infos to the variable
print("\nGetting general room Infos...\n")
File_Content = "# "+Title+"\n" + "> By AUTHOR | "+ str(date.today()) + "\n------------------------------------------" + "\n\n # "+ Description + "\n\n"

# set implicit wait time
driver.implicitly_wait(10) # seconds

# Get the Tasks
Tasks = driver.find_elements_by_class_name("card-link")
NbOfTasks = len(Tasks)
TaskNb=1

# Get the questions
Questions = driver.find_elements_by_class_name("room-task-question-details")

print("Getting the tasks & questions...\n\n")
for task in Tasks:
    
    driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", task)
    
    if TaskNb !=1: task.click()
    sleep(0.35)

    File_Content = File_Content + "# " + task.text + "\n\n"
    
    CurrentTask = driver.find_element_by_id('task-'+str(TaskNb))
    CurrentQuestions = CurrentTask.find_elements_by_class_name("room-task-question-details")
    
    for Q in CurrentQuestions:
        driver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", Q)
        sleep(0.5)
        
        if Q.is_displayed() == True:
            File_Content = File_Content + "## " + Q.text + "\n'''\n\n'''\n\n"

    print("Completed : Task " + str(TaskNb) + "/" + str(NbOfTasks), end="\r")
    TaskNb=TaskNb+1

f.write(File_Content)
f.close()
driver.quit()
print("That's it! Everything should be saved. Thank you for using this script - Maxime Beauchamp, AKA Octomany\n")
exit()