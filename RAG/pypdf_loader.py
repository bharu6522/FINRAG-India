from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

from langchain_community.document_loaders import PyPDFLoader


load_dotenv()

model = ChatOpenAI()

loader = PyPDFLoader(r"D:\Gitlab_repos\personal\LangChain\RAG\VENTURA SECURITIES_updated.pdf")
docs = loader.load()


print(docs[0].page_content)
print(docs[0].metadata)


