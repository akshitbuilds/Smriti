from parser import parse_whatsapp_file
from database import create_database, save_messages


file_path = "../data/demo_chat.txt"

create_database()

messages = parse_whatsapp_file(file_path)

save_messages(messages)

print(f"Imported {len(messages)} messages successfully.")
print("Messages saved to SQLite.")