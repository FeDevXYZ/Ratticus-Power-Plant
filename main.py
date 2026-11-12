import time
import os
import webbrowser
import webhandler
import pyfiglet
import random

bananasminute = 0
coolingcores = 0
energyrequest = 0
temperature = 0
production = 0
frequency = 50

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        temperature = (bananasminute/200)*192
        temperature = (temperature / 100)*(100-(7 * coolingcores))
    elif bananasminute > 1250:
        temperature = (bananasminute/150)*192
        temperature = (temperature/100)*(100-(7*coolingcores))

    # MW - Production value calculation:
    production = bananasminute/10

    # Hz - Frequency value calculation:
    if production > energyrequest:
        a = production - energyrequest
        frequency = 50 + (random.uniform(0.1, 0.8) * a)
    elif production < energyrequest:
        a = energyrequest - production
        frequency = 50 + (random.uniform(0.1, 0.8) * a)
def menu():
    global bananasminute
    global coolingcores
    global energyrequest

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
    calculateData()
def gameEmulator():
    global bananasminute
    global coolingcores
    global energyrequest
    global temperature
    global production
    global frequency

    print("Placeholder testing game emulator - you can see variables, and monitor code logic.")
    print(f"Bananas per minute: {bananasminute}")
    print(f"Cooling cores: {coolingcores}")
    print(f"Temperature: {temperature}")
    print(f"Energy request: {energyrequest}")
    print(f"Production: {production}")
    print(f"Frequency: {frequency:05.2f}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    webhandler.webStarter()
    time.sleep(2)
    clear()
    input("Press ENTER to start your journey...")
    # open_narrative("", webhandler.port)
    clear()
    result = pyfiglet.figlet_format("Ratticus Power Plant")
    print(result)
    while True:
        menu()
        clear()
        gameEmulator()
    print("")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/