from os import environ
import datetime 

def get_env(name) -> str | None:
    return environ.get(name)

def str_date_to_python(date) -> datetime.date:
    return datetime.datetime.strptime(date, "%m/%d/%Y").date()
