from ollama import chat


messages = """
[12/08/2026, 10:32 AM] Rohan: Poster kal tak bhej dunga, pakka.
[12/08/2026, 10:35 AM] Priya: Venue confirm hua kya?
[12/08/2026, 10:40 AM] Akash: Auditorium available hai 28 August ko.
[18/08/2026, 09:15 AM] Priya: Guys auditorium already booked on 28th.
[18/08/2026, 09:20 AM] Rohan: Okay let's shift to Hall B.
[18/08/2026, 09:22 AM] Priya: Done. Hall B final.
[19/08/2026, 11:00 AM] Rohan: Poster kal tak bhej dunga.
[21/08/2026, 09:00 AM] Priya: Rohan poster ka kya hua?
[21/08/2026, 09:05 AM] Rohan: Aaj raat tak bhej dunga.
[22/08/2026, 06:30 PM] Akash: Sponsorship deck Friday tak complete karunga.
[23/08/2026, 10:00 AM] Priya: Sponsorship deck Friday tak ready hona chahiye.
"""


prompt = f"""
You are Smriti, a private team-memory assistant.

Analyze the following WhatsApp conversation.

Find:
1. commitments
2. deadlines
3. decisions
4. changed decisions
5. overdue commitments

Conversation:

{messages}

Give a short structured answer.
"""


response = chat(
    model="qwen3:4b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(response.message.content)