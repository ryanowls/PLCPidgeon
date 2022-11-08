import sqlite3
import pylogix
import typer
from typing import Tuple, List, Optional    
import json
from rich import print, print_json
import os

app = typer.Typer()

@app.command()
def setipaddress(ip : str):
    """
    Set the IP Address of the PLC to be connected to.
    """
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile) # Reading the file
        jsonfile.close()
    data["ip"] = ip
    with open("config.json", "w") as jsonfile:
        mjson = json.dump(data, jsonfile)
        print("Update IP Successful")
        jsonfile.close()

@app.command()
def showconfig():
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile)
        print_json(data=data)
        jsonfile.close()

@app.command()
def addtag(tag : str):
    """Add a single tag to the list of recorded tags"""
    with open("config.json") as f:
        data = json.load(f)
        f.close()
    if tag in data["tags"]:
        print("[bold red] Tag already included [/bold red]")
        raise typer.Exit()
    else:
        data["tags"].append(tag)
        with open("config.json", "w") as f:
            json.dump(data, f)
            f.close()
        print(":sparkles:[green] Tag Succesfully added [/green] :sparkles:")

@app.command()
def addtags(tags : List[str]):
    """
    Add multiple tags at once.
    
    Enter one after the other with spaces.
    """
    with open("config.json") as f:
        data = json.load(f)
        f.close()
    for t in tags:
        if t not in data["tags"]:
            data["tags"].append(t)
        else:
            print(f"[bold yellow] {t} already included - ignoring. [/bold yellow]")
    with open("config.json", "w") as f:
        json.dump(data, f)
        f.close()
    print(":sparkles:[green] Tag Succesfully added [/green] :sparkles:")

@app.command()
def cleartags():
    """Clears all the existing tags from the list."""
    with open("config.json") as f:
        data = json.load(f)
        f.close()
    data["tags"] = []
    with open("config.json", "w") as f:
        json.dump(data, f)
        f.close()
    print(":sparkles:[green] Tags Succesfully cleared [/green] :sparkles:")

@app.command()
def addTimerTrigger(
    timer : int = typer.Argument(..., min=0),
    seconds : bool = typer.Option(
        True, help = "Timer in seconds"
    ),
    minutes : bool = typer.Option(
        False, help = "Timer in minutes"
    ),
    hours : bool = typer.Option(
        False, help = "Timer in hours"
    )
    ):
    """
    Add a timer for the data to be collected. Default is in seconds. 

    Add a --minutes or --hours tag as needed.

    Values are stored in total seconds in the config.
    """
    if minutes:
        adjusted = timer * 60
    elif hours:
        adjusted = timer * 60 * 60
    else:
        adjusted = timer
    with open("config.json") as f:
        data = json.load(f)
        f.close()
    data["trigger"] = {"time" : adjusted, "value" : None}
    with open("config.json", "w") as f:
        json.dump(data, f)
        f.close()
        print(f":sparkles:[green] Timer for {timer} succesfully added [/green] :sparkles:")

@app.command()
def addValueReqs(req : Optional[List[str]] = typer.Option(None)):
    """
        Allows you to add a value trigger to record data. 

        For example: "temp1 <= 30"

        Must be entered seperated with a --req flag.

        pidgeon addvaluereqs --req "t1 <= 40" --req "pressure >= 100"

        MUST ENTER QUOTES AROUND REQUIREMENTS
    """
    if not req:
        print(f"[bold yellow] You didn't enter any requirements. [/bold yellow]")
        raise typer.Abort()
    with open("config.json") as f:
        data = json.load(f)
        f.close()
    for r in req:
        data["trigger"]["requirements"].append(r)
    with open("config.json", "w") as f:
        json.dump(data, f)
        print(f":sparkles:[green] Requirements added. [/green] :sparkles:")

@app.command()
def clearValueReqs():
    """Clears all the existing requirements"""
    with open("config.json") as f:
        data = json.load(f)
        f.close()
    data["trigger"]["requirements"] = []
    with open("config.json", "w") as f:
        json.dump(data, f)
        f.close()
        print(":sparkles:[green] Requirements Succesfully cleared [/green] :sparkles:")

@app.command()
def clearConfig():
    clearValueReqs()
    cleartags()

@app.command()
def setfilename(name : str):
    """
    Sets the filename. Logs are stored in the rootdirectory log folder.
    
    If you don't set a name, it will default to the "{month}-{date}" at the time of running.
    """
    with open("config.json") as f:
        data = json.load(f)
        f.close()
    data["filename"] = name
    with open("config.json", "w") as f:
        json.dump(data, f)
        f.close()
        print(":sparkles:[green] Filename set. [/green] :sparkles:")

@app.command()
def setup():
    """Walks you through setup without calling individual commands."""
    pass

if __name__ == "__main__":
    app()