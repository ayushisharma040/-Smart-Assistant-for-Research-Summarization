# Smart Assistant for Research Summarization - Streamlit + LangChain + PyMuPDF + FAISS

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader, TextLoader
from langchain.prompts import PromptTemplate
import tempfile
import os

st.set_page_config(page_title="Smart Research Assistant")
st.title("📄 Smart Assistant for Research Summarization")

openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file and openai_api_key:
    file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Load document
    if uploaded_file.name.endswith(".pdf"):
        loader = PyMuPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
    documents = loader.load()

    # Split document
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    # Create embeddings and vector DB
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectordb = FAISS.from_documents(chunks, embeddings)
    retriever = vectordb.as_retriever()

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=openai_api_key, temperature=0),
        retriever=retriever,
        return_source_documents=True
    )

    # Auto-summary
    summary_prompt = PromptTemplate(
        input_variables=["context"],
        template="""
        Summarize the following document in less than 150 words:
        {context}
        """
    )
    context_text = "\n".join([doc.page_content for doc in chunks[:3]])
    summary_chain = ChatOpenAI(openai_api_key=openai_api_key)
    summary = summary_chain.predict(summary_prompt.format(context=context_text))

    st.subheader("🔍 Auto Summary")
    st.write(summary.strip())

    # Modes
    mode = st.radio("Choose Interaction Mode:", ("Ask Anything", "Challenge Me"))

    if mode == "Ask Anything":
        user_query = st.text_input("Ask a question about the document:")
        if user_query:
            result = qa_chain({"query": user_query})
            st.subheader("Answer")
            st.write(result["result"])

            source_doc = result["source_documents"][0]
            st.caption(f"Justification: From page {source_doc.metadata.get('page', 'unknown')}.")
            with st.expander("See supporting text"):
                st.write(source_doc.page_content)

    elif mode == "Challenge Me":
        challenge_prompt = PromptTemplate(
            input_variables=["context"],
            template="""
            Based on the following document, generate 3 logic-based questions for comprehension:
            {context}
            """
        )
        logic_questions = summary_chain.predict(challenge_prompt.format(context=context_text))

        st.subheader("🧠 Answer These Questions")
        st.markdown(logic_questions)

        st.write("**Your Answers:**")
        q1 = st.text_input("Q1:")
        q2 = st.text_input("Q2:")
        q3 = st.text_input("Q3:")

        if q1 or q2 or q3:
            eval_prompt = PromptTemplate(
                input_variables=["context", "a1", "a2", "a3"],
                template="""
                Evaluate the user's answers:
                Context: {context}
                User Answers:
                1. {a1}
                2. {a2}
                3. {a3}
                Provide detailed feedback with justification from the context.
                """
            )
            eval = summary_chain.predict(eval_prompt.format(
                context=context_text,
                a1=q1 or "",
                a2=q2 or "",
                a3=q3 or ""
            ))
            st.subheader("📝 Evaluation and Feedback")
            st.write(eval)

else:
    st.info("Please upload a document and enter your OpenAI API key to begin.")
