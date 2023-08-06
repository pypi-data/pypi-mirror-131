import subprocess

class colors():
    reset = "\033[0m"
    Y = "\033[33m"

def main():
    print("""****************************************************************************
    |    DEVELOPED by  Mauricio Rossi                     CopyrightⒸ 2021      |
    ****************************************************************************
    __________ 
    /    ___   \            (_)
    |   |   |   |   __    __ __ ___    ___ ________ ________     ____
    |   |   |   |  |  |  |  |  |   \  /   |  ______|   ___  \   /    \ 
    |   |   |   |  |  |  |  |  |    \/    |  __|   |  |___|  | /  /\  \ 
    |   |___|   |__|  |__|  |  |  |\__/|  |  |_____|   __   / /  /__\  \ 
    \______________|________|__|__|    |__|________|__|  \__\/__/    \__\  v1.0
    ****************************************************************************
    |     Whatsapp: (+598) 94 860 590          Email: mrossiph@gmail.com       |
    ****************************************************************************""")
    print(""" Quimera is a Tool Kit of Python scripts for Pentesting, Ethical Hacking and OSINT\n""")

    print("""[+] Select the tool you want to use
        """+colors.Y+"""### WiFi Tools ###"""+colors.reset+"""
        1 WiFi Password Retriever
        2 WiFi MAC Blocker
        
        """+colors.Y+"""### MAC Address Tools ###"""+colors.reset+"""
        3 MAC Changer
        
        """+colors.Y+"""### OSINT Tools ###"""+colors.reset+"""
        4 OSINT""")
    print("\n")
    num = input(str('Option Number > '))
    optionsList = ['1', '2', '3']

    def openOption(num):
        fileIndex = int(num) - 1 
        fileList = ['WiFiPasswords', 'WiFiDOSAttack', 'MacChanger']
        file = fileList[fileIndex]+'.py'
        op1 = subprocess.call(["python", file])
        return op1

    if num in optionsList:
        openOption(num)
    else:
        print("Esa Opcion no es valida")