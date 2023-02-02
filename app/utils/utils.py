import json
from datetime import datetime
import os
from pathlib import Path


def to_log(message_="",name_="error"):
    this_folder_path = Path(os.path.dirname(os.path.abspath(__file__)))
    if "log" not in os.listdir(this_folder_path.parent):
        os.mkdir(f"{this_folder_path.parent}/log")

    with open("log/{}.log".format(name_), "a", encoding="utf8") as f:
        if isinstance(message_, dict) or isinstance(message_, list):
          try:
            message_ = json.dump(message_)
          except Exception as e:
             to_log(e)
        log_time = datetime.utcnow()
        f.writelines("{}: {}\n".format(log_time, message_))

def get_list_from_list_by_field(data_=list(), field_='id', value_=""):
    new_list = list()
    if not data_:
      return ["Input error: No data!"]
    if isinstance(value_,list):
      for i in data_:
          if str(i[field_]) in value_:
              new_list.append(i)
      return new_list
    new_list = [i for i in data_ if str(i[field_]) == str(value_)]
    return new_list