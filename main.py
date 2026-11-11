from flask import Flask, render_template
import time
import threading
import os

app = Flask(__name__)

page_closed = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/closed", methods=["POST"])
def closed():
    global page_closed
    page_closed = True
    return "OK"


def open_narrative(page):
    global page_closed
    page_closed = False

    import webbrowser
    webbrowser.open(f"http://127.0.0.1:5000/{page}")

    print("Aspetto che il giocatore chiuda la pagina...")

    while not page_closed:
        time.sleep(1)

    print("Pagina chiusa! Il gioco riprende.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    threading.Thread(
        target=lambda: app.run(debug=False, use_reloader=False),
        daemon=True
    ).start()
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    input("Premi INVIO per aprire Ratticus...")

    open_narrative("")

    print("GIOCO RIPRESO!")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
