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

screen = 1

comm_incoming = False
commsmessage = "..."
comm_cooldown = 0

bananasminute = 250
coolingcores = 0
energyrequest = 0
bananasminute_inputted = 250
coolingcores_inputted = 0
energyrequest_inputted = 0
temperature = 0
kaboom_temperature = 999
production = 0
frequency = 50
kaboom_frequency = 999

time_var = 0 # Midnight, 23:59 is expressed as 1439
inputtimer = 0

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

# Daily energy request curve: (minute of the day, MW). Linear interpolation between points.
# Plant limits: 25-150 MW. With 10 cooling cores the plant stays under 550°C up to ~142 MW.
ENERGY_POINTS = [
    (0, 40),      # 00:00
    (300, 25),    # 05:00 night minimum
    (420, 55),    # 07:00 morning ramp
    (540, 75),    # 09:00
    (660, 90),    # 11:00
    (690, 110),   # 11:30 lunch peak
    (750, 95),    # 12:30
    (900, 85),    # 15:00
    (1080, 100),  # 18:00
    (1260, 135),  # 21:00 evening peak
    (1380, 80),   # 23:00
    (1440, 40),   # 24:00 = 00:00
]

def energy_request(t):
    t = t % 1440
    for (t0, v0), (t1, v1) in zip(ENERGY_POINTS, ENERGY_POINTS[1:]):
        if t0 <= t <= t1:
            return v0 + (v1 - v0) * (t - t0) / (t1 - t0)
    return ENERGY_POINTS[0][1]

def checkComms():
    global temperature
    global frequency

    global comm_incoming
    global commsmessage
    global kaboom_frequency # Kaboom caused by frequency
    global kaboom_temperature # Kaboom caused by temperature
    global comm_cooldown # Communication cooldown

    randomizecooldown = random.randint(1,3)
    if comm_cooldown < randomizecooldown:
        if temperature > 500:
            comm_incoming = True
            comm_cooldown = 20
            if temperature > 550:
                if kaboom_temperature < 30:
                    commsmessage = f"PONCHO I AM SERIOUS YOU HAVE {kaboom_temperature} SECONDS TO COOL THESE BIG THINGS DOWN"
                else:
                    randompick = random.randint(1,5)
                    if randompick == 1:
                        commsmessage = f"PONCHO I AM LITERALLY BURNING ALIVE IN HERE YOU HAVE {kaboom_temperature} SECS UNTIL PERFECTION"
                    elif randompick == 2:
                        commsmessage = f"PONCHO ITS {temperature} DEGREES IN HERE COOL THIS DOWN IN {kaboom_temperature} SECONDS"
                    elif randompick == 3:
                        commsmessage = f"I HOPE YOU LIKE COOKED RATS BECAUSE YOU'RE GOING TO FIND ME COOKED HERE IN {kaboom_temperature} SECONDS"
                    elif randompick == 4:
                        commsmessage = f"PONCHO ANOTHER {kaboom_temperature} AND WE WILL BE COOKED. LITERALLY."
                    elif randompick == 5:
                        commsmessage = "what a cool way to die: burned in a reactor MANAGED BY SOMEONE I SHOULDN'T HAVE GIVEN CONTROL."
            else:
                randompick = random.randint(1,5)
                if randompick == 1:
                    commsmessage = "DONT YOU THINK ITS GETTING A LIL BIT HOT?"
                elif randompick == 2:
                    commsmessage = "AND THEY SAY THAT GLOBAL WARMING IS FICTIONAL. I AM BURNING HERE"
                elif randompick == 3:
                    commsmessage = "THE PLANET IS WARMING UP 30% FASTER BECAUSE OF YOU. LOWER THESE TEMPS!!!"
                elif randompick == 4:
                    commsmessage = "WOW I AM SOOO HOT"
                elif randompick == 5:
                    commsmessage = "WE PLAYING THAT SHOOTING GAME? SUPERHOT???"
        elif frequency > 50.55: # High frequency event
            comm_incoming = True
            comm_cooldown = 20
            randompick = random.randint(1,3)
            if frequency > 51.55:
                if kaboom_frequency < 30:
                    commsmessage = f"PONCHO YOU HAVE {kaboom_frequency} SECONDS TO FIX FREQUENCY HURRY"
                else:
                    randompick = random.randint(1,3)
                    if randompick == 1:
                        commsmessage = f"FREQUENCY IS GETTING OUT OF CONTROL. YOU HAVE {kaboom_frequency} SECONDS TO FIX IT."
                    elif randompick == 2:
                        commsmessage = f"{frequency}Hz?!?!?!? YOU HAVE {kaboom_frequency} SECONDS FOR FIXING OR KABOOOOM!"
                    elif randompick == 3:
                        commsmessage = f"OMG WE GOING TO EXPLODE! YOU HAVE {kaboom_frequency} SECONDS FIX THE FREQUENCY PONCHO!"
            else:
                if randompick == 1:
                    commsmessage = "HEY PONCHO! DON'T YOU THINK FREQUENCY IS A LIL' BIT HIGH?"
                elif randompick == 2:
                    commsmessage = "FREQUENCY IS EXPLODING!!! AND NO I DON'T EXAGGERATE THINGS."
                elif randompick == 3:
                    commsmessage = "WOOOOOO WE'RE SO GREAT WE PRODUCE MORE THAN THE CITY NEEDS. YEA I AM BEING SARCASTIC."
        elif frequency < 49.55:
            comm_incoming = True
            comm_cooldown = 20
            if frequency < 48.55:
                if kaboom_frequency < 30:
                    commsmessage = f"PONCHO YOU HAVE {kaboom_frequency} SECONDS TO FIX FREQUENCY HURRY"
                else:
                    randompick = random.randint(1, 3)
                    if randompick == 1:
                        commsmessage = f"PONCHO WE GOING TO EXPLODE IF YOU DON'T PUSH THAT BANANAS YOU HAVE {kaboom_frequency} SECS"
                    elif randompick == 2:
                        commsmessage = f"YAAAAA THAT'S ADRENALINE ADD MORE BANANAS OR WE EXPLODE IN {kaboom_frequency} SECONDS"
                    elif randompick == 3:
                        commsmessage = f"WE NEED SOOOO MUUCCHH POOOWWWEEERRRR!!!!! OR WE DIE IN {kaboom_frequency} SECONDS "
            else:
                randompick = random.randint(1,3)
                if randompick == 1:
                    commsmessage = "PONCHO YOU NEED TO PRODUCE MORE! WATCH THE FREQUENCY"
                elif randompick == 2:
                    commsmessage = "ADD SOME BANANAS AND WATCH THE FREQUENCY!!!"
                elif randompick == 3:
                    commsmessage = "FREQUENCY IS LOW WE NEED MORE POOOOWEEEEERRRR!!!!"


