import constantstemplate

from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

import json
import os
import random
import string

os.environ["OPENAI_API_KEY"] = constantstemplate.OPENAI_API_KEY
embeddings = OpenAIEmbeddings()


def create_db_from_pdf(pdf_url):
    loader = PyMuPDFLoader(pdf_url)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, chunk_overlap=0)
    docs = text_splitter.split_documents(data)

    db = FAISS.from_documents(docs, embeddings)
    return db


def get_response_from_query(db, query, k=5):

    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

    # Template to use for the system message prompt
    template = """
        You are a helpful assistant that can answer questions about candidates` resumes 
        based on the resume chunks: {docs}
        
        Only use the factual information from the transcript to answer the question, do not use any information from outside the scope of the transcript.
        
        If you feel like you don't have enough information to answer the question, just say "It isn't mentioned." and nothing else.
        
        Your answers should stick to detail.
        """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "Answer the following question:\n {question}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(
        human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(
        llm=chat,
        prompt=chat_prompt
    )

    response = chain.run(question=query, docs=docs_page_content)
    response = response.replace("\n", "")
    return response, docs




def make_json_from_resume(pdf_url):
    db = create_db_from_pdf(pdf_url)
    dict_queries = {
        "education": "What education does this candidate has, also mention GPA if there?",
        "experience": "What experiences does this candidate have?",
        "projects": "What projects has this candidate worked on?",
        "languages": "What languages/tech stacks does this candidate know?",
        "interests": "Are there any interests does this candidate has?",
        "skills": "What technical skills  does this candidate has?",
        "certifications": "What professional certifications does this candidate have to prove their skills?",
        "awards": "What awards does this candidate have?",
    }
    dict_answers = {}
    for i in dict_queries:
        response, _ = get_response_from_query(db, dict_queries[i])
        print(f" ------------------- Analyzed {i} -------------------")
        dict_answers[i] = response
    # convert dict to json
    json_data = json.dumps(dict_answers)
    random_ID = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    file_path = f"C:\\Users\\maazi\\OneDrive\\Documents\\WORK\\CODE\\Prometheus\\empty\\DevHire-Extended\\src\\output_{random_ID}_data.json"
    # Write the data to a JSON file
    with open(file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)
    return json_data


if __name__ == "__main__":
    url = "C:\\Users\\maazi\\OneDrive\\Documents\\WORK\\CODE\\Prometheus\\DResume.pdf"
    print(make_json_from_resume(url))
