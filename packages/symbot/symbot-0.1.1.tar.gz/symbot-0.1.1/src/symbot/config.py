from os.path import join, dirname, abspath


# directories
data_path = join(dirname(abspath(__file__)), 'data')
dev_path = join(dirname(abspath(__file__)), 'dev')

# server connection
server = 'irc.chat.twitch.tv'
port = 6667

# connection credentials
# get your token on https://twitchapps.com/tmi/
channel = 'broadcaster username'
nick = 'bot username'
token = 'oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
