import os, re

class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

formats = [ "MM/DD/YYYY HH:MM",
            "DD/MM/YYYY HH:MM",
            "MM/DD/YYYY HH:MM:SS",
            "DD/MM/YYYY HH:MM:SS"]

def saveFormat(format):
    with open('format.txt', 'w') as f:
        f.write(format)

dtformat = '1'
if os.path.isfile('format.txt'):
    with open('format.txt', 'r') as f:
        dtformat = f.read()

os.system('clear')
print("Welcome to the Clock command line tool!")

running = True
first_time = True

while running:
    print("\nOptions:")
    print("0: Exit")
    print("1: Date & Time Format\n")

    if first_time:
        print("To check the current time in a specific time zone enter the timezone as a UTC offset.")
        print("For example \"UTC-05\" or \"UTC+06\" or \"UTC+00\"\n")
        first_time = False

    user = input("-> ")

    time = re.search(r"UTC[-+][0-9]{2}", user)
    settings = re.search(r"^[0-1]$", user)

    if not time and not settings:
        print(f"\n{tcolors.FAIL}Incorrect input. Please enter the full UTC offset to see the time.")
        print("For example:\n\"UTC-02\"\n\"UTC+04\"")
        print(f"\nOr enter a number from the settings options{tcolors.ENDC}")
    elif time:
        # microservice communication code
        print("\ntime")
    elif settings:
        if user == "0":
            quit()
        elif user == "1":
            while True:
                print("\nPlease select the format you'd like.\n")
                print("0: Cancel")
                for i, x in enumerate(formats):
                    print(f"{i+1}: {x} {'- current' if i+1 == int(dtformat) else ''}")
                print(f"\n{tcolors.WARNING}The formats that include seconds may be inaccurate up to a few seconds.{tcolors.ENDC}")
                new_dtformat = input("\n-> ")

                if re.search(r'[1-4]', new_dtformat) and len(new_dtformat) == 1:
                    saveFormat(new_dtformat)
                    dtformat = new_dtformat
                    print(f"\n{tcolors.OKGREEN}Format saved.")
                    print(f"{formats[int(dtformat)-1]}{tcolors.ENDC}")
                    break
                elif new_dtformat == "0":
                    print("\nOperation cancelled.")
                    break
                else:
                    print(f"\n{tcolors.FAIL}Incorrect input please enter a number from 0 to 4.{tcolors.ENDC}")