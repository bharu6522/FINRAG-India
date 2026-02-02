from langchain_anthropic import ChatAnthropic

from dotenv import load_dotenv

load_dotenv()

model = ChatAnthropic(mdoel = ""
                      )

result = model.invoke("What is capital of India")
print(result.content)