A tool used to scrape data for all Steam games and DLC

Uses Steams API paired with beautifulsoup4 to gather price data, genres data, game IDs, game reviews, and game tags (game tags being inaccessible with Steams API)
All data is saved to a JSON file which can be updated by running the code again, appending any new data to the end of the file.

If any game cannot be properly scraped, it is added to a second file along side the reason for its failiure to be ignored in future runs

### Required:
- python3.8+  
- beautifulsoup4 : 
```pip install beautifulsoup4```

### Plans for this tool:  
- Fix any bugs  
- Provide complete base data Json files  
- Allow for specification of desired data  
- Implement into potential future project  

### Current Issues:  
- Very long run-time. Can take up to a week for the initial data gathering which seems unavoidable without breaking the Steam API TOS. Potentially fixed by providing pre-scraped data files
