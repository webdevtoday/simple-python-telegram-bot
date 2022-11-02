# Description

Instructions for installing a Python bot on Ubuntu 18

# Instruction

Run in the server console on first startup:
```
sudo apt update
```
```
sudo apt install -y htop git build-essential libssl-dev libffi-dev python3-pip python3-dev python3-setuptools
```

Create user:
```
adduser user
```

Switch to new user:
```
whoami
```
```
su - user
```
```
whoami
```

Clone repository
```
cd /home/user
```
```
git clone https://github.com/webdevtoday/simple-python-telegram-bot.git
```

Create a virtual environment
```
cd /home/user/simple-python-telegram-bot
```
```
python3 -m venv .venv
```

Activate virtual environment and install packages
```
source /home/user/simple-python-telegram-bot/.venv/bin/activate
```
```
pip install -r /home/user/simple-python-telegram-bot/pip-requirements.txt
```

Check if the bot is working (from the virtual environment):
```
/home/user/simple-python-telegram-bot/.venv/bin/python /home/user/simple-python-telegram-bot/ubuntu18/main.py
```
