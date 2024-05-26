'''Develop a chatbot equipped with sentiment analysis capabilities. The chatbot will analyze the sentiment of the user's input. The sentiment analysis component will determine whether the user's message expresses a positive, negative, or neutral sentiment.
This project combines natural language processing (NLP) techniques, machine learning algorithms To Find the Sentiment Of User. '''

import nltk
from textblob import TextBlob

class Chatbot:
    def __init__(self):
        self.greetings = ["hello", "hi", "hey", "greetings", "sup", "what's up"]
        self.goodbyes = ["Bye", "Goodbye", "See you", "Take care", "Farewell"]
        self.bot_name = "ChatBot"

    def get_sentiment(self, text):
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

    def chat(self):
        print(f"{self.bot_name}: Hi! I am chatbot. How can I help you?")
        while True:
            user_input = input("You: ").strip().lower()

            if user_input in self.goodbyes:
                print(f"{self.bot_name}: Goodbye!")
                break

            if user_input in self.greetings:
                print(f"{self.bot_name}: Hello! How can I assist you?")
                continue

            sentiment, polarity, subjectivity = self.get_sentiment(user_input)
            print(f"{self.bot_name}: You expressed a {sentiment} sentiment.")
            print(f"{self.bot_name}: Polarity: {polarity:.2f}, Subjectivity: {subjectivity:.2f}")

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.chat()
