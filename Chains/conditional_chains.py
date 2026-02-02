from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# from langchain.schema.runnable import RunnableParellel 
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
from dotenv import load_dotenv

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()


model = ChatOpenAI()

parser = StrOutputParser()

class Feedback(BaseModel):
    sentiment : Literal['Positive','Negative'] = Field(description= "Give the sentiment of the Feedback")

parser2 = PydanticOutputParser(pydantic_object= Feedback)

prompt1 = PromptTemplate(template= ' {format_instruction} Classify the sentiment of the following feedback either postive or negative : {feedback} ',
                         input_variables= ['feedback'],
                         partial_variables= {'format_instruction': parser2.get_format_instructions()})


classifier_chain = prompt1 | model | parser2 

# result = classifier_chain.invoke({'feedback': 'I like the product too much. It is awesom'}).sentiment 
# print(result)


prompt2 = PromptTemplate(template= "Write an approprate response for this Positive feedback : {feedback}",
                         input_variables= ['feedback'])

prompt3 = PromptTemplate(template= "Write an approprate response for this Negative feedback : {feedback}",
                         input_variables= ['feedback'])


branch_chain = RunnableBranch((lambda x : x.sentiment == 'Positive' , prompt2 | model | parser ),
                              ( lambda x : x.sentiment == 'Negative', prompt3 | model | parser), 
                              RunnableLambda(lambda x : "Could not find any sentiment")) # converting simple condtion into tunnable Lambda 

chain = classifier_chain | branch_chain

result2 = chain.invoke({'feedback' : 'This is terrible phone. I will never purchase it again'})

print(result2)

print(chain.get_graph().print_ascii())