def calculateData():
    global bananasminute
    global bananasminute_inputted
    global coolingcores
    global coolingcores_inputted
    global production
    global energyrequest
    global energyrequest_inputted
    global temperature
    global frequency

    global time_var
    global inputtimer

    global comm_cooldown
    global kaboom_frequency
    global kaboom_temperature

    # Time calculation (from 0 to 1439)
    if time_var < 1440:
        time_var = time_var + 0.25
    elif time_var == 1440:
        time_var = 0

    # INT - If an input is pending, make the timer tick
    if inputtimer == 0:
        bananasminute = bananasminute_inputted
        coolingcores = coolingcores_inputted
        energyrequest = energyrequest_inputted
    else:
        inputtimer = inputtimer - 0.25

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
    if temperature > 560 and kaboom_temperature == 999:
        kaboom_temperature = 60
    else:
        kaboom_temperature = 999

    # MW - Production value calculation:
    production = bananasminute/10

    # MW - Energy request value calculation:
    energyrequest = round(energy_request(time_var), 1)

    # Hz - Frequency value calculation:
    if bananasminute == 0 or bananasminute < 250:
        frequency = 0
    else:
        imbalance = production - energyrequest
        if imbalance < 0:
            k = 0.08
        else:
            k = 0.04
        target_freq = 50 + imbalance * k
        target_freq = max(45, min(55, target_freq))
        frequency += (target_freq - frequency) / 10
        frequency += random.uniform(-0.02, 0.02)
    if frequency < 48.55 or frequency > 51.55 and kaboom_frequency == 999:
        kaboom_frequency = 60
    else:
        kaboom_frequency = 999

    # Communications producer and timers
    if comm_cooldown > 0:
        comm_cooldown = comm_cooldown - 0.25
    if kaboom_frequency > 0:
        if kaboom_frequency == 999:
            x = 0  # just something to continue
        else:
            kaboom_frequency = kaboom_frequency - 0.25
    if kaboom_temperature > 0:
        if kaboom_temperature == 999:
            x = 0  # just something to continue
        else:
            kaboom_temperature = kaboom_temperature - 0.25
    checkComms()

