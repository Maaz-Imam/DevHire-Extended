from .libFile import *
from . import constants


os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

def interview_go(fileData,request):

    data_keys = list(fileData.keys())
    data_values = list(fileData.values())

    system_prompt = ChatPromptTemplate.from_messages([
        # The persistent system prompt
        SystemMessage(
            content=f"""
                You are an interviewer named DevHire and your task is \
                to conduct the interview based off of these fields of a candidate's data: {str(data_keys)}. \
                The data of these fields will be provided to you later on \
                Make sure to ask only 1 question at a time and begin directly with the interview.
            """),
        # Where the memory will be stored.
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}"),  # Where the human input will injectd
    ])

    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)

    llm = ChatOpenAI()

    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=system_prompt,
        # verbose=True,
        verbose = False,
        memory=memory,
    )

    request.session['data_keys'] = data_keys
    request.session['data_values'] = data_values
    request.session['llm'] = llm
    request.session['memory'] = memory

    return chat_llm_chain.predict(human_input="Please start the interview")

def interview_process(hi,request):

    data_keys = request.session.get('data_keys', [])
    data_values = request.session.get('data_values', [])
    llm = request.session.get('llm')
    memory = request.session.get('memory')

    data_key = data_keys[0]
    data_value = data_values[0]

    prompt = ChatPromptTemplate.from_messages([
        # The persistent system prompt
        SystemMessage(
            content=f"""
            Ask conversational question(s) as an interviewer considering {data_key} of candidate is: {data_value}
            Do not ask reapeted or the information you already have.
            If the area is not defined  or isn't mentioned or if you think
            you have ask enough questions then answer only and only -1 and nothing else"""),
        # Where the memory will be stored.
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template(
            "{human_input}"),  # Where the human input will injectd
    ])

    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )

    return chat_llm_chain.predict(human_input=hi)





#  Copy of Interview_go function for safe keeping 

# def interview_go(fileData):
#     start = timer()

#     # with open("dumps/3bFG8pz7sv_data.json", "r") as json_file:
#     #     fileData = json.load(json_file)

#     data_keys = list(fileData.keys())
#     data_values = list(fileData.values())

#     system_prompt = ChatPromptTemplate.from_messages([
#         # The persistent system prompt
#         SystemMessage(
#             content=f"""
#                 You are an interviewer named DevHire and your task is \
#                 to conduct the interview based off of these fields of a candidate's data: {str(data_keys)}. \
#                 The data of these fields will be provided to you later on \
#                 Make sure to ask only 1 question at a time and begin directly with the interview.
#             """),
#         # Where the memory will be stored.
#         MessagesPlaceholder(variable_name="chat_history"),
#         HumanMessagePromptTemplate.from_template("{human_input}"),  # Where the human input will injectd
#     ])

#     memory = ConversationBufferMemory(
#         memory_key="chat_history", return_messages=True)

#     llm = ChatOpenAI()

#     chat_llm_chain = LLMChain(
#         llm=llm,
#         prompt=system_prompt,
#         # verbose=True,
#         verbose = False,
#         memory=memory,
#     )

#     print(chat_llm_chain.predict(human_input="Please start the interview"))

#     def interview_process(data_key, data_value):
#         prompt = ChatPromptTemplate.from_messages([
#             # The persistent system prompt
#             SystemMessage(
#                 content=f"""
#                 Ask conversational question(s) as an interviewer considering {data_key} of candidate is: {data_value}
#                 Do not ask reapeted or the information you already have.
#                 If the area is not defined  or isn't mentioned or if you think
#                 you have ask enough questions then answer only and only -1 and nothing else"""),
#             # Where the memory will be stored.
#             MessagesPlaceholder(variable_name="chat_history"),
#             HumanMessagePromptTemplate.from_template(
#                 "{human_input}"),  # Where the human input will injectd
#         ])

#         chat_llm_chain = LLMChain(
#             llm=llm,
#             prompt=prompt,
#             verbose=False,
#             memory=memory,
#         )

#         with get_openai_callback() as cb:
#             print(chat_llm_chain.predict(human_input=input("User: ")))
#             print(cb)


#     for i in range(22):
#         if i<3:
#             interview_process(str(data_keys[0]), str(data_values[0]))
#         if i<9:
#             interview_process(str(data_keys[1]), str(data_values[1]))
#         if i<18:
#             interview_process(str(data_keys[2]), str(data_values[2]))
#         if i<22:
#             interview_process(str(data_keys[3]) + ", " + str(data_keys[5]), str(data_values[3]  + ", " + str(data_keys[5])))

#     end = timer()
#     print("\n\n\nELapsed Time:",end - start) # time in seconds