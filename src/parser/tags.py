import asyncio
import csv
import logging
import re
from datetime import datetime
from pathlib import Path

from telethon import TelegramClient  # type: ignore

from common import TAG_PATTERN, SESSION_NAME, SYSTEM_VERSION

_log = logging.getLogger(__name__)


def get_tags(channel_name: str,
             api_id: int,
             api_hash: str,
             ):
    client = TelegramClient(SESSION_NAME, api_id, api_hash, system_version=SYSTEM_VERSION)
    client.start()

    tags: dict = {}

    async def main():
        channel = await client.get_entity(channel_name)
        messages = await client.get_messages(channel, limit=None)
        for msg in messages:
            if msg.text:
                _log.debug(msg.text)
                matches = re.findall(TAG_PATTERN, msg.text)
                for tag in matches:
                    tags[tag] = tags.get(tag, 0) + 1

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    if not tags:
        _log.warning("No tags collected, csv will not be created")
        return

    _log.debug(tags)
    write_csv(tags)


def write_csv(tags: dict):
    fieldnames = ["Tag", "Amount"]
    timestamp = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
    here = Path(__file__).parents[2].resolve()
    output_folder = here / 'output' / 'tags'
    tags_file = output_folder / f"{timestamp}_tags.csv"
    output_folder.mkdir(exist_ok=True, parents=True)

    with open(tags_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for tag in tags:
            writer.writerow({fieldnames[0]: tag, fieldnames[1]: tags[tag]})
