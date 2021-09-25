#!/usr/bin/env python3

import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
from time import sleep
from os.path import exists
import argparse
import psutil

''' 
-----------------------------------------------------------------------------------------------------
Here is a script for automatically scraping and preparing TryHackMe rooms Write-Up files in Markdown.
It creates a README.md file filled with the tasks and 
questions.
Author :    Maxime Beauchamp AKA Octomany
Date :      24 September 2021

NOTE : Selenium AND Chrome needs to be installed for this script to work

Selenium installation : 
    pip install selenium

Chrome installation : (Debian) 
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install ./google-chrome-stable_current_amd64.deb
-----------------------------------------------------------------------------------------------------
''' 

Options = Options()
Options.add_argument('headless')

Current_Dir = os.getcwd()
Script_Dir = sys.path[0]
driver = webdriver.Chrome(Script_Dir + '/chromedriver', options=Options)

parser = argparse.ArgumentParser(description='Automatic THM Write-Up README file creator.')
parser.add_argument('RoomName', action='store', type=str, help='Specify the room name (Taken from URL)')
arg = parser.parse_args()

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



# Open the README.md file for writing
ReadMeFile = Current_Dir + '/README.md'

print (ReadMeFile)

# Check if there's a README.md file already existing
file_exists = exists(ReadMeFile)


if file_exists == True:
    while True:
        Ans = input("A README.md file already exists. Overwrite it? (Y/n) : ")
        if Ans == ("y") or Ans == ("Y"):
            break
        elif Ans == ("n") or Ans == ("N"):
            print("Renaming the file to Scraper_README.md...")
            ReadMeFile = Current_Dir + '/Scraper_README.md'
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
print("Readme file successfully created and filled.\nNow shutting down Chromedriver...")

# Killing the chromedriver process manually since selenium does not seem to be able to do it by itself.
PSDriver = "chromedriver"
PSChrome = "chrome"

for proc in psutil.process_iter():
    if proc.name() == PSDriver or proc.name() == PSChrome: 
        proc.kill()
        

exit()
