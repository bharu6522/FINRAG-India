from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()

prompt = PromptTemplate(template= "Write a Joke about {topic}",
                        input_variables= ['topic'])

prompt2 = PromptTemplate(template= "Give the easiest explaination for the joke : {joke}", 
                         input_variables= ['joke'])


model = ChatOpenAI()
parser = StrOutputParser()

chain = RunnableSequence(prompt , model, parser , prompt2 , model, parser)

result = chain.invoke({'topic': 'Modi Ji'})
print(result)