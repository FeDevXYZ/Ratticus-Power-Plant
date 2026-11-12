import socket
import threading
import errno
from flask import Flask, render_template
app = Flask(__name__)

page_closed = False
port = 5000
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/closed", methods=["POST"])
def closed():
    global page_closed
    page_closed = True
    return "OK"


def webStarter():
    global port
    while port <= 65535:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(("127.0.0.1", port))
            break
        except OSError as error:
            if error.errno != errno.EADDRINUSE and getattr(error, "winerror", None) != 10048:
                raise
            print(f"La porta {port} è occupata, provo la {port + 1}...")
            port += 1
    else:
        raise RuntimeError("Nessuna porta disponibile.")

    threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False),
        daemon=True
    ).start()