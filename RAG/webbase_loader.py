from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, WebBaseLoader
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI()

url = "https://en.wikipedia.org/wiki/A._P._J._Abdul_Kalam"
loader = WebBaseLoader(url)

docs = loader.load()
print(len(docs))
print(docs[0].page_content)