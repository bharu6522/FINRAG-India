from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# from langchain.schema.runnable import RunnableParellel 
from langchain_core.runnables import RunnableParallel
from dotenv import load_dotenv

load_dotenv()

model1 = ChatOpenAI()

model2 = ChatOpenAI(model= "gpt-4")

prompt1 = PromptTemplate(template = "Generate a simple and short notes on the  {topic}",
                            input_variables=['topic'])

prompt2 = PromptTemplate(template = "Generate a 5 short question and answers from the text :  {text}",
                            input_variables=['text'])


prompt3 = PromptTemplate(template = "Merge the provided notes and quiz into a single document  {notes} & {quiz}",
                         input_vatariables=['notes', 'quiz'])


parser = StrOutputParser()

parellal_chain = RunnableParallel({ 'notes' : prompt1 | model1 | parser , 'quiz': prompt2 | model2 | parser })

merge_chain = prompt3 | model1 | parser 

chain = parellal_chain | merge_chain 

text = """ Generally, Support Vector Machines is considered to be a classification approach, it but can be employed in both types of classification and regression problems. It can easily handle multiple continuous and categorical variables. SVM constructs a hyperplane in multidimensional space to separate different classes. SVM generates optimal hyperplane in an iterative manner, which is used to minimize an error.
 The core idea of SVM is to find a maximum marginal hyperplane(MMH) that best divides the dataset into classes. Support Vectors
Support vectors are the data points, which are closest to the hyperplane. These points will define the separating line better by calculating margins. These points are more relevant to the construction of the classifier.

Hyperplane
A hyperplane is a decision plane which separates between a set of objects having different class memberships.

Margin
A margin is a gap between the two lines on the closest class points.
This is calculated as the perpendicular distance from the line to support vectors or closest points. 
If the margin is larger in between the classes, then it is considered a good margin, a smaller margin is a bad margin."""


result= chain.invoke({'text': text , 'topic' : 'Support Vector Machine'} )

print(result)

print(chain.get_graph().print_ascii())
