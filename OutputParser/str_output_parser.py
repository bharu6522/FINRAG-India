from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate


from langchain_openai import  ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI() #model = 'gpt-4.1-nano'
# result = model.invoke("What is my name")

# Prompt Template    
template1 = PromptTemplate(template=  "Write a detailed report on the {topic}",
                           input_variables=["topic"])
 
template2 = PromptTemplate(template="Write a 5 Line of Summary for the following text. /n",
                            input_variables=["text"])

prompt1 = template1.invoke({'topic': "Black Hole"})
result1 = model.invoke(prompt1)

prompt2 = template2.invoke({'text': result1.content})
result2 = model.invoke(prompt2)

print(result2.content)


