'''Develop a chatbot equipped with sentiment analysis capabilities. The chatbot will analyze the sentiment of the user's input. The sentiment analysis component will determine whether the user's message expresses a positive, negative, or neutral sentiment.
This project combines natural language processing (NLP) techniques, To Find the Sentiment Of User. '''

import nltk
from textblob import TextBlob
import sys
import random
import langdetect
from langdetect import detect
import json
from datetime import datetime

# Ensure Python 3.12 or later
if sys.version_info < (3, 12):
    print("Error: This code requires Python 3.12 or later.")
    sys.exit(1)

# Print Python version and compatibility status
print(f"Running on Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
if sys.version_info >= (3, 12):
    print("This version is compatible and supported.")

# Ensure NLTK punkt tokenizer is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except Exception as e:
        print(f"Error: Failed to download NLTK 'punkt' tokenizer: {e}")
        sys.exit(1)

CHAT_HISTORY_FILE = "chat_history.json"

class Chatbot:
    def __init__(self):
        self.greetings = ["hello", "hi", "hey", "greetings", "sup", "what's up"]
        self.goodbyes = ["bye", "goodbye", "see you", "take care", "farewell"]
        self.bot_name = "ChatBot"
        # Lists of varied responses for each sentiment
        self.positive_responses = [
            "That's awesome to hear!",
            "Wow, you're in great spirits!",
            "Love the positive vibes!",
            "That's so cool, keep it up!",
            "You're radiating positivity!"
        ]
        self.negative_responses = [
            "Oh, I'm sorry you're feeling down. Want to share more?",
            "That sounds tough. I'm here if you need to talk!",
            "Sorry to hear that. Can I help cheer you up?",
            "Ouch, that doesn't sound fun. Want to discuss it?",
            "I'm here for you—let's talk about what's going on."
        ]
        self.neutral_responses = [
            "Got it, keeping things chill!",
            "Alright, nice and neutral!",
            "Cool, just cruising along!",
            "Keeping it steady, I see!",
            "All good, what's next?"
        ]
        # Initialize JSON file
        self._initialize_json_file()

    def _initialize_json_file(self):
        try:
            with open(CHAT_HISTORY_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        except Exception as e:
            print(f"Error initializing JSON file: {e}")
            return []

    def _save_interaction(self, user_input, sentiment, polarity, subjectivity, response):
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "sentiment": sentiment,
            "polarity": polarity,
            "subjectivity": subjectivity,
            "response": response
        }
        history = self._initialize_json_file()
        history.append(interaction)
        try:
            with open(CHAT_HISTORY_FILE, 'w') as f:
                json.dump(history, f, indent=4)
        except Exception as e:
            print(f"Error saving to JSON file: {e}")

    def get_sentiment(self, text):
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            if polarity > 0:
                sentiment = "positive"
            elif polarity < 0:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            return sentiment, polarity, subjectivity
        except Exception as e:
            return "error", 0, 0 

    def chat(self):
        print(f"{self.bot_name}: Hi! I am your chatbot. How can I help you? (Please use English for best results)")
        while True:
            try:
                user_input = input("You: ").strip().lower()

                if not user_input:
                    response = "Please say something!"
                    print(f"{self.bot_name}: {response}")
                    self._save_interaction(user_input, "error", 0, 0, response)
                    continue

                if user_input in self.goodbyes:
                    response = "Goodbye!"
                    print(f"{self.bot_name}: {response}")
                    self._save_interaction(user_input, "neutral", 0, 0, response)
                    break

                if user_input in self.greetings:
                    response = "Hello! How can I assist you?"
                    print(f"{self.bot_name}: {response}")
                    self._save_interaction(user_input, "neutral", 0, 0, response)
                    continue

                # Check for non-English input
                try:
                    if detect(user_input) != 'en':
                        non_english_warning = "I work best with English input. Results may be less accurate for other languages."
                        print(f"{self.bot_name}: {non_english_warning}")
                except langdetect.lang_detect_exception.LangDetectException:
                    non_english_warning = ""
                    pass  # Ignore detection errors for short or ambiguous text

                sentiment, polarity, subjectivity = self.get_sentiment(user_input)

                if sentiment == "error":
                    response = "Sorry, I couldn't analyze that input."
                    print(f"{self.bot_name}: {response}")
                    self._save_interaction(user_input, sentiment, polarity, subjectivity, response)
                else:
                    sentiment_message = f"You expressed a {sentiment} sentiment."
                    metrics_message = f"Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f}"
                    varied_response = random.choice(
                        self.positive_responses if sentiment == "positive" else
                        self.negative_responses if sentiment == "negative" else
                        self.neutral_responses
                    )
                    print(f"{self.bot_name}: {sentiment_message}")
                    print(f"{self.bot_name}: {metrics_message}")
                    print(f"{self.bot_name}: {varied_response}")
                    response = f"{non_english_warning}\n{sentiment_message}\n{metrics_message}\n{varied_response}".strip()
                    self._save_interaction(user_input, sentiment, polarity, subjectivity, response)

            except KeyboardInterrupt:
                response = "Goodbye!"
                print(f"\n{self.bot_name}: {response}")
                self._save_interaction("", "neutral", 0, 0, response)
                break
            except Exception as e:
                response = "Oops, something went wrong. Please try again."
                print(f"{self.bot_name}: {response}")
                self._save_interaction(user_input if 'user_input' in locals() else "", "error", 0, 0, response)

if __name__ == "__main__":
    try:
        chatbot = Chatbot()
        chatbot.chat()
    except ImportError as e:
        print("Error: Please ensure the latest 'nltk', 'textblob', and 'langdetect' are installed. Run:")
        print("pip install --upgrade nltk textblob langdetect")
        sys.exit(1)
