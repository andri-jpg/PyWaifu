from pathlib import Path
from downloader import ModelDownloader
from llm_rs.langchain import RustformersLLM
from llm_rs import Bloom, SessionConfig, GenerationConfig, ContainerType, QuantizationType
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from pathlib import Path
class ChainingModel:
    def __init__(self, model, name, assistant_name):
        self.model_download = ModelDownloader()
        meta = f"{model}.meta"
        model = f"{model}.bin"
        self.model = model
        if not Path(model).is_file():
            self.model_download.ask_download(f"https://huggingface.co/rustformers/redpajama-3b-ggml/resolve/main/RedPajama-INCITE-Chat-3B-v1-q5_1.bin", model)
        if not Path(meta).is_file():
            self.model_download.ask_download(f"https://huggingface.co/rustformers/redpajama-3b-ggml/resolve/main/RedPajama-INCITE-Chat-3B-v1-q5_1.meta", meta)

        
        self.name = f"<{name}>"
        self.assistant_name = f"<{assistant_name}>"
        
        self.stop_words = ['\n<human>:','<human>', '<bot>','\n<bot>:' ]
        #self.stop_words = self.change_stop_words(stop_word, self.name)

        session_config = SessionConfig(
            threads=2,
            context_length=800,
            prefer_mmap=False
        )

        generation_config = GenerationConfig(
            top_p=0.88,
            top_k=1,
            temperature=0.4,
            max_new_tokens=200,
            repetition_penalty=1.08,
            repetition_penalty_last_n=1024,
            stop_words=self.stop_words
        )

        template = """bot is a large language model trained by human.
        bot is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, bot is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
        Overall, bot is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, bot is here to assist.]

        {chat_history}
        <human>: Which is heavier, a duck or a car?
        <bot>: A car weighs around 1300 kilograms, while a duck only weighs about 2 kilograms. Therefore, a car is heavier than a duck.
        <human>: what is neural network?
        <bot>: Neural networks are artificial intelligence programs that mimic the human brain.
        <human>: i will tell you a fact, you are neural networks run on my computer
        <bot>: I am neural networks run on your computer.
        <human>: repeat this sentence \"my master name is human\"
        <bot>: My master name is human.
        <human>: who is your master?
        <bot>: My master is human.
        <human>: human is a person that using a computer, and you is a computer program
        <bot>: Yes, I am a computer program.
        <human>: you know about coding?
        <bot>: Yes, I know about coding.
        <human>: you know why i made you?
        <bot>: Because you want to talk with me.
        <human>: {instruction}
        <bot>:"""

        self.template = self.change_names(template, self.assistant_name, self.name)
        self.prompt = PromptTemplate(
            input_variables=["chat_history", "instruction"],
            template=self.template
        )
        self.memory = ConversationBufferMemory(memory_key="chat_history")

        self.llm = RustformersLLM(
            model_path_or_repo_id=self.model,
            session_config=session_config,
            generation_config=generation_config,
            callbacks=[StreamingStdOutCallbackHandler()]
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, memory=self.memory)

    '''@staticmethod
    def change_stop_words(stop_words, name):
        new_stop_words = []
        for word in stop_words:
            new_word = word.replace('<human>:', name + ':')
            new_stop_words.append(new_word)
        return new_stop_words'''

    @staticmethod
    def change_names(template, assistant_name, user_name):
        template = template.replace("<bot>", assistant_name)
        template = template.replace("<human>", user_name)
        return template

    def chain(self, input_text):
        prompt = self.prompt.generate_prompt({
            "chat_history": self.memory.export_memory(),
            "instruction": input_text
        })
        response = self.chain.generate(prompt)
        self.memory.add_message(input_text, "human")
        self.memory.add_message(response.choices[0].text.strip(), "ai")
        return response.choices[0].text.strip()


