from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv

chat_template = ChatPromptTemplate.from_messages([
    ("system", "you are a helpfull {domain} expert" ) ,
    ("human", "Explain the {topic} in very simple manner using all key details")
    
    # SystemMessage(content= 'you are a helpfull {domain} expert'),
    #                                HumanMessage(content= 'Explain the {topic} in very simple manner using all key details')
                                   ])


prompt = chat_template.invoke({'domain': 'medicine', 'topic': 'paracetamol'})

print(prompt)


# from langchain_core.prompts import ChatPromptTemplate

# chat_template = ChatPromptTemplate.from_messages([
#     ("system", "you are a helpful {domain} expert"),
#     ("human", "Explain the {topic} in very simple manner using all key details")
# ])

# prompt = chat_template.invoke(
#     {"domain": "medicine", "topic": "paracetamol"}
# )

# print(prompt)
