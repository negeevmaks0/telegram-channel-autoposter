import asyncio
import datetime
import os
from dotenv import load_dotenv

import logging

from telethon import TelegramClient



class AutoPost:
    def __init__(self, schedule, channels):
        load_dotenv()

        self.channels: list[int] | None = channels

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s"
        )
        self.logger = logging.getLogger(__name__)

        self.api_id = int(os.getenv('APP_ID')) # format: *******
        self.api_hash = os.getenv('APP_HASH') # format: ********************************
        self.phone_number = os.getenv('PHONE_NUMBER') # format: +************

        self.schedule: list[tuple[int,int]] = schedule

        with open("post.txt", "r", encoding="utf-8") as f:
            self.post_text = f.read()

        self.logger.info(f"Post text loaded from post.txt ({len(self.post_text)} chars)")

        self.tg_client = TelegramClient('userbot_session', self.api_id, self.api_hash)
        self.tg_client.start(self.phone_number)


    def get_client(self) -> TelegramClient:
        """
        Return the initialized Telegram client instance.

        Returns
        -------
        TelegramClient
            Active Telethon client used for Telegram communication.
        """
        return self.tg_client


    async def get_channels(self) -> list[int]:
        """
        Retrieve IDs of all Telegram channels available in the account dialogs.

        This method scans the user's dialogs and extracts IDs of
        all Telegram channels accessible by the account.

        Returns
        -------
        list[int]
            List of channel IDs.
        """

        dialogs = await self.tg_client.get_dialogs()
        result = []
        
        for dialog in dialogs:
            if dialog.is_channel:
                result.append(dialog.id)

                self.logger.info(f"Channel discovered: {dialog.name} (ID: {dialog.id})")

        return result


    async def main(self):
        """
        Main scheduler loop.

        Continuously checks the system time and compares it with the
        configured schedule. When the time matches, the post from
        'post.txt' is sent to all configured channels.
        """
        if not self.channels:
            self.channels = list(set(await self.get_channels()))


        while True:
            now = datetime.datetime.now()

            for hour, minute in self.schedule:
                if now.hour == hour and now.minute == minute:
                    for channel in self.channels:
                        try:
                            await self.tg_client.send_message(channel, self.post_text)

                            self.logger.info(f"Post sent to channel ID {channel}")

                        except Exception as e:
                            self.logger.error(f"Send error: {e}")

                    await asyncio.sleep(61)

            await asyncio.sleep(20)



if __name__ == '__main__':
    schedule = [(13,57), (14,56), (18,30)]
    channels = [-4705845672]
    # If you do not want to automatically parse channels from the account,
    # manually specify them here ^.

    app = AutoPost(schedule, channels)
    tg_client = app.get_client()

    with tg_client:
        tg_client.loop.run_until_complete(app.main())
