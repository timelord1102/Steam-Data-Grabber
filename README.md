A tool I made for a future project.

Using Steam's API and beautifulSoup4, gets data from steams entire library following a specific criteria. 

Steam API gets game data including appID , price, review data and DLC data (by default) and saves to a new json file. BeautifulSoup4 acts at the same time scraping the game's steam page to gather it's tag data

Games that do not match the criteria are put in a seperate json file with their information and reason for failiure. If the reason is a result of the app not being a game no game data is savd, only reason for failiure.

This tool was necissary to prevent a large amount of very slow API calls to steams API and because steam's API does not provide game tag data