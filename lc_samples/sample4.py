from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_openai import ChatOpenAI

load_dotenv(dotenv_path="../.env")

# Create a HumanMessagePromptTemplate directly from the template string
template_string = "Hello {name}"
human_message_template = HumanMessagePromptTemplate.from_template(template_string)

system_message = SystemMessagePromptTemplate.from_template("You are a helpful assistant. answer in japanese.")
ai_message = AIMessagePromptTemplate.from_template("こんにちは {name}! 本日はいかがしますか？")

# Create the ChatPromptTemplate
prompts = ChatPromptTemplate.from_messages([
    system_message,
    human_message_template,
    ai_message,
    ("human", "How to lean Rust lang")
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

output_parser = StrOutputParser()

# Invoke the template with the required variables
texts = (prompts | llm | output_parser).invoke({"name": "John"})


print(texts)
