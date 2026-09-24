import re
from datetime import datetime


def parse_whatsapp_file(file_path):
    messages = []

    pattern = re.compile(
        r"\[(\d{2}/\d{2}/\d{4}),\s*(\d{1,2}:\d{2}\s*[AP]M)\]\s*([^:]+):\s*(.*)"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            match = pattern.match(line)

            if not match:
                continue

            date, time, sender, text = match.groups()

            timestamp = datetime.strptime(
                f"{date} {time}",
                "%d/%m/%Y %I:%M %p"
            )

            messages.append({
                "timestamp": timestamp.isoformat(),
                "sender": sender.strip(),
                "text": text.strip()
            })

    return messages