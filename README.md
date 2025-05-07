# Sentiment Analysis Chatbot

This project implements a chatbot with sentiment analysis capabilities, built using Python 3.12. The chatbot analyzes user input to determine whether the sentiment is positive, negative, or neutral, using Natural Language Processing (NLP) techniques via the TextBlob library. It responds with varied messages based on the detected sentiment and stores all interactions in a JSON file for persistence.

## Features

- **Interactive Chatbot**: Recognizes greetings (e.g., "hello", "hi") and goodbyes (e.g., "bye", "goodbye") for natural conversation flow.
- **Sentiment Analysis**: Classifies user input as positive, negative, or neutral using TextBlob, providing polarity and subjectivity scores.
- **Non-English Detection**: Warns users if non-English input is detected, as sentiment analysis is optimized for English.
- **Conversation History**: Stores all interactions (user input, sentiment, polarity, subjectivity, response, timestamp) in 'chat_history.json'.
- **Robust Error Handling**: Handles empty inputs, keyboard interrupts, file I/O errors, and missing dependencies gracefully.
- **Python 3.12 Compatibility**: Ensures compatibility with Python 3.12, with a version checkpoint at startup.

## Requirements

- **Python**: Version 3.12 or later.
- **Dependencies** (Listed in 'requirements.txt'):
  - 'nltk==3.8.1'
  - 'textblob==0.18.0.post0'
  - 'langdetect==1.0.9'

## Installation

### 1. Install Python 3.12:
Download and install Python 3.12 or later from [python.org](https://www.python.org/).  
Verify the version:
'''bash
python --version
'''
Output should be 'Python 3.12.x'.

### 2. Clone or Download the Project:
Clone the repository or download the project files.

### 3. Set Up a Virtual Environment (recommended):
'''bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
'''

### 4. Install Dependencies:
'''bash
pip install --upgrade pip
pip install -r requirements.txt
'''

### 5. Run the Chatbot:
'''bash
python chatbot.py
'''

## Usage

### Start the Chatbot:
Run 'chatbot.py' to launch the chatbot. It will display the Python version and compatibility status:
'''text
Running on Python 3.12.1
This version is compatible and supported.
ChatBot: Hi! I am your chatbot. How can I help you? (Please use English for best results)
'''

### Interact with the Chatbot:

- **Greetings**:  
  '''
  You: hello  
  ChatBot: Hello! How can I assist you?
  '''

- **Sentiment Analysis**:  
  '''
  You: I love this!  
  ChatBot: You expressed a positive sentiment.  
  ChatBot: Polarity: 0.50, Subjectivity: 0.60  
  ChatBot: That's awesome to hear!
  '''

- **Non-English Input**:  
  '''
  You: Bonjour  
  ChatBot: I work best with English input. Results may be less accurate for other languages.  
  ChatBot: You expressed a neutral sentiment.  
  ChatBot: Polarity: 0.00, Subjectivity: 0.00  
  ChatBot: Got it, keeping things chill!
  '''

- **Goodbye**:  
  '''
  You: bye  
  ChatBot: Goodbye!
  '''

- **Empty Input**:  
  '''
  You:  
  ChatBot: Please say something!
  '''

### View Conversation History:
All interactions are saved in 'chat_history.json' in the project directory. Example entry:
'''json
{
    "timestamp": "2025-05-07T12:34:56.789123",
    "user_input": "I love this!",
    "sentiment": "positive",
    "polarity": 0.5,
    "subjectivity": 0.6,
    "response": "You expressed a positive sentiment.\nPolarity: 0.50, Subjectivity: 0.60\nThat's awesome to hear!"
}
'''

## Limitations

- **English-Centric**: Sentiment analysis may be inaccurate for non-English languages. A warning is issued using 'langdetect'.
- **No Machine Learning**: Sentiment analysis uses rule-based NLP via TextBlob, not machine learning.
- **File Size Growth**: Continuous use may grow 'chat_history.json', affecting performance.
- **Performance**: Limited to TextBlob’s capabilities, which may not handle complex sentiments.

## Potential Improvements

- **Multilingual Support**: Replace TextBlob with a multilingual model like 'nlptown/bert-base-multilingual-uncased-sentiment'.
- **Machine Learning**: Use ML models (e.g., 'scikit-learn', 'transformers') for improved sentiment analysis.
- **File Management**: Implement log rotation or archiving for 'chat_history.json'.
- **Enhanced Responses**: Add more varied or context-aware replies.

## Troubleshooting

- **Dependency Errors**:
  '''bash
  pip install -r requirements.txt
  pip install --upgrade pip
  '''

- **NLTK Download Errors**:
  '''python
  import nltk
  nltk.download('punkt')
  '''

- **File I/O Errors**:
  - Check write permissions on 'chat_history.json'
  - Ensure sufficient disk space and access

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or contributions, please open an issue or submit a pull request on the project repository.