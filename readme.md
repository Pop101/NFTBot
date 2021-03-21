# NFTBot
Upload entire albums as NFTs without paying a dime!

## Table of contents
* [Technologies](#technologies)
* [General info](#general-info)
* [Setup](#setup)
* [Usage](#usage)

## Technologies
This project is created with:
* [Selenium](https://pypi.org/project/opencv-contrib-python/): 3.141.0
* [Metamask](https://pypi.org/project/numpy/): 1.19.0
* [AutoIt](https://www.autoitscript.com/site/) via [PyAutoIt](https://pypi.org/project/PyAutoIt/): 0.6.0
* [Opensea](https://opensea.io)

## General info
This project automates the production of NFTs on [Opensea](opensea.io). It seeks to allow photographers and artists to upload many of their works as NFTs at once with minimal effort. [Opensea](opensea.io) is ideal for this as it allows for the off-chain creation and sale of assets, so you can create many of them without any initial investment. \
Sadly, I could not upload a file automatically to [Opensea](opensea.io) without [AutoIt](https://www.autoitscript.com/site/). Therefore, this program **cannot run headlessly.** and **only supports windows!** 

Please use this responsibly. Do not run bots.

All included images are from [Pixabay](https://pixabay.com) and are licensed under [Pixabay's license](https://pixabay.com/service/terms/#license) 
	
## Setup
To run this project, first download it and install the requirements with `pip3 install -r requirements.txt`. \
It is very likely that you will need to update your chrome driver if you wish to run it with its default settings. Get the most recent version of ChromeDriver [here](https://chromedriver.chromium.org/) \
When running the program, you will need to have an Ethereum wallet's Seed Phrase.

## Usage
Simply starting the program with python3: `python3 nftbot.py` will automatically prompt for a seed phrase and upload all images in the `./images/` directory as NFTs

For implementation in your own projects, the `file_to_nft_info(...)` function converts a file's path into the dictionary used to make an nft with the program. `setup_metamask_with_opensea(driver, seed_phrase)` takes in a Selenium Webdriver and logs it into both Metamask and Opensea with the given seed phrase. `create_nft(driver, nft_info)` takes a logged-in Webdriver and the nft's info to create it on opensea. It can be called many times once a Webdriver has been logged in.

### Configuration
```pyt
 # Required fields:
'name': str
'image': set by program

 # Possible fields:
'link': str # must be valid url
'description': str # Write something nice here
'unlocked': str # Hidden Info

'properties': {   # listed as plaintext
  str : str
 }
'levels': {       # listed as a large bar
  str : (int, int)
 }
'stats': {        # listed as a single number
  str : (int, int)
 }
```
#### Default Placeholders
```pyt
 # Placeholders:
'%n' # the name of the file (\ and " and ' are skipped). The case will be adjusted
'%t' # the file's type
'%i' # the number of file processed (starting at 1)
'%o' # the total number of files the program will process
'%d' # the date the file was last modified
'%c' # the file's creation date
'%z' # the file's size
```
