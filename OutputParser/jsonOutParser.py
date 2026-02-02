from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


from langchain_openai import  ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI() #model = 'gpt-4.1-nano'
# result = model.invoke("What is my name")

parser = JsonOutputParser()
# Prompt Template    
template = PromptTemplate(template=  "give me the name, age and city of a fictional person \n {format_instructions}",
                           input_variables=[], 
                           partial_variables=  {"format_instructions": parser.get_format_instructions()})

prompt = template.format()
result = model.invoke(prompt)

final_result = parser.parse(result.content)
 
print(final_result)