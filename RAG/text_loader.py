from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader 
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI()

loader = TextLoader(r"D:\Gitlab_repos\personal\LangChain\RAG\textloader.txt", encoding = 'utf-8')

docs = loader.load()

prompt = PromptTemplate(template= "Write a summary for the given {text}", input_variables= ['text'])

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({'text': docs[0].page_content})

print(result)
