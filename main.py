import time
import os
import webbrowser
import webhandler
import pyfiglet
import random
import sys
import io
import threading
from contextlib import redirect_stdout
pyfigure = ""
os.system('')

bananasminute = 250
coolingcores = 0
energyrequest = 0
temperature = 0
production = 0
frequency = 50

def clear():
    global pyfigure

    os.system('cls' if os.name == 'nt' else 'clear')
    print(pyfigure)

def open_narrative(page, port):
    webhandler.page_closed = False

    webbrowser.open(f"http://127.0.0.1:{port}/{page}")

    print("Close page to continue the game...")
    while not webhandler.page_closed:
        time.sleep(1)

    print("Pagina chiusa! Il gioco riprende.")

def calculateData():
    global bananasminute
    global coolingcores
    global production
    global energyrequest
    global temperature
    global frequency

    # °C - Temperature calculation:
    if not 250 <= bananasminute <= 1500 :
        raise SystemExit(f'Bananas/minute value not in range. {bananasminute}: should be from 250 to 1500.')
    elif bananasminute < 1250:
        target = (bananasminute / 200) * 192
        target = (target / 100) * (100 - (7 * coolingcores))
        if temperature != target :
            raiseby = (target-temperature)/10
            temperature = temperature + raiseby
    else:
        target = (bananasminute / 150) * 192
        target = (target / 100) * (100 - (7 * coolingcores))
        if temperature != target:
            raiseby = (target - temperature) / 10
            temperature = temperature + raiseby

    # MW - Production value calculation:
    production = bananasminute/10

    # Hz - Frequency value calculation:
    imbalance = production - energyrequest
    if imbalance < 0:
        k = 0.08
    else:
        k = 0.04
    target_freq = 50 + imbalance * k
    target_freq = max(45, min(55, target_freq))
    frequency += (target_freq - frequency) / 10
    frequency += random.uniform(-0.02, 0.02)
def menu():
    global bananasminute
    global coolingcores
    global energyrequest
    print("")
    print("Placeholder testing menu")
    print(" 1. Set bananas/minute  ")
    print(" 2. Set cooling cores   ")
    print(" 3. Set energy request  ")
    answer = input("Enter the option number: ")
    if answer == "1":
        print("min: 250b/m   |   max:  1500b/m")
        bananasminute = int(input("Enter number of bananas/minute: "))
    elif answer == "2":
        print("max: 10    [one cooling core -> 7% cooling]")
        coolingcores = int(input("Enter number of bananas/minute: "))
    elif answer == "3":
        print("min: 25MW   max: 150MW |  testing value - the real value will oscillate from 25MW to 150MW") # Se la richiesta è più alta della produzione, la frequenza scende e si verifica un blackout. Se richiesta < produzione di tanto, il giocatore viene penalizzato con un avviso
        energyrequest = int(input("Enter value of energy request: "))

def gameEmulator():
    global bananasminute
    global coolingcores
    global energyrequest
    global temperature
    global production
    global frequency

    print("Placeholder testing game emulator - you can see variables, and monitor code logic.")
    print("")
    print(" Bananas/minute      Cooling cores       Temperature      Energy Request       Production          Frequency   ")
    print("╒══════════════╕   ╒══════════════╕   ╒══════════════╕   ╒══════════════╕   ╒══════════════╕   ╒══════════════╕")
    print(f"|{str(bananasminute).center(14)}|   |{str(coolingcores).center(14)}|   |{str(format(temperature, "05.2f")).center(14)}|   |{str(energyrequest).center(14)}|   |{str(production).center(14)}|   |{str(format(frequency, "05.2f")).center(14)}|")
    print("╘══════════════╛   ╘══════════════╛   ╘══════════════╛   ╘══════════════╛   ╘══════════════╛   ╘══════════════╛   ")
    #print(f"{bananasminute}")
    #print(f"Cooling cores: {coolingcores}")
    #print(f"Temperature: {temperature+0.01:05.2f}")
    #print(f"Energy request: {energyrequest}")
    #print(f"Production: {production}")
    #print(f"Frequency: {frequency:05.2f}")

DATA_LINES = 6
data_row = 1 # Calculated in main

def draw_loop():
    while True:
        calculateData()

        buf = io.StringIO()
        with redirect_stdout(buf):
            gameEmulator()
        text = buf.getvalue().replace("\n", "\033[K\n")

        sys.stdout.write(f"\033[s\033[{data_row};1H{text}\033[u")
        sys.stdout.flush()
        time.sleep(0.25)

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    webhandler.webStarter()
    time.sleep(2)
    clear()
    pyfigure = pyfiglet.figlet_format("Ratticus Power Plant")
    input("Press ENTER to start your journey...")
    # open_narrative("", webhandler.port)
    clear()
    data_row = pyfigure.count("\n") + 2
    menu_row = data_row + DATA_LINES + 1
    threading.Thread(target=draw_loop, daemon=True).start()

    while True:
        sys.stdout.write(f"\033[{menu_row};1H\033[J")
        sys.stdout.flush()
        menu()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/