import requests
import json
import matplotlib.pyplot as plt

def getShowData(id, apikey):
    url = "http://www.omdbapi.com/?i={}&apikey={}".format(id, apikey)
    data = requests.get(url)
    if not data.ok:
        print("Could not get number of episodes in {} using api key {}".format(id, apikey))

    jData = json.loads(data.content)
    return int(jData["totalSeasons"]), jData["Title"]



def getListOfEpisodes(id, season, apikey):
    url = "http://www.omdbapi.com/?i={}&apikey={}&Season={}".format(id, apikey, season)
    data = requests.get(url)
    if not data.ok:
        print("Could not get episodes of {}, season {} using api key {}".format(id, season, apikey))

    jData = json.loads(data.content)
    print("Fetched {} season {}".format(jData["Title"], jData["Season"]))
    return jData["Episodes"]

def getRatingsFromSeason(episodes):
    return {int(i["Episode"]):float(i["imdbRating"]) for i in episodes if i["imdbRating"] != "N/A" }

def plotRatings(ratings, title):

    # Flatten dict into 1D list
    tmp = [list(ratings[season].values()) for season in ratings.keys()]
    raw_values = [v for s in tmp for v in s]

    seasonLenghts = [len(i) for i in ratings.values()]

    fig, ax = plt.subplots()
    ax.plot(range(1, sum(seasonLenghts) + 1), raw_values, color="lightgray")

    delta = 1
    for i,v in enumerate(seasonLenghts):
        x = list(range(delta, delta + v))
        y = raw_values[delta - 1:delta + v - 1]
        ax.plot(x, y, 'o', label="Season " + str(i + 1))
        delta += v
    plt.xlabel("Episode number")
    plt.ylabel("IMDb Rating")
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left", borderaxespad=0)
    plt.grid(True)
    plt.savefig(title.replace(" ", "_") + ".eps", bbox_inches="tight")
    plt.show()


def main():
    gotIMDBId = "tt0944947"
    API_KEY = "2c2c66ba"

    nSeasons, title = getShowData(gotIMDBId, API_KEY)
    
    ratings = {}
    for i in range(1, nSeasons + 1):
        data = getListOfEpisodes(gotIMDBId, i, API_KEY)
        ratings[i] = getRatingsFromSeason(data)

    with open(title.replace(" ", "_") + "_ratings.json", "w") as f:
        f.write(json.dumps(ratings))
    
    plotRatings(ratings, title)



if __name__ == "__main__":
    main()
