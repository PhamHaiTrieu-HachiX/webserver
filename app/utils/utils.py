import json
from datetime import datetime


def to_log(message_="",name_="log"):
    with open("log/{}.log".format(name_), "a", encoding="utf8") as f:
        if isinstance(message_, dict) or isinstance(message_, list):
            message_ = json.dumps(message_)
        log_time = datetime.utcnow()
        f.writelines("{}: {}\n".format(log_time, message_))
        