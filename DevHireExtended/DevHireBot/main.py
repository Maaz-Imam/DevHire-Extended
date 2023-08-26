from . import constants
from .libFile import *

os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
embeddings = OpenAIEmbeddings()

def resume_loader(file):
    documents = []
    if file.endswith('.pdf'):
        # pdf_path = './resumes/' + file
        loader = PyMuPDFLoader(file)
        documents.extend(loader.load())
    elif file.endswith('.docx') or file.endswith('.doc'):
        # doc_path = './resumes/' + file
        loader = Docx2txtLoader(file)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        # text_path = './resumes/' + file
        loader = TextLoader(file)
        documents.extend(loader.load())
    return documents



def create_db_from_pdf(pdf_url):
    data = resume_loader(pdf_url)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, 
        chunk_overlap=0
    )
    print(len(data))
    docs = text_splitter.split_documents(data)

    db = FAISS.from_documents(docs, embeddings)
    return db


def get_response_from_query(db, query, k=5):

    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    chat = ChatOpenAI(
        model_name="gpt-3.5-turbo", 
        temperature=0.2
    )

    # Template to use for the system message prompt
    template = """
        You are a helpful assistant that can answer questions about candidates` resumes 
        based on the resume chunks: {docs}
        
        Only use the factual information from the transcript to answer the question and not out of it.
        
        If you feel like you don't have enough information to answer the question, just say "It isn't mention." and nothing else.
        
        Your answers should be to detailed.
        """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "Answer the following question:\n {question}"
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

    response = chain.run(
        question=query, 
        docs=docs_page_content
    )
    response = response.replace("\n", "")
    return response, docs




def make_json_from_resume(pdf_url, user_id, is_print=True):
    db = create_db_from_pdf(pdf_url)
    dict_queries = {
        "education": "What education does this candidate has, also mention GPA if there?",
        "experience": "What experiences does this candidate has?",
        "projects": "What projects does this candidate has?",
        "languages": "What languages does this candidate know?",
        "interests": "Are there any interests does this candidate has?",
        "skills": "What technical skills  does this candidate has?",
        "certifications": "What professional certifications does this candidate has to prove their skills?",
        "awards": "What awards does this candidate has?",
    }
    dict_answers = {}
    for i in dict_queries:
        response, _ = get_response_from_query(db, dict_queries[i])
        # @Dinesh's work to make it prettier :,)
        print(f" ------------------- Analyzed {str(i)} -------------------")
        dict_answers[i] = response
        

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = f"dumps\\{user_id}_data.json"
    full_path = os.path.join(script_dir, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # convert dict to json
    json_data = json.dumps(dict_answers, indent=4)
    with open(full_path, "w") as json_file:
        json_file.write(json_data)
    if is_print:
        print(json_data)
    
    return full_path