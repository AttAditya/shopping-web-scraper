from os.path import isfile
from flask import Flask
from logging import getLogger, _nameToLevel

def fread(filename: str, *,
    path_prefix: str="web/",
    extension: str=".html",
    replace_format=lambda s: f"[[{s}]]",
    **replace_keywords
) -> str:
    """
    Reads the file
    """

    fpath: str = f"{path_prefix}{filename}{extension}"

    if not isfile(fpath):
        return ""
    
    fdata: str = ""

    with open(fpath, "r") as file:
        fdata = file.read()
        file.close()
    
    for key in replace_keywords:
        fdata = fdata.replace(
            replace_format(key),
            replace_keywords[key]
        )

    return fdata

getLogger("werkzeug").setLevel(_nameToLevel["WARNING"])

app = Flask(
    "Scrape Backend",
    static_folder="resources",
    static_url_path="/resources"
)

@app.route("/")
def home() -> str:
    """
    Home Page
    """

    return fread("index")

