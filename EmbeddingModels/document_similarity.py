from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 

load_dotenv()


embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=300)

docs = ["Virat Kohli is known for his aggressive batting style and exceptional chase mastery.", 
        "Rohit Sharma holds multiple double centuries in ODI cricket and is famous for his effortless timing.", 
        "Jasprit Bumrah is India's premier fast bowler, recognized for his deadly yorkers and unorthodox action.",
        "KL Rahul is a technically sound batsman who can adapt to any batting position across formats.",
        "Ravindra Jadeja is one of the best all-rounders in world cricket, offering match-winning performances with bat, ball, and fielding."]


query = "tell me about jasprit bumrah"


doc_embedding = embedding.embed_documents(docs)

query_embedding = embedding.embed_query(query)

# print(cosine_similarity([query_embedding], doc_embedding)) ## Need to be a 2d list 
scores = cosine_similarity([query_embedding], doc_embedding)[0]

index, score = sorted(list(enumerate(scores)),key= lambda x:x[1])[-1] # Sorting based on second argument 
# using enumerate giving index to that list 
# print(sorted(list(enumerate(scores)),key= lambda x:x[1]))
print(query)
print(docs[index])
print("similarity_score is :",score)