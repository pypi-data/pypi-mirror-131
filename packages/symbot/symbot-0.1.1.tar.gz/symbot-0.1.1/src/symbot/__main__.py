import asyncio
import logging
import sys

from symbot.chat.chat import Chat
from symbot.control.control import Control


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s: %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    chat = Chat()
    control = Control()
    control.msg_queue = chat.msg_queue
    chat.resp_queue = control.resp_queue

    await chat.open_connection()
    await asyncio.gather(chat.read(), control.process(), chat.write())


if __name__ == '__main__':
    asyncio.run(main())
