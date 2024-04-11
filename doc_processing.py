from langchain_core.pydantic_v1 import BaseModel, Field


def justnames(docs):
    names = []
    for d in docs:
        u = d.name.split('.')[0]
        names.append(u)
    return names    ## retrieving names and storing them in a file for future use


def process_pdf(files):
    
    import os
    import streamlit as st
    paths = []
    
    names = justnames(files) # we send our input files of bytesIO type to this function to just retrieve their names
    for f in files:
        f.seek(0) 
        n = f.name.split('.')[0]
        if (os.path.isfile("{}.pdf".format(n))):
            paths.append(os.path.abspath("{}.pdf".format(n)))
        else:
            with open("{}.pdf".format(n), mode="wb") as doc:
                doc.write(f.read())
                paths.append(os.path.abspath("{}.pdf".format(n)))
    
    
    return paths, names


def vectordb(l,noun):

    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.vectorstores import FAISS
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_text_splitters import CharacterTextSplitter

    tools = []
        
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    for id,road in enumerate(l):  # l is the list with paths 
        loader = PyPDFLoader(road)
        pages = loader.load_and_split()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(pages)
        embeddings = OpenAIEmbeddings()
        retriever = FAISS.from_documents(docs, embeddings).as_retriever()
        t = toolbox(llm, retriever, noun[id])  ## function call to the function in toolkit.py
        #print(f"tool appended{t}")
        tools.append(t)


    return tools




        
# class DocumentInput(BaseModel):
#     question: str = Field(description="This is the user's query that must be answered by referring to tools")


def toolbox(model, context, n):
        
        from langchain.chains import RetrievalQA
        from langchain.agents import Tool,load_tools
        
        from langchain_core.pydantic_v1 import BaseModel, Field
        class DocumentInput(BaseModel):
                question: str = Field()
        
        t = Tool(
            args_schema=DocumentInput,
            name=n,
            description="when user queries information related to {}, use this tool".format(n),
            func=RetrievalQA.from_chain_type(llm=model, retriever=context),
        )

        return t



    

