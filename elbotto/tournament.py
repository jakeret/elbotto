import threading

from elbotto import launcher



def start_bots():
    threading.Thread(target=launcher.launch).start()
    threading.Thread(target=launcher.launch).start()
    threading.Thread(target=launcher.launch, kwargs={"bot_name": "Dude"} ).start()
    t = threading.Thread(target=launcher.launch, kwargs={"bot_name": "Dude"} )
    t.start()
    t.join()


if __name__ == '__main__':
    start_bots()