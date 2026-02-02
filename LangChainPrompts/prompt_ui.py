from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate , load_prompt



from dotenv import load_dotenv
import streamlit as st 

load_dotenv()

st.header("Research Tool")
# user_input = st.text_input("Enter your prompt")

# 1. Select Research Paper (you will provide the list)
paper_input = st.selectbox(
    "📄 Choose a research paper",
    [
        "Paper 1: Transformer Architecture", "Paper 2: BERT Pretraining",
        "Paper 3: Autoencoders Explained", "Paper 4: GANs Introduction",
        "Paper 5: LSTM & Seq2Seq Models"
    ]
)

# 2. Select Summary Style
style_input = st.selectbox(
    "📝 Choose summary style",
    [
        "Concise",
        "Detailed",
        "Beginner-Friendly",
        "Technical-Expert",
        "Bullet Points",
        "Executive Summary"
    ]
)

# 3. Select Summary Length
length_input = st.selectbox(
    "📏 Summary Length",
    [
        "50 words",
        "100 words",
        "150 words",
        "200 words",
        "300 words",
        "500 words"
    ]
)

# template = PromptTemplate(template= f"""
# You are an expert research paper summarizer.

# Summarize the following research paper based on user selections:

# Paper Title: **{paper_input}**
# Summary Style: **{style_input}**
# Target Length: **{length_input}**

# Instructions:
# - Use a clear and accurate tone.
# - Preserve key contributions, methodology, and results.
# - Follow the selected style strictly.
# - Match the selected word count as closely as possible.
# - Explain the mathematical concepts using code snippets wherever applicable
# - use related analogies to simplify complex ideas 
# - if certain information in not avalible in the paper,respons with : "Insufficient information avaliable" instead of guessing. 

# Generate the best possible summary.
# """ , input_variables= ['paper_input', 'style_input','length_input' ] )

template = load_prompt(r"D:\Gitlab_repos\personal\LangChain\LangChainPrompts\template.json")



model = ChatOpenAI(model='gpt-4.1-nano')

if st.button('summarize'):


    # prompt = template.invoke({'paper_input': paper_input, 
    #              'style_input': style_input, 
    #              'length_input': length_input})
    
    # result = model.invoke(prompt)

    chain = template | model  # instead of calling 2 times invoke method, we used chain and then invoke at aa single time
    
    result = chain.invoke({'paper_input': paper_input, 
                 'style_input': style_input, 
                 'length_input': length_input})
    st.write(result.content)
    