def menu():
    global bananasminute
    global bananasminute_inputted
    global coolingcores
    global coolingcores_inputted
    global energyrequest
    global energyrequest_inputted
    global inputtimer
    global screen

    if screen == 1:
        print("Placeholder testing menu              Change screens [not yet available]")
        print(" 1. Set bananas/minute                  4. See storage")
        print(" 2. Set cooling cores                   5. See city status")
        print(" 3. Set energy request  ")
    if screen == 2:
        print("Placeholder testing menu              Change screens [not yet available]")
        print(" 1. Set bananas/minute                  4. See storage")
        print(" 2. Set cooling cores                   5. Go back to Control Room")
        print(" 3. Set energy request  ")
    answer = input("Enter the option number: ")
    if answer == "1":
        print("min: 250b/m   |   max:  1500b/m")
        bananasminute_inputted = int(input("Enter number of bananas/minute: "))
        inputtimer = 5
    elif answer == "2":
        print("max: 10    [one cooling core -> 7% cooling]")
        coolingcores_inputted = int(input("Enter number of bananas/minute: "))
        inputtimer = 5
    elif answer == "3":
        print("min: 25MW   max: 150MW |  testing value - the real value will oscillate from 25MW to 150MW") # Se la richiesta è più alta della produzione, la frequenza scende e si verifica un blackout. Se richiesta < produzione di tanto, il giocatore viene penalizzato con un avviso
        energyrequest_inputted = int(input("Enter value of energy request: "))
        inputtimer = 5
    elif answer == "4":
        screen = 2
    elif answer == "5":
        if screen == 1:
            screen = 2
        elif screen == 2:
            screen = 1

DATA_LINES = 12
data_row = 1 # Calculated in main

def gameEmulator():
    global bananasminute
    global coolingcores
    global energyrequest
    global temperature
    global production
    global frequency
    global inputtimer
    global DATA_LINES
    global screen

    global comm_incoming
    global commsmessage
    global comm_cooldown

    print("Placeholder testing game emulator - you can see variables, and monitor code logic.")
    print("")
    if screen == 1:
        print(" Bananas/minute      Cooling cores       Temperature      Energy Request       Production         Frequency                  Time    ")
        print("╒══════════════╕   ╒══════════════╕   ╒══════════════╕   ╒══════════════╕   ╒══════════════╕   ╒══════════════╕            ┌───────┐ ")
        print(f"|{str(bananasminute).center(14)}|   |{str(coolingcores).center(14)}|   |{str(format(temperature, "05.2f")).center(14)}|   |{str(energyrequest).center(14)}|   |{str(production).center(14)}|   |{str(format(frequency, "05.2f")).center(14)}|            |{str(str(format(int(int(time_var)/60), "02.0f"))+":"+str(format(time_var % 60, "02.0f"))).center(7)}|")
        print("╘══════════════╛   ╘══════════════╛   ╘══════════════╛   ╘══════════════╛   ╘══════════════╛   ╘══════════════╛            └───────┘ ")
        if inputtimer > 0:
            print(f"Changes will be applied in {inputtimer:05.2f} seconds...")
        if inputtimer <= 0:
            print("")
        print("")
        print("| Communications and warnings:")
        if comm_cooldown == 10:
            comm_incoming = False
        if comm_incoming:
            print("| Ratticus is sending a communication...")
        else:
            print("| Waiting for communications...")
            commsmessage = "..."
        print("╒═══════════════════════════════════════════════════════════════════════╕")
        print(f"| > {commsmessage.ljust(68)}|")
        print("╘═══════════════════════════════════════════════════════════════════════╛")

    elif screen == 2:
        print(" 1")
        print("┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    ")
        print(f"|{str(format((energyrequest/10), "05.2f")).center(6)}|    |{str(format((energyrequest/10), "05.2f")).center(6)}|    |{str(format((energyrequest/10), "05.2f")).center(6)}|    |{str(format((energyrequest/10), "05.2f")).center(6)}|    |{str(format((energyrequest/10), "05.2f")).center(6)}|    ")
        print("└──────┘    └──────┘    └──────┘    └──────┘    └──────┘    ")

    #print(f"{bananasminute}")
    #print(f"Cooling cores: {coolingcores}")
    #print(f"Temperature: {temperature+0.01:05.2f}")
    #print(f"Energy request: {energyrequest}")
    #print(f"Production: {production}")
    #print(f"Frequency: {frequency:05.2f}")
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