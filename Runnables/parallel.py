from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel, RunnableSequence

load_dotenv()

model = ChatOpenAI()

prompt = PromptTemplate(template="Generate a tweet about the topic: {topic}",
                        input_variables= ['topic'])

prompt2 = PromptTemplate(template= "Generate a post for linkedin on the topic: {topic}",
                         input_variables= ['topic'])

parser = StrOutputParser()

chain = RunnableParallel({'tweet': RunnableSequence(prompt, model, parser),
                          'linkedin': RunnableSequence(prompt2, model, parser)})

result = chain.invoke({'topic': 'Autoencoder In Deep Learning'})

print(result)