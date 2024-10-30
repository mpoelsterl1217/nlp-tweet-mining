import json
import spacy
from fuzzywuzzy import fuzz
from find_winner import identify_winner
from find_nominees import identify_nominees
from aggregate_person import aggregate_people
from reader import read_tweet_data

tweets, users = read_tweet_data("gg2013.json")


award_name_13=['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

# # Initialize the dictionary to hold lists of tweets for each award
# tweet_with_award_name = {award: [] for award in award_name_13}

# # Assuming 'tweets' is a dictionary where each value is an object with a 'clean_text' attribute
# for tweet in tweets.values():
#     for award in award_name_13:
#         if award in tweet.clean_text.lower():  # Using lower() for case-insensitive matching
#             tweet_with_award_name[award].append(tweet)

# empty=[]
# with open('tweet_award_names.txt', 'w', encoding='utf-8') as f:
#     for award, tweets in tweet_with_award_name.items():
#         if tweets:
#             f.write(f"Award: {award}\n")
#             f.write("Tweets:\n")
#             for tweet in tweets:
#                 f.write(f" - {tweet.clean_text}\n")  # Adjust this line based on how you want to display the tweet
#             f.write("\n")  # For better separation between awards
#         else:
#             empty.append(award)

# print(empty)

# for i in award_name_13:
# winners=identify_winner("best animated", [], tweets)
# print(winners)
    # if result:
    #     print(i+" : "+max(result, key=result.get))
    # else:
    #     print(i + " : empty")

nominees=identify_nominees("best animated", tweets)
print(nominees)