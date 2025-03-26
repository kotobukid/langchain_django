from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableBranch

from langchain_openai import ChatOpenAI

load_dotenv(dotenv_path="../.env")

# Create a HumanMessagePromptTemplate directly from the template string
template_string = "{query}"
human_message_template = HumanMessagePromptTemplate.from_template(template_string)

system_message = SystemMessagePromptTemplate.from_template("You are a helpful assistant. Answer in japanese.")
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

# chat_prompt = ChatPromptTemplate.from_messages([("human", "{query}")])

# 分岐した処理のカスタム関数を定義
def add_synonyms(prompt: dict) -> dict:
    """同義語付きでプロンプトを加工"""
    query = prompt["query"]
    return {"query": f"Rust is FPS game.\n{query}", "name": prompt["name"]}


def pass_through(prompt: dict) -> dict:
    """そのままのプロンプトで処理"""
    return {"query": prompt["query"], "name": prompt["name"]}


add_synonyms_runnable = RunnableLambda(add_synonyms) | prompts | llm
pass_through_runnable = RunnableLambda(pass_through) | prompts | llm

# Parallel Runnableで並列処理の作成
parallel_runnable = RunnableParallel(
    with_synonyms=add_synonyms_runnable,
    without_synonyms=pass_through_runnable
)

input_data = {
    "query": "How to learn Rust?",
    "name": "Saori"
}


# 実行して結果を取得
result = parallel_runnable.invoke(input_data)

# 結果の出力
print("With Synonyms:", result["with_synonyms"])
print("Without Synonyms:", result["without_synonyms"])
