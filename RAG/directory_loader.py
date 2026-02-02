from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI()
loader = DirectoryLoader(path = r"D:\Gitlab_repos\personal\LangChain\RAG\Apptitude",
                         glob= "*.pdf",
                         loader_cls= PyPDFLoader)

docs = loader.lazy_load()
# print(len(docs))

for document in docs :
    print(document)
