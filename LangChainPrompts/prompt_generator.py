from langchain_core.prompts import PromptTemplate

template = PromptTemplate(template= f"""
You are an expert research paper summarizer.

Summarize the following research paper based on user selections:

Instructions:
- Use a clear and accurate tone.
- Preserve key contributions, methodology, and results.
- Follow the selected style strictly.
- Match the selected word count as closely as possible.
- Explain the mathematical concepts using code snippets wherever applicable
- use related analogies to simplify complex ideas 
- if certain information in not avalible in the paper,respons with : "Insufficient information avaliable" instead of guessing. 

Generate the best possible summary.
""" , input_variables= ['paper_input', 'style_input','length_input' ] )


# Paper Title: **{paper_input}**
# Summary Style: **{style_input}**
# Target Length: **{length_input}**


template.save('template.json')