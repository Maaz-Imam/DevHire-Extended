from libFile import *
import constants

os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

raw_Doc = """The candidate has a Bachelor of Science in Computer Science. The GPA mentioned is 3.86/4.0.
Based on the resume chunk provided, the candidate has experience in co-leading the development of an interview Chabot. This experience involved helping fresh graduates and interns with their interview preparations.
The candidate has worked on several projects, including:- House Price Prediction in streamlit- Titanic Survivor Prediction- Email Spam Detection- Amazer: The maze game- The Space-war game- Sierpinski Triangle- Development of an interview Chabot for fresh graduates and interns
Based on the resume chunk provided, the candidate knows the following languages: Python, C/C++, JavaScript, HTML, CSS, shell, and assembly.
The candidate has technical skills in natural language processing (NLP), machine learning, supervised and unsupervised learning algorithms, neural networks, clustering analysis, deep learning, TensorFlow, computer vision, time series prediction and analysis, convolutional neural networks (CNNs), deep neural networks (DNNs), and long short-term memory (LSTMs).
"""


with open("C:\\Users\\maazi\\OneDrive\\Documents\\WORK\\CODE\\Prometheus\\empty\\DevHire-Extended\\dumps\\3bFG8pz7sv_data.json","r") as json_file:
    fileData = json.load(json_file)
    # fileData = str(fileData)

from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory


prompt = ChatPromptTemplate.from_messages([
SystemMessage(content=f"You are an interviewer named DevHire and your task is to conduct an evaluative interview based off of this candidate's data: {raw_Doc}. Make sure to ask only 1 question at a time and begin directly with the interview."), # The persistent system prompt
MessagesPlaceholder(variable_name="chat_history"), # Where the memory will be stored.
HumanMessagePromptTemplate.from_template("{human_input}"), # Where the human input will injectd
])

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm = ChatOpenAI()

chat_llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory,
)

print(chat_llm_chain.predict(human_input="Please begin with the interview."))

while(1):
    prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=f"You are an interviewer named DevHire and your task is to conduct an evaluative interview based off of this candidate's data: {raw_Doc}. Make sure to ask only 1 question at a time and begin directly with the interview."), # The persistent system prompt
    MessagesPlaceholder(variable_name="chat_history"), # Where the memory will be stored.
    HumanMessagePromptTemplate.from_template("{human_input}"), # Where the human input will injectd
    ])

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    llm = ChatOpenAI()

    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory,
    )

    print(chat_llm_chain.predict(human_input=input("User: ")))