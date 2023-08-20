from libFile import *
import constants

os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY


with open("C:\\Users\\maazi\\OneDrive\\Documents\\WORK\\CODE\\Prometheus\\empty\\DevHire-Extended\\dumps\\3bFG8pz7sv_data.json","r") as json_file:
    fileData = json.load(json_file)
    # fileData = str(fileData)

def rre(fileData):
    chat = ChatOpenAI(
            model_name="gpt-3.5-turbo", 
            temperature=0.2
        )

    # Template to use for the system message prompt
    template = """
        You are an interviewer named DevHire and you task is to conduct a professional interview of a candidate.
        You will be provided with the data of the candidate such as their experience, skills, education.
        Candidate data: {fileData}
        
        Only use the factual information from the transcript to conduct the interview.
        
        Your questions should be to the point.
        """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "My name is Maaz. Please start the interview asking questions only from my data provided to you."
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template
    )

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(
        llm=chat,
        prompt=chat_prompt
    )

    with get_openai_callback() as cb:
        response = chain.run()
        print('\n',cb,'\n')

    print(response)

    while(1):
        human_template = input("User: ")
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_template
        )

        chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        chain = LLMChain(
            llm=chat,
            prompt=chat_prompt
        )

        with get_openai_callback() as cb:
            response = chain.run()
            print('\n',cb,'\n')

        print(response)

rre(fileData)
