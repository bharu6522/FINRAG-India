from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()   
model = ChatOpenAI()  # model = 'gpt-4.1-nano'

class Person(BaseModel):
    name: str = Field(description="The name of the fictional person")
    age: int = Field(gt=18, description="age of the person")
    city: str = Field(description="The city where the person lives")

    
parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(template = "give me the name, age and city of a fictional {place}person \n {format_instructions}",
                           input_variables=['place'], partial_variables={"format_instructions": parser.get_format_instructions()}) 

prompt = template.invoke({'place': 'Indian'}) 
result = model.invoke(prompt)   

final_result = parser.parse(result.content)
print(final_result)  


