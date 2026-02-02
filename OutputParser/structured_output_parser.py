from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import  ResponseSchema, StructuredOutputParser

from langchain_openai import  ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI() #model = 'gpt-4.1-nano'
# result = model.invoke("What is my name")

schema = [
    ResponseSchema(name="fact_1", description="fact 1 about the {topic}"),
    
    ResponseSchema(name="fact_2", description="fact 2 about the {topic}"),
    ResponseSchema(name="fact_3", description="fact 3 about the {topic}")
    ]

parser = StructuredOutputParser.from_response_schemas(schema)
template = PromptTemplate(template=  "Give me 3 interesting facts about {topic} \n {format_instructions}",
                           input_variables=["topic"],
                           partial_variables=  {"format_instructions": parser.get_format_instructions()}
                           )   

prompt = template.format({'topic': "Black Hole"})
result = model.invoke(prompt)

final_result = parser.parse(result.content)   
print(final_result )

