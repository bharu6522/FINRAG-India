from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal

load_dotenv()
model = ChatOpenAI(model= 'gpt-4o-mini')


class Review(TypedDict):
    key_themes: Annotated[list[str], "write down all the key themes discussed in the review"]
    summary: Annotated[str, "A brief summary of the review"] 
    sentiment: Annotated[Literal["pos","neg"], "Return sentiment of the review either positive, negative or neutral"]
    pros: Annotated[Optional[list[str]], "write down all the pros inside a list"]
    cons: Annotated[Optional[list[str]], "write down all the cons inside a list"]

structured_model = model.with_structured_output(Review)

# result = structured_model.invoke("""
# This product delivers excellent performance with a smooth user experience and reliable build quality.
#                        The design feels modern and intuitive, making everyday use effortless. 
#                       Customer support is responsive and helpful, adding to the overall satisfaction. 
#                       While there’s still room for small improvements, it offers great value and stands
#                        out as a dependable choice.  """)


result = structured_model.invoke("""
The laptop delivers outstanding performance for both professional workloads and casual use, with fast boot times, 
                                 vibrant display quality, and excellent battery life.
                                  Its lightweight design and sturdy build make it ideal for frequent travelers. 
                                 However, the speakers are underwhelming for media consumption, and the device
                                  tends to heat up during prolonged gaming sessions. Despite these limitations, 
                                 it remains a highly reliable choice 
                                 for productivity-focused users who value speed, portability, and a premium feel  
                                  """)


print(result)

# print(result['summary'])
# print(result['sentiment'])

