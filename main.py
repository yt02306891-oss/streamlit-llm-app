from langchain.chains import RetrievalQA

from langchain.chat_models import ChatOpenAI

from langchain.memory import ConversationBufferMemory

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

memory = ConversationBufferMemory()

chain = RetrievalQA.from_chain_type(

    llm=llm,

    chain_type="stuff",

    retriever=retriever,

    memory=memory

)

chain.run("HealthXの、ユーザー体験向上のための仕掛けを一言で教えてください。")