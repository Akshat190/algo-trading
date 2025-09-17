# websocket Programming Testing

from SharekhanApi.sharekhanWebsocket import SharekhanWebSocket
import csv
import os
from datetime import datetime

# Prompt for access token at runtime to avoid editing the file
try:
    user_token = input("Enter your Sharekhan access token: ").strip()
except Exception:
    user_token = ""

if not user_token:
    print("No access token provided. Exiting.")
    raise SystemExit(1)

sws = SharekhanWebSocket(user_token)

# CSV setup
csv_filename = os.path.join(os.getcwd(), f"ticks_{datetime.now().strftime('%Y%m%d')}.csv")
_csv_file = None
_csv_writer = None


def ensure_csv():
    global _csv_file, _csv_writer
    if _csv_file is None:
        exists = os.path.exists(csv_filename)
        _csv_file = open(csv_filename, mode="a", newline="", encoding="utf-8")
        _csv_writer = csv.writer(_csv_file)
        if not exists:
            _csv_writer.writerow(["timestamp", "message"])  # simple schema; raw message per line


def on_data(wsapp, message):
    print("Ticks: {}".format(message))
    try:
        ensure_csv()
        _csv_writer.writerow([datetime.now().isoformat(timespec="seconds"), message])
        _csv_file.flush()
    except Exception as e:
        print(f"CSV write error: {e}")


def on_open(wsapp):
    print("on open")
    # Example feed usage (uncomment and adjust as needed):
    # token_list = {"action": "subscribe", "key": ["feed"], "value": [""]}
    # feed = {"action":"feed","key":["ltp"],"value":["NC22,NF37833,NF37834,MX253461,RN7719"]}
    # sws.subscribe(token_list)
    # sws.fetchData(feed)


def on_error(wsapp, error):
    print(error)


def on_close(wsapp):
    print("Close")
    try:
        if _csv_file:
            _csv_file.close()
    except Exception:
        pass


# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close

sws.connect()