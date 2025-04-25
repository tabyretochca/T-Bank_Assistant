import redis
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig

class RAGSystem:
    def __init__(self, chroma_dir="./chroma_db"):
        # Эмбеддинги
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
        # Векторная база
        self.vectorstore = Chroma(persist_directory=chroma_dir, embedding_function=self.embeddings)
        # Redis для кэширования
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0)
        # Модель генерации
        self.llm = None

    def load_llm(self):
        # Квантизация для ruGPT-3.5 
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)
        tokenizer = AutoTokenizer.from_pretrained("ai-forever/ruGPT-3.5")
        model = AutoModelForCausalLM.from_pretrained("ai-forever/ruGPT-3.5", quantization_config=quantization_config)
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=50)
        self.llm = HuggingFacePipeline(pipeline=pipe)

    def format_response(self, raw_answer, source):
        return f"📋 Ответ: {raw_answer}\n🔗 Источник: {source}\nЕсли у вас есть другие вопросы, напишите!"

    def get_response(self, query, use_llm=False):
        # Проверяем кэш
        cached = self.redis_client.get(query)
        if cached:
            return cached.decode(), self.get_buttons(query)

        # Поиск документов
        docs = self.vectorstore.similarity_search(query, k=1)
        if not docs:
            response = "Извините, не нашёл ответа на ваш вопрос."
            return response, self.get_buttons(query)

        context = docs[0].page_content
        answer = context.split("Ответ: ")[1] if "Ответ: " in context else context
        source = docs[0].metadata["source"]

        # Если LLM не используется (локально)
        if not use_llm or not self.llm:
            response = self.format_response(answer, source)
            self.redis_client.set(query, response)
            return response, self.get_buttons(query)

        # Генерация с LLM 
        prompt = f"На основе текста:\n{context}\nОтветь на вопрос: {query}\nДобавь: Источник: {source}"
        response = self.llm(prompt)
        formatted_response = self.format_response(response, source)
        self.redis_client.set(query, formatted_response)
        return formatted_response, self.get_buttons(query)

    def get_buttons(self, query):
        buttons = [
            {"text": "Открыть счёт", "url": "https://tbank.ru/kassa/form/partner/"},
            {"text": "Связаться с поддержкой", "url": "https://tbank.ru/support/"}
        ]
        if "лимит" in query.lower():
            buttons.append({"text": "Проверить лимиты", "url": "https://tbank.ru/app/check-limits"})
        return buttons