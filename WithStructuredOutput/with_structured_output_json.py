from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel, Field


load_dotenv()
model = ChatOpenAI(model= 'gpt-4o-mini')


# class Review(BaseModel):
#     key_themes:list[str] = Field(description="write down all the key themes discussed in the review list")
#     summary: str = Field(description= "A brief summary of the review")
#     sentiment: Literal["pos", "neg"] = Field(description= "Return sentiment of the review either positive, negative or neutral")
    
#     pros: Optional[list[str]] = Field(default=None ,description= "write down all the pros inside a list")

#     cons: Optional[list[str]] = Field(default= None, description= "write down all the cons inside a list")
#     name : Optional[list[str]] = Field(default= None, description= "write the name of the reviewer")


# Schema 

json_schema = {
  "title": "Review",
  "type": "object",
  "properties": {
    "key_themes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "write down all the key themes discussed in the review list"
    },
    "summary": {
      "type": "string",
      "description": "A brief summary of the review"
    },
    "sentiment": {
      "type": "string",
      "enum": ["pos", "neg"],
      "description": "Return sentiment of the review either positive, negative or neutral"
    },
    "pros": {
      "type": "array",
      "items": { "type": "string" },
    #   "nullable": true,
      "description": "write down all the pros inside a list"
    },
    "cons": {
      "type": "array",
      "items": { "type": "string" },
    #   "nullable": true,
      "description": "write down all the cons inside a list"
    },
    "name": {
      "type": "array",
      "items": { "type": "string" },
    #   "nullable": true,
      "description": "write the name of the reviewer"
    }
  },
  "required": ["key_themes", "summary", "sentiment"]
}







structured_model = model.with_structured_output(json_schema)

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
                                  
                                 review by Bharti Jain
                                 """)


print(result.name)

# print(result['summary'])
# print(result['sentiment'])

