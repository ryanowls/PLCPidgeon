import os, csv, datetime
import os.path
import json
from pylogix import PLC
import time, threading

def logtask():
    with open("config.json", "r") as jsonfile:
        data = json.load(jsonfile) # Reading the file
        jsonfile.close()
    try:
        while True:
            log()
            time.sleep(data['trigger']['time'])
    except KeyboardInterrupt:
        print("Exited Successfully")

def log():
    dt = datetime.datetime.now()
    with PLC("10.0.0.100") as comm:
        with open("config.json", "r") as jsonfile:
            data = json.load(jsonfile) # Reading the file
            jsonfile.close()
        current_time_string = dt.strftime("%H:%M:%S")
        headers = ["time"] + data["tags"]
        trigger_type = data["trigger"]
        if trigger_type["requirements"] == None:
            file_path = data["filename"]
            if file_path == "":
                file_path = f"{dt.month}-{dt.day}"
            with open(file_path + ".csv", "a") as csvfile:
                file_is_empty = os.stat(file_path + ".csv").st_size  == 0
                csvwriter = csv.DictWriter(csvfile, fieldnames = headers, lineterminator='\n')
                if file_is_empty:
                    csvwriter.writeheader()
                row = {}
                row["time"] = current_time_string
                for tag in data["tags"]:
                    val = comm.Read(tag)
                    row[tag] = val
                print(row)
                csvwriter.writerow(row)
        else:
            compare_string = trigger_type["requirements"]
            tag, req, value = compare_string.split()
            tag_data = comm.Read(tag)
            requirements_met = eval(f"{tag_data} {req} {value}")
            if requirements_met:
                file_path = data["filename"]
                if file_path == "":
                    file_path = f"{dt.month}-{dt.day}"
                with open(file_path + ".csv", "a") as csvfile:
                    file_is_empty = os.stat(file_path).st_size  == 0
                    csvwriter = csv.DictWriter(csvfile, fieldnames = headers, lineterminator='\n')
                    if file_is_empty:
                        csvwriter.writeheader()
                    row = {}
                    row["time"] = current_time_string
                    for tag in data["tags"]:
                        val = comm.Read(tag)
                        row[tag] = val
                    csvwriter.writerow(row)

