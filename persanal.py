from IPython.display import Markdown, display, update_display
from dotenv import load_dotenv
from openai import OpenAI
import ollama

MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'


load_dotenv()
openai=OpenAI()

def get_model_responses(question):
    """
    Takes a question as input, queries GPT-4o-mini and Llama 3.2 models, 
    and displays their responses.
    
    Args:
        question (str): The question to be processed by the models.
    """
    # system_prompt is already declared above lets generate a new user prompt so that the input question can be sent
    user_input_prompt = f"Please give a detailed explanation to the following question: {question}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input_prompt}
    ]
     # GPT-4o-mini Response with Streaming
    print("Fetching response from GPT-4o-mini...")
    stream = openai.chat.completions.create(model=MODEL_GPT, messages=messages, stream=True)

    response_gpt = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response_gpt += chunk.choices[0].delta.content or ''
        response_gpt = response_gpt.replace("```", "").replace("markdown", "")
        update_display(Markdown(response_gpt), display_id=display_handle.display_id)

    # Llama 3.2 Response
    print("Fetching response from Llama 3.2...")
    response_llama = ollama.chat(model=MODEL_LLAMA, messages=messages)
    reply_llama = response_llama['message']['content']
    display(Markdown(reply_llama))
    
 # Prompt user for their question
my_question = input("Please enter your question: ")
# Fetch and display responses from models
get_model_responses(my_question)
    

