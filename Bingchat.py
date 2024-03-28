import logging
from bing-chat import BingChat

logging.basicConfig(level=logging.INFO)
chat = BingChat("")
initial_message = "Hello, Bing!"
messages = chat.run(initial_message)
print("Chat history:", messages)