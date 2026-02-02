from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model = "gpt-3.5-turbo-instruct-0914")

result = llm.invoke("what is capital of India")

print(result)  