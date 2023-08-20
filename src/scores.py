from libFile import *
from textblob import TextBlob

def get_score_by_answer(message):
    blob = TextBlob(message)
    score = 0.0
    for word in blob.words:
        sentiment_score = TextBlob(word).sentiment.polarity
        score += ((sentiment_score + 1) / 2) * 9 + 1
    
    return score / len(message.split(" "))


def get_score_by_question(message):
    message = message.split(".")[0] # So this is like k it will only take one sentence maybe for scoring, like 
                                    # "Thats great. What else you been working on?" will be "Thats great", so the actual sentiment should be extracted
                                    # from the sentence and not the whole message (that can contain question for the cand as well) 
                                    # Try this i can update this with higher score as well!
    print(message)
    blob = TextBlob(message)
    score = 0.0
    for word in blob.words:
        sentiment_score = TextBlob(word).sentiment.polarity
        score += ((sentiment_score + 1) / 2) * 9 + 1
    
    return score / len(message.split(" "))



def get_ai_score(question, answer):
    pass