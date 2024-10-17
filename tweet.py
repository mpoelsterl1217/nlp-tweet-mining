import user
import datetime
import preprocess

class Tweet:
    clean_text: str
    user: user.User
    id: int
    timestamp: datetime.datetime

    ## TODO: add in fields for QTs, RTs, @s

    def __init__(self, raw_text, user, id, timestamp):
        self.clean_text = preprocess.clean_text(raw_text)
        self.user = user
        self.id = id
        self.timestamp = preprocess.timestamp_to_datetime(timestamp)



