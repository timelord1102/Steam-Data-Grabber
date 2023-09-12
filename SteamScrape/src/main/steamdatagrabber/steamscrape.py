import json
import requests
import time
import bs4


steamDataPath = "steamscrape\data\jsons\SteamData.json"
failDataPath = "steamscrape\data\jsons\SteamFailed.json"

def getTags(gameID):
    gameSite = requests.get("https://store.steampowered.com/app/" + str(gameID))
    gameSoup = bs4.BeautifulSoup(gameSite.text, "html.parser")
    
    # get all text from app_tag class

    tags = gameSoup.find_all("a", class_="app_tag")
    
    
    tagList = []
    
    for tag in tags:
        tagList.append(tag.getText().strip())

    return tagList

def checkServer():
    try:
        requests.get("https://store.steampowered.com/api/appdetails?appids=10")
    except:
        print("Steam cannot be accessed. Exiting...")
        exit()
        
def saveData(failedDict, gamesDict, origGameLen, origFailLen):
    if(len(failedDict) > origFailLen) or (len(gamesDict) > origGameLen):
        print('\033[91m'+"Saving..." + '\033[0m')
        with open (steamDataPath, "w") as newJSON:
            json.dump(gamesDict, newJSON, indent=4, separators=(',', ': '))
        with open (failDataPath, "w") as newJSON:
            json.dump(failedDict, newJSON, indent=4, separators=(',', ': '))
    with open (steamDataPath) as steamJSON:
        gamesDict = json.load(steamJSON)
    with open (failDataPath) as failedJSON:
            failedDict = json.load(failedJSON)
    return failedDict, gamesDict, origGameLen, origFailLen

def addGame(gamesDict, game, gameID, reviewData):
    print("\tGame: " + str(game["name"]))
    tags = getTags(gameID)
    gamesDict[gameID] = {}
    gamesDict[gameID]["tags"] = tags
    gamesDict[gameID]["is_free"]  =(game["is_free"])
    if(game["is_free"] == False):
        gamesDict[gameID]["price_overview"] = (game["price_overview"])
    try:
        gamesDict[gameID]["dlc"] = (game["dlc"])
    except:
        gamesDict[gameID]["dlc"] = ["None"]
    gamesDict[gameID]["reviews"] = [reviewData["query_summary"]["total_reviews"], reviewData["query_summary"]["review_score_desc"]]
    
    
    return gamesDict

def addFailed(failedDict, reviewData, game, gameID, failed):
    print('\033[93m' + "False" + '\033[0m')
    failedDict[gameID] = {}
    if(failed):
        checkServer()
        failedDict[str(gameID)]["fail_reason"] = "JSON Access Failed"
    elif(game[str(gameID)]["success"] == False):
        failedDict[gameID]["fail_reason"] = "No game found"
    elif game[str(gameID)]["data"]["type"] != ("game"):
        failedDict[gameID]["fail_reason"] = game[str(gameID)]["data"]["type"]    
    else:
        game = game[str(gameID)]["data"]
        tags = getTags(gameID)
        if game["name"].lower().find("playtest") == -1:
            failedDict[gameID]["fail_reason"] = "playtest"
        else:
            failedDict[gameID]["fail_reason"] = "Bad review data" 
        failedDict[gameID]["tags"] = tags
        failedDict[gameID]["is_free"]  =(game["is_free"])
        if(game["is_free"] == False):
            try:
                failedDict[gameID]["price_overview"] = game["price_overview"]
            except:
                failedDict[gameID]["price_overview"] = "No price data (most likely playtest)"
        try:
            failedDict[gameID]["dlc"] = (game["dlc"])
        except:
            failedDict[gameID]["dlc"] = ["None"]
        failedDict[gameID]["reviews"] = [reviewData["query_summary"]["total_reviews"], reviewData["query_summary"]["review_score_desc"]]
    failed = False
    return failedDict, failed
        
        
checkServer() 
        
jsonFile = requests.get("http://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json").json()


try:
    open(steamDataPath).close()
except:
    open(steamDataPath, "x").close()
    
try:
    open(failDataPath, "a")
except:
    open(failDataPath, "x").close()
      
if(len(open(failDataPath).read()) == 0):
    json.dump({}, open(failDataPath, "w"))
    time.sleep(0.3)
    
if(len(open(steamDataPath).read()) == 0):
    json.dump({}, open(steamDataPath, "w"))
    time.sleep(0.3)
    
gamesDict = {}
failedDict = {}
dlcDict = {}
comingsoonDict = {}

with open (steamDataPath) as steamJSON:
    gamesDict = json.load(steamJSON)
    time.sleep(0.3)

with open (failDataPath) as failedJSON:
    failedDict = json.load(failedJSON)
    time.sleep(0.3)


print("Starting...")
origFailLen = len(failedDict)
origGameLen = len(gamesDict)
i = 0
for app in jsonFile["applist"]["apps"]:
    i += 1
    if(i % 10 == 0):
        failedDict, gamesDict, origGameLen, origFailLen = saveData(failedDict, gamesDict, origGameLen, origFailLen)
    gameID = str(app["appid"])
    
    if gameID not in gamesDict and gameID not in failedDict:
        print('\033[96m' + str(i) + '/' + str(len(jsonFile["applist"]["apps"]))+ '\033[0m')
        time.sleep(1)
        print("\t" + str(gameID) + ": ", end="")
        
        failed = False
        try:
            game = requests.get("https://store.steampowered.com/api/appdetails?appids=" + str(gameID)).json()
        except:
            failed = True
        while(game == None):
            checkServer()
            failed = False
            print('\033[91m' + "None" + '\033[0m' + " (Waiting 5 minutes)")
            time.sleep(300)
            try:
                game = requests.get("https://store.steampowered.com/api/appdetails?appids=" + str(gameID)).json()
            except:
                failed = True
        
        reviewData = requests.get("https://store.steampowered.com/appreviews/" + str(gameID) + "?json=1").json()
        if(not failed and game[str(gameID)]["success"] == True and game[str(gameID)]["data"]["type"] == ("game")and reviewData["success"] == 1 and 
           (("positive" in reviewData["query_summary"]["review_score_desc"].lower() and reviewData["query_summary"]["total_reviews"] > 100) or game[str(gameID)]["data"]["release_date"]["coming_soon"] == True)) and game[gameID]["data"]["name"].lower().find("playtest") == -1:
            print('\033[92m' + str(game[str(gameID)]["success"]) + '\033[0m')
            game = game[str(gameID)]["data"]
            if(game["release_date"]["coming_soon"] == False):
                gamesDict = addGame(gamesDict, game, gameID, reviewData)
            elif (game["release_date"]["coming_soon"] == True):
                print("\tComing Soon, skipping...")
            else:
                print("Unknown Error")
                exit()
        else:
            failedDict, failed = addFailed(failedDict, reviewData, game, gameID, failed)
        



