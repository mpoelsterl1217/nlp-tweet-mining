from reader import read_tweet_data
from find_hosts import find_host
from find_nominees import find_nominees
from find_presenters import find_presenters
from find_winner import find_winner
from alternate_find_award import find_award
from find_performers import find_performers
from filter_tweets import filter_tweets
from pickle_preprocess import unpickle_tweets
import json

if __name__ == "__main__":
    JSON_FILE = "gg2013.json"

    # tweets = read_tweet_data(JSON_FILE)
    tweets = unpickle_tweets()
    tweets = filter_tweets(tweets)
    print("tweet length:", len(tweets))

    host = find_host(tweets)
    print("hosts:", host)

    print("\n\n")
    performers = find_performers(tweets)
    print("performers:", performers)

    json_data= {
        "Host": host,
        "Performers": performers,
        "award_data": {}
    }

    award_list = find_award(tweets)
    awards_final = []
    for i in award_list:
        awards_final.append(max(i, key=len))

    with open("output.txt", "w", encoding="utf-8") as file:
        for award in award_list:
            # award = awards_final[i]
            print("\n\n")
            print("AWARD:", award)
            print("alternative names:", award_list[award])
            award_names = "(" + "|".join(award_list[award]) + ")"
            nominees = find_nominees(award_names, tweets)
            print("nominees:", nominees)
            winner_list = find_winner(award_names, nominees, tweets)
            winner = winner_list[0] if winner_list != [] else None
            if not winner:
                continue
            print("winner:", winner)
            presenter = find_presenters(award_names, winner, tweets)
            print("presenters:", presenter)

            file.write(f"Award: {award}\n")
            file.write(f"alternative names: {award_list[award]}\n")
            file.write(f"Presenters: {presenter}\n")
            file.write(f"Nominees: {nominees}\n")
            file.write(f"Winner: {winner}\n")
            
            json_data["award_data"][award]={
                "nominees" : nominees,
                "presenters" : presenter,
                "winner" : winner
            }
        file.write(f"performers: \"{performers}\"\n")

    # with open("output.txt", "w", encoding="utf-8") as file:
    #     for i in range(len(award_list)):
    #         award = awards_final[i]
    #         print("\n\n")
    #         print("AWARD:", award)
    #         print("alternative names:", award_list[i])
    #         award_names = "(" + "|".join(award_list[i]) + ")"
    #         nominees = find_nominees(award_names, tweets)
    #         print("nominees:", nominees)

    #         winner = find_winner(award_names, nominees, tweets)
    #         if not winner:
    #             continue
    #         print("winner:", winner)

    #         presenter = find_presenters(award_names, winner[0], tweets)
    #         print("presenters:", presenter)
            
    #         file.write(f"Award: {award}\n")
    #         file.write(f"alternative names: {award_list[i]}\n")
    #         file.write(f"Presenters: {presenter}\n")
    #         file.write("Nominees: " + ", ".join(f'"{nominee}"' for nominee in nominees) + "\n")
    #         file.write(f"Winner: \"{winner}\"\n")
            
    #         json_data["award_data"][award]={
    #             "nominees" : nominees,
    #             "presenters" : presenter,
    #             "winner" : winner
    #         }
    #     file.write(f"performers: \"{performers}\"\n")
    
    output_file = "result.json"
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    print(f"Data has been written to {output_file}")
