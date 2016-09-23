import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
import socket
import re
import time

CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

s = socket.socket()
s.connect((config.HOST, config.PORT))
s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(config.CHANNEL).encode("utf-8"))

def chat(sock, msg):
    sock.send("PRIVMSG {} :{}\r\n".format(config.CHANNEL, msg).encode("utf-8"))

def ban(sock, user):
    chat(sock, ".ban {}".format(user))

def timeout(sock, user, sec=600):
    chat(sock, ".timeout {} {}".format(user, sec))

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        username = re.search(r"\w+", response).group(0)
        message = CHAT_MSG.sub("", response)
        print(username + ": " + message)
        if message.strip() == "!timeout":
            print("timing out user " + username)
            timeout(s, username, 10)
    time.sleep(0.1)
