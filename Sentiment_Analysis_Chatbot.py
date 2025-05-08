'''Develop a chatbot equipped with sentiment analysis capabilities. The chatbot will analyze the sentiment of the user's input. The sentiment analysis component will determine whether the user's message expresses a positive, negative, or neutral sentiment.
This project combines natural language processing (NLP) techniques, To Find the Sentiment Of User. '''

import os
import nltk
from textblob import TextBlob
import sys
import random
import logging
import langdetect
from langdetect import detect
import json
from datetime import datetime

# Get the directory where the current .py file is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up logging to store log file in the same directory as the .py file
LOG_FILE = os.path.join(SCRIPT_DIR, 'Sentiment_Analysis.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def log_and_print(message, level='info'):
    print(message)
    if level == 'info':
        logging.info(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'warning':
        logging.warning(message)

# Print Python version and compatibility status
log_and_print(f"Running on Python [ {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} ]")
if sys.version_info >= (3, 12):
    log_and_print("     - This version is compatible and supported for the execution of the code.")
else:
    log_and_print("Error: ")
    log_and_print(f"    - The version [ {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} ] is not compatible and not supported for the execution of the code.")
    log_and_print("    - This code requires Python [ 3.12 ] or later versions.")
    sys.exit(1)

# Ensure NLTK punkt tokenizer is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
        logging.info("Downloaded NLTK 'punkt' tokenizer.")
    except Exception as e:
        logging.error(f"Error: Failed to download NLTK 'punkt' tokenizer: {e}")
        sys.exit(1)

CHAT_HISTORY_FILE = os.path.join(SCRIPT_DIR, "Sentiment_Analysis_Chat.json")

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
            "I'm here for you-let's talk about what's going on."
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
        logging.info("Chatbot initialized.")

    def _initialize_json_file(self):
        try:
            with open(CHAT_HISTORY_FILE, 'r') as f:
                logging.info(f"Loaded chat history from {CHAT_HISTORY_FILE}.")
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning(f"{CHAT_HISTORY_FILE} not found or empty. Starting new chat history.")
            return []
        except Exception as e:
            logging.error(f"Error initializing JSON file: {e}")
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
            logging.info(f"Saved interaction to {CHAT_HISTORY_FILE}: {interaction}")
        except Exception as e:
            logging.error(f"Error saving to JSON file: {e}")

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
            logging.info(f"Sentiment analysis for input: '{text}' | Sentiment: {sentiment}, Polarity: {polarity}, Subjectivity: {subjectivity}")
            return sentiment, polarity, subjectivity
        except Exception as e:
            logging.error(f"Error during sentiment analysis: {e}")
            return "error", 0, 0 

    def chat(self):
        log_and_print(f"{self.bot_name}: Hi! I am your chatbot. How can I help you? (Please use English for best results)")
        logging.info("Chat session started.")
        while True:
            try:
                user_input = input("You: ").strip().lower()
                logging.info(f"User input: {user_input}")

                if not user_input:
                    response = "Please say something!"
                    log_and_print(f"{self.bot_name}: {response}")
                    self._save_interaction(user_input, "error", 0, 0, response)
                    continue

                if user_input in self.goodbyes:
                    response = "Goodbye!"
                    log_and_print(f"{self.bot_name}: {response}")
                    self._save_interaction(user_input, "neutral", 0, 0, response)
                    logging.info("User ended chat with a goodbye.")
                    break

                if user_input in self.greetings:
                    response = "Hello! How can I assist you?"
                    log_and_print(f"{self.bot_name}: {response}")
                    self._save_interaction(user_input, "neutral", 0, 0, response)
                    continue

                # Check for non-English input
                non_english_warning = ""
                try:
                    if detect(user_input) != 'en':
                        non_english_warning = "I work best with English input. Results may be less accurate for other languages."
                        log_and_print(f"{self.bot_name}: {non_english_warning}", 'warning')
                        logging.warning(f"Non-English input detected: {user_input}")
                except langdetect.lang_detect_exception.LangDetectException:
                    non_english_warning = ""
                    logging.warning("Language detection failed (possibly due to short or ambiguous input).")

                sentiment, polarity, subjectivity = self.get_sentiment(user_input)

                if sentiment == "error":
                    response = "Sorry, I couldn't analyze that input."
                    log_and_print(f"{self.bot_name}: {response}", 'error')
                    self._save_interaction(user_input, sentiment, polarity, subjectivity, response)
                else:
                    sentiment_message = f"You expressed a {sentiment} sentiment."
                    metrics_message = f"Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f}"
                    varied_response = random.choice(
                        self.positive_responses if sentiment == "positive" else
                        self.negative_responses if sentiment == "negative" else
                        self.neutral_responses
                    )
                    log_and_print(f"{self.bot_name}: {sentiment_message}")
                    log_and_print(f"{self.bot_name}: {metrics_message}")
                    log_and_print(f"{self.bot_name}: {varied_response}")
                    response = f"{non_english_warning}\n{sentiment_message}\n{metrics_message}\n{varied_response}".strip()
                    self._save_interaction(user_input, sentiment, polarity, subjectivity, response)

            except KeyboardInterrupt:
                response = "Goodbye!"
                log_and_print(f"\n{self.bot_name}: {response}")
                self._save_interaction("", "neutral", 0, 0, response)
                logging.info("Chat session ended by user (KeyboardInterrupt).")
                break
            except Exception as e:
                response = "Oops, something went wrong. Please try again."
                log_and_print(f"{self.bot_name}: {response}", 'error')
                self._save_interaction(user_input if 'user_input' in locals() else "", "error", 0, 0, response)
                logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    try:
        logging.info("Chatbot is starting up.")
        chatbot = Chatbot()
        chatbot.chat()
        logging.info("Chatbot session ended.")
    except ImportError as e:
        log_and_print("Error: Please ensure the latest 'nltk', 'textblob', and 'langdetect' are installed. Run:", 'error')
        log_and_print("pip install --upgrade nltk textblob langdetect", 'error')
        logging.error(f"ImportError: {e}")
        sys.exit(1)
