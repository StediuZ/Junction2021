from datetime import datetime

class TimeNow():
    def __repr__(self):
        now = datetime.now()
        return now.strftime("%H:%M:%S")
