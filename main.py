import requests
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
AI_DEVS_KEY = os.getenv("AIDEVS_API_KEY")

TOKEN = "https://tasks.aidevs.pl/token/liar"
ANSWER = "https://tasks.aidevs.pl/answer"
TASK = "https://tasks.aidevs.pl/task"
TOKEN_PARAMS = {
    "apikey": AI_DEVS_KEY
}
BLOG_TEXTS = []

token_response = requests.post(url=TOKEN, json=TOKEN_PARAMS)
token_response.raise_for_status()
token_data = token_response.json()
token = token_data["token"]

get_task_response = requests.get(url=f"{TASK}/{token}")
token_response.raise_for_status()
task_data = get_task_response.json()

question_data = {"question": "what is capitol city of germany?"}
question = question_data["question"]
question_response = requests.post(url=f"{TASK}/{token}", data=question_data)
token_response.raise_for_status()
answer_data = question_response.json()
answer = answer_data["answer"]
print(answer)

chat = ChatOpenAI(api_key=OPEN_AI_KEY)

system_prompt = ("Is the answer to the question relevant?Question: What is the capital of Germany?"
                 "Answer YES if it is relevant. Answer NO if it is not relevant.")

system_message = {"role": "system", "content": system_prompt}
human_message = HumanMessage(content=answer)
response = chat.invoke([system_message, human_message])

content = response.content
print(content)

answer = {
    "answer": content
}
send_answer = requests.post(url=f"{ANSWER}/{token}", json=answer)
