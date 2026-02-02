from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

prompt1 = PromptTemplate(template = "Generate a detailed report on the {topic}",
                         input_variables=['topic'])

prompt2 = PromptTemplate(template = "Generate a 5 point summary from the following text : {text}",
                         input_variables=['text'])

model = OpenAI()
parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser
result = chain.invoke({'topic': 'Impact of Climate Change on Coastal Cities'})

print(result)

chain.get_graph().print_ascii()