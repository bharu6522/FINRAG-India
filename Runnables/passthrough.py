from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableSequence
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
model = ChatOpenAI()

prompt = PromptTemplate(template="Generate a Joke for the {topic}", input_variables= ['topic'])

parser = StrOutputParser()

joke_generate_chain = RunnableSequence(prompt, model, parser)

prompt2 = PromptTemplate(template= "Give the easiest and simple explanation of the {joke}", input_variables= ['joke'])

parallel_chain = RunnableParallel({'joke': RunnablePassthrough(), 'explanation': RunnableSequence(prompt2, model, parser)})


final_chain = RunnableSequence(joke_generate_chain, parallel_chain)

result = final_chain.invoke({'topic': 'Poverty in India'})

print(result)