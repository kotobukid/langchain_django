import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_openai import ChatOpenAI
from sample2 import Recipe

load_dotenv(dotenv_path="../.env")
api_key = os.environ.get("OPENAI_API_KEY")


def main(dish: str):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    output_parser = PydanticOutputParser(pydantic_object=Recipe)
    str_output_parser = StrOutputParser()
    format_instructions = output_parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "ユーザーが入力した料理のレシピを教えて下さい。\n\n" "{format_instructions}"),
            ("human", "{dish}")
        ]
    )

    prompt_with_format_instructions = prompt.partial(
        format_instructions=format_instructions
    )

    chain = prompt_with_format_instructions | model | str_output_parser

    ai_message = chain.invoke({"dish": dish})

    print(ai_message)

if __name__ == "__main__":
    main("冷や汁")
