import asyncio
import logging

from symbot.chat.message import Message
from symbot.config import *


class Chat:
    """Provides an interface for Twitch chat

    Attributes
    ----------
    reader : StreamReader
        stream to download content from Twitch channel
    writer : StreamWriter
        stream to upload content to Twitch channel
    msg_queue : Queue
        thread safe queue to put downloaded content into
    resp_queue : Queue
        thread safe queue contains content to be uploaded

    Methods
    -------
    open_connection
        open an asyncio connection to a server
    read
        continuously download messages from Twitch channel
    write
        continuously upload messages to Twitch channel
    ping_pong
        handle PINGs from the server
    """

    def __init__(self):
        self.reader = None
        self.writer = None
        # thread safe queue produced here, consumed by control
        self.msg_queue = asyncio.Queue()
        # thread safe queue produced by control, consumed here
        self.resp_queue = None

    async def open_connection(self):
        """open an asyncio connection to a server"""

        # obtain reader, writer streams by connecting to server
        logging.info('connecting to server')
        self.reader, self.writer = await asyncio.open_connection(host=server, port=port)
        # log into channel with credentials
        logging.info('logging in')
        self.writer.write(f'PASS {token}\r\nNICK {nick}\r\nJOIN #{channel}\r\n'.encode('utf-8'))
        await self.writer.drain()
        # drain welcome message from reader
        logging.info('receiving welcome message')
        await self.reader.readuntil(separator='list\r\n'.encode('utf-8'))

    async def read(self):
        """continuously download messages from Twitch channel"""

        # run forever
        logging.info('awaiting messages')
        while True:
            # download message from Twitch channel
            received = (await self.reader.read(n=2048)).strip().decode('utf-8')
            # skip if PING
            if not await self._ping_pong(received):
                # parse message to workable object
                msg = Message(received)
                print(f'{msg.user}: {msg.content}')  # DEBUG
                # put to msg_queue
                # provides to control
                # MAYBE treats every message as command,
                #       because no identifying prefix is used.
                #       Monitor performance and change accordingly
                await self.msg_queue.put(msg)

    async def write(self):
        """continuously upload messages to Twitch channel"""

        # run forever
        while True:
            # wait for responses to send
            # provided by control
            resp = await self.resp_queue.get()
            # upload respond to Twitch channel
            self.writer.write(f'PRIVMSG #{channel} :{resp}\r\n'.encode('utf-8'))
            await self.writer.drain()

    async def _ping_pong(self, received):
        """handle PINGs from the server

        Parameters
        ----------
        received : str
            raw message received from Twitch channel

        Returns
        -------
        bool
            whether message was a PING
        """

        # skip if not PING
        if received.startswith('PING'):
            # respond with PONG
            self.writer.write('PONG\r\n'.encode('utf-8'))
            await self.writer.drain()
            return True
        return False
