import asyncio
import csv
import logging
import re
from datetime import datetime, date, timezone
from pathlib import Path

from telethon import TelegramClient  # type: ignore

from common import TAG_PATTERN, SESSION_NAME, SYSTEM_VERSION

DATE = "Date"
MESSAGE = "Message"

_log = logging.getLogger(__name__)


def get_messages(tags: str,
                 start: str,
                 end: str,
                 api_id: int,
                 api_hash: str,
                 channel_name: str,
                 ):
    needed_tag_list, start_date, end_date = normalize_input(tags=tags, start=start, end=end)
    _log.debug("Normalized data: list - %s, start - %s, end - %s", needed_tag_list, start_date, end_date)

    client = TelegramClient(SESSION_NAME, api_id, api_hash, system_version=SYSTEM_VERSION)
    client.start()

    collected_data = []

    async def main():
        reverse = False
        offset_date = None
        if start_date:
            reverse = True
            offset_date = start_date
        elif end_date:
            offset_date = end_date

        chat = await client.get_input_entity(channel_name)

        async for msg in client.iter_messages(chat, reverse=reverse, offset_date=offset_date):
            if end_date and msg.date > datetime(end_date.year, end_date.month, end_date.day, tzinfo=timezone.utc):
                break
            if needed_tag_list and msg.text:
                re_matches = re.findall(TAG_PATTERN, msg.text)
                if not bool(set(re_matches) & set(needed_tag_list)):
                    _log.debug("%s doesn't contain needed tags", msg.text)
                    continue

            if msg.text:
                _log.debug("%s ----- %s", msg.date, msg.text)
                collected_data.append({MESSAGE: msg.text, DATE: msg.date})

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    if not collected_data:
        _log.warning("No messages collected, csv will not be created")
        return

    _log.debug(collected_data)
    write_csv(collected_data)


def normalize_input(tags: str, start: str, end: str) -> tuple[tuple | list | None, date | None, date | None]:
    if tags:
        needed_tag_list = [x.strip().lstrip('#') for x in tags.split(',')]
    else:
        needed_tag_list = None
    if start:
        split_start_date = [int(x) for x in start.split('/')]
        start_date = date(split_start_date[2], split_start_date[1], split_start_date[0])
    else:
        start_date = None
    if end:
        split_end_date = [int(x) for x in end.split('/')]
        end_date = date(split_end_date[2], split_end_date[1], split_end_date[0])
    else:
        end_date = None
    return needed_tag_list, start_date, end_date


def write_csv(collected_data: list):
    fieldnames = [DATE, MESSAGE, "Tags"]
    timestamp = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
    here = Path(__file__).parents[2].resolve()
    output_folder = here / 'output' / 'messages'
    tags_file = output_folder / f"{timestamp}_messages.csv"
    output_folder.mkdir(exist_ok=True, parents=True)

    with open(tags_file, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for msg in collected_data:
            if msg[MESSAGE]:
                matches = re.findall(TAG_PATTERN, msg[MESSAGE])
                writer.writerow({fieldnames[0]: msg[DATE],
                                 fieldnames[1]: msg[MESSAGE],
                                 fieldnames[2]: '; '.join(matches)})
