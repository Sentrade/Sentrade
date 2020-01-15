#author: davide

"""
pip install -U spacy
python -m spacy download en_core_web_sm
"""
import json
import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")

#doc = nlp("My name is Davide.")
#print (doc)
#print ([t for t in doc])
#for t in doc:
#    print(t,t.pos_,t.dep_)

index = "apple"
#news = "Apple is looking at buying U.K. startup for $1 billion."

def is_org(news,index):
    doc = nlp(news["text"])
    for t in doc.ents:
        if t.lower_ == index:
            if t.label_ == "ORG":
                return True
    return False

def analyze_sent(inputfile,outputfile):
    with open(inputfile) as news_file:
        input_data= json.load(news_file)

    #Integrating @Ziyou's TextBlob
    for news in input_data:
        if is_org(news,index):
            blob = TextBlob(news["text"])
            news["polarity"] = blob.sentiment.polarity
            news["subjectivity"] = blob.sentiment.subjectivity

    with open(outputfile, "w") as results:
        json.dump(input_data, results)

if __name__ == "__main__":
    analyze_sent("FN_data.json", "FN_data_results.json")

            
