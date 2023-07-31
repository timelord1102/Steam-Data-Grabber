A tool I made for a future project.

Using Steam's API and beautifulSoup4, gets data from steams entire library following a specific criteria. 

Steam API gets game data including appID , price, review data and DLC data (by default) and saves to a new json file. BeautifulSoup4 acts at the same time scraping the game's steam page to gather it's tag data

Games that do not match the criteria are put in a seperate json file with their information and reason for failiure. If the reason is a result of the app not being a game no game data is savd, only reason for failiure.

This tool was necessary to prevent a large amount of very slow API calls to steams API and because steam's API does not provide game tag data

Plans for this tool:
Fix any bugs
Provide complete base data jsons
Allow specifying wanted data

	
Current Issues:

Absurdly long run time: 	                                                                                            
             Takes almost a week to run through all data from scratch. This is due to steam's absolutly massive game library and their limit on API calls. Unsure if fixable
