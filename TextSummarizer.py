import re
from tika import parser
import string
import heapq
#!pip3 install nltk
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize
stop_word = stopwords.words('english')

def read_file(file_name):
    raw = parser.from_file(file_name)
    text= raw['content']
    article = text.replace('\n','')
    processed = article.replace(r'^\s+|\s+?$','')
    processed = processed.replace('\n',' ')
    processed = processed.replace('\r',' ')
    processed = processed.replace("\\",'')
    processed = processed.replace(",",'')
    processed = processed.replace('"','')
    processed = re.sub(r'\[[0-9]*\]','',processed)
    return processed
    
def compute_score(processed):
    sentences = sent_tokenize(processed)
    frequency = {}
    processed1 = processed.lower()
    for word in word_tokenize(processed1):
      if word not in stop_word and word not in string.punctuation:
         if word not in frequency.keys():
            frequency[word]=1
         else:
            frequency[word]+=1
    
    max_fre = max(frequency.values())
    for word in frequency.keys():
         frequency[word]=(frequency[word]/max_fre)
    sentence_score = {}
    for sent in sentences:
       for word in word_tokenize(sent):
          if word in frequency.keys():
             if len(sent.split(' '))<50:
                if sent not in sentence_score.keys():
                    sentence_score[sent] = frequency[word]
                else:
                    sentence_score[sent]+=frequency[word]
    return sentence_score
    
def extract_top(sentence_score):
   summary = heapq.nlargest(5,sentence_score,key = sentence_score.get)
   summary = '\n'.join(summary)
   return summary
   
def generate_summary(file_name):
    text=read_file(file_name)
    sentence_dict=compute_score(text)
    final_summary=extract_top(sentence_dict)
    return(final_summary)

def summarize(filename):
  
   summarized_file=generate_summary(filename)
   body={}
   body['summary']=summarized_file
   return body
  
