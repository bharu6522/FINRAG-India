# from langchain_core.documents.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter


from dotenv import load_dotenv

load_dotenv()


text = """ Kalam worked with metallurgist V. S. R. Arunachalam, who was then scientific adviser to the 
Defence Minister, on the suggestion by the then Defence Minister R. Venkataraman on the simultaneous development 
of a quiver of missiles instead of taking planned missiles one after another.[28] Venkatraman was instrumental in
 getting the cabinet approval for allocating ₹3.88 billion (equivalent to ₹66 billion or US$780 million in 2023) 
 for the project titled Integrated Guided Missile Development Programme (IGMDP) and appointed Kalam as its chief 
 executive.[28] Kalam played a major role in the development of missiles including Agni, an intermediate range 
 ballistic missile and Prithvi, the tactical surface-to-surface missile, despite inflated costs and time 
 overruns.[28][29] He was known as the "Missile Man of India" for his work on the development of ballistic 
 missile and launch vehicle technology."""


splitter = RecursiveCharacterTextSplitter(chunk_size = 100, 
                                 chunk_overlap = 0
                                #  separator = ''
                                 )
result = splitter.split_text(text)

print(result)

