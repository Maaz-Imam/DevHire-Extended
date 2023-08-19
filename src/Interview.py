from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.callbacks import get_openai_callback
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory

import json
import os
import constants

os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY


with open("dumps\\3bFG8pz7sv_data.json","r") as json_file:
    fileData = json.load(json_file)

# Template to use for the system message prompt
template = f"""
                You are DevHire, an interviewer conducting a candidate's interview.
                Here is the candidate's data:
                Education: {fileData["education"]}
                Experience: {fileData["experience"]}
                Projects: {fileData["projects"]}
                Languages/Tech Stack: {fileData["languages"]}
                Interests: {fileData["interests"]}
                Skills: {fileData["skills"]}
                Certifications: {fileData["certifications"]}
                Awards: {fileData["awards"]}

                Your task is to ask interview questions based solely on the provided data.
                Your questions should explore the candidate's education, experience, projects, skills, and other details.

                Remember, you are only allowed to ask questions related to the information provided above.
            """



# first initialize the large language model
llm = OpenAI(
	temperature=0,
	model_name="text-davinci-003"
)

conversation_sum_bufw = ConversationChain(
    llm=llm, memory=ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=1000
    )
)


def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        print(f'Spent a total of {cb.total_tokens} tokens')
    return result


print(count_tokens(conversation_sum_bufw,template))

while(True):
    print(count_tokens(conversation_sum_bufw,input("User: ")))