from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableSequence, RunnableLambda, RunnableBranch
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
model = ChatOpenAI()

prompt1 = PromptTemplate(template= "Write a detailed report on {topic}", input_variables= ['topic'])
prompt2 = PromptTemplate(template= "Summarize the following {text}", input_variables= ['text'])

parser = StrOutputParser()

report_gen_chain = RunnableSequence(prompt1 , model, parser)

branch_chain = RunnableBranch(( lambda x: len(x.split()) > 500, RunnableSequence(prompt2, model, parser)),
                              RunnablePassthrough())

final_chain = RunnableSequence(report_gen_chain, branch_chain)

result = final_chain.invoke({'topic': 'Russia v/s Ukrain'})

print(result)