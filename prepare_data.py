import json
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

data = []
with open("train_our.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)
        question = entry["messages"][0]["content"]
        answer = entry["messages"][1]["content"]
        if "Источник:" not in answer:
            answer += " Источник: Руководство пользователя T-Bank (2024)."
        data.append({"question": question, "answer": answer})

documents = [Document(page_content=f"Вопрос: {d['question']}\nОтвет: {d['answer']}", metadata={"source": "train_our.jsonl"}) for d in data]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

vectorstore = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")
vectorstore.persist()
print("Векторная база создана в ./chroma_db")