# Robo-Advisor

## Prerequsites

*Anaconda 3.7
*Python 3.7
*Pip

## Installation
Use the GitHub.com online interface to create a new remote project repository called something like "robo-advisor". Also add a "README.md" file during the repo creation process. After this process is complete, you should be able to view the repo on GitHub.com at an address like https://github.com/YOUR_USERNAME/robo-advisor.

After creating the remote repo, use GitHub Desktop software or the command-line to download or "clone" it onto your computer. Choose a familiar download location like the Desktop.

```sh
cd ~/Desktop/robo-advisor
```
From this repository you should be able to access the complete python code with the "app" folder, requirements.txt file and the .gitignore file. 

## Setup
Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 
conda activate stocks-env
```
From inside the virtual environment, install package dependencies:
```sh
pip install -r requirements.txt
```
## Setup
Before using or developing this application, take a moment to obtain an AlphaVantage API Key (e.g. "abc123").
The link is: https://www.alphavantage.co/support/#api-key

After obtaining an API Key, copy the ".env.example" file to a new file called ".env", and update the contents of the ".env" file to specify your real API Key.

## Usage
In order to run the program and successfully use it please enter the 
follwing in your command line promopt:

```sh
python robo_advisor.py
```
## Understanding

Valid identifiers for this program are based on the user prompted "please enter a stock ticker". A valid stock ticker is 3 or 4 characters that don't include any digits (there is a test to check if there is any digits or if the string is greater than 5 characters). If the code identifies that there is a clearly invalid ticker entered, it will ask the user to try again before implementing the API request. At this point there is another test to make sure the ticker is actually valid and stock data is accessible. If stock data is not accessible, the program will once again request a different ticker from the user.

Important understanding also includes the visualization which showcases the stock price at the close of the market daily. Once the user clicks out the visualization, a csv file is generated called prices.csv which contains all the relevant stock information displayed in the printed output. The stock recommendation is based off the highest and lowest price the stock has traded at in the available time period and calculates the average. It then adds a 20% margin to the average and checks if the current price of the stock is above or below the adjusted average. Below the adjusted average results in a buy recommendation and over the adjusted average means the stock is too expensive and the user is not advised to purchase the stock.


