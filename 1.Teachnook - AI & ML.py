'''Develop a chatbot equipped with sentiment analysis capabilities. The chatbot will analyze the sentiment of the user's input. The sentiment analysis component will determine whether the user's message expresses a positive, negative, or neutral sentiment.
This project combines natural language processing (NLP) techniques, To Find the Sentiment Of User. '''

import nltk
from textblob import TextBlob
import sys
import random
import langdetect
from langdetect import detect

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
                    print(f"{self.bot_name}: Please say something!")
                    continue

                if user_input in self.goodbyes:
                    print(f"{self.bot_name}: Goodbye!")
                    break

                if user_input in self.greetings:
                    print(f"{self.bot_name}: Hello! How can I assist you?")
                    continue

                # Check for non-English input
                try:
                    if detect(user_input) != 'en':
                        print(f"{self.bot_name}: I work best with English input. Results may be less accurate for other languages.")
                except langdetect.lang_detect_exception.LangDetectException:
                    pass  # Ignore detection errors for short or ambiguous text

                sentiment, polarity, subjectivity = self.get_sentiment(user_input)

                if sentiment == "error":
                    print(f"{self.bot_name}: Sorry, I couldn't analyze that input.")
                else:
                    print(f"{self.bot_name}: You expressed a {sentiment} sentiment.")
                    print(f"{self.bot_name}: Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f}")
                    # Select a random response based on sentiment
                    if sentiment == "positive":
                        print(f"{self.bot_name}: {random.choice(self.positive_responses)}")
                    elif sentiment == "negative":
                        print(f"{self.bot_name}: {random.choice(self.negative_responses)}")
                    else:
                        print(f"{self.bot_name}: {random.choice(self.neutral_responses)}")

            except KeyboardInterrupt:
                print(f"\n{self.bot_name}: Goodbye!")
                break
            except Exception as e:
                print(f"{self.bot_name}: Oops, something went wrong. Please try again.")

if __name__ == "__main__":
    try:
        chatbot = Chatbot()
        chatbot.chat()
    except ImportError as e:
        print("Error: Please ensure the latest 'nltk', 'textblob', and 'langdetect' are installed. Run:")
        print("pip install --upgrade nltk textblob langdetect")
        sys.exit(1)
