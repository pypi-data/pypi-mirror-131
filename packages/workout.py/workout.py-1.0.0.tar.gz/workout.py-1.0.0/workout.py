# pip install pyttsx3 pypiwin32
import pyttsx3
import time

engine = pyttsx3.init()

def announce(name, wait=30):
    print(name)
    engine.say(name)
    engine.runAndWait() 

    time.sleep(wait)

    print('Done')
    engine.say('Done')
    engine.runAndWait()

def main():
    announce('Leg stretches')
    announce('Arm stretches')
    announce('Kettle squats')
    announce('Kettle curls')

if __name__ == '__main__':
    main()

