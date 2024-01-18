import utils
import openai
from llama_index import SimpleDirectoryReader
from llama_index import VectorStoreIndex
from llama_index import ServiceContext
from llama_index.llms import OpenAI
from llama_index import Document


def retrieval_function(book, query, retrieve_only=True):
    if book == "The R Book": fp = "TheRBook.pdf"
    else: fp = "R_for_Data_Science.pdf"

    openai.api_key = utils.get_openai_api_key()

    documents = SimpleDirectoryReader(
        input_files=[fp]
    ).load_data()

    document = Document(text="\n\n".join([doc.text for doc in documents]))

    if retrieve_only:
        service_context = ServiceContext.from_defaults()
        index = VectorStoreIndex.from_documents([document])
        retriever = index.as_retriever()
        answer = retriever.retrieve(query)
        similarity, text = answer[0].score, str(answer[0].text)
        text = "This page contains information {} % similar to your query\n\n{}".format(similarity, text)
        return text

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0.1)
    service_context = ServiceContext.from_defaults(
        llm=llm,
    )
    index = VectorStoreIndex.from_documents([document],
                                            service_context=service_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return(str(response))
