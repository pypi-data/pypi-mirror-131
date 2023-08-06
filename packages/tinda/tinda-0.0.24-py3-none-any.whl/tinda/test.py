

test_json = {"intents": [
        {"tag": "greetings",
        "patterns": ["hi"," greetings", "hello", "hey there", "hey", "hi there", "hiya", "how are ya", "how ya doin", "how are you", "sup", "howdy","yo", "how are things", "good day", "how's it going" ],
        "responses": ["Hi", "Greetings", "Hello", "Hey there", "Hey", "Hi there", "Hiya", "How are you?", "What can i do for you?", "How can i help?", "How you doing?", "Howdy", "Yo!"],
        "context": ["someone trying to greet, to initiate conversation or maybe no reason"]
        },
        {"tag": "goodbye",
        "patterns": ["Bye", "See you later", "Goodbye", "Nice chatting to you, bye", "Till next time"],
        "responses": ["See you!", "Have a nice day", "Bye! Come back again soon."],
        "context": ["saying bye as a parting tradition"]
        },
        {"tag": "cat",
        "patterns":["Cat", "Cat you there", "hey cat", "cat whats up"],
        "responses":["Hey Boss", "I'm here", "Hows it going?", "How can i help?", "What can i do for you?", "What's on your mind"],
        "context":["trying to access cat"]
        },
        {"tag": "time",
        "patterns":["what time is it", "what time of the day", "what time", "time of the day", "current time"],
        "responses":[],
        "context":[]
        },
        {"tag": "date",
        "patterns":["what date is it", "date today", "what date", "date if the month", "current date"],
        "responses":[],
        "context":[]
        }
        ]}

