# nlp-tweet-mining

Catherine Tawadros, Runkai Qiu, Mattie Poelsterl
GitHub link: [https://github.com/noah-alvarado/cs-337-project-1.git](https://github.com/mpoelsterl1217/nlp-tweet-mining.git)

Our code can be run simply by running "pip install -r requirements.txt" in a virtual environment and then running python main.py. Right now, it is set to use "gg2013.json" as input data in the main loop - this can be changed by simply typing in a different json file name on line 13 of main.py.

Our code identifies the hosts and performers, along with award names, presenters, nominees, and winners of each award.

The output of json file is result.json. The output of txt file is output.txt. You also can check the result in terminal which should also contain the list of candidates.

I don't think you need specify the python version, but if you can't run you can try Python 3.11.5
Yes, you need to download some models like spacy or NLTK, but it should be in requirements.txt

Our program takes lots of time to run and get the result. Please wait a moment.

Output:
    
    {
        hosts: host names
        performer: performer names
        award_data[award]={
                    "nominees" : nominees,
                    "presenters" : presenter,
                    "winner" : winner
                }
    }
