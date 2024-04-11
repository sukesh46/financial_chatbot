def agent_init(reper):

    from langchain.agents import AgentType, initialize_agent
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain.memory import ConversationBufferMemory

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    memory1 = ConversationBufferMemory(memory_key="chat_history")
    
    agent = initialize_agent(
        agent=AgentType.OPENAI_FUNCTIONS,
        memory = memory1,
        tools=reper,
        llm=llm,
        verbose=True,
        handle_parsing_errors = True
)
    
    return agent