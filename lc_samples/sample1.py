import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from sample2 import Recipe

load_dotenv(dotenv_path="../.env")
api_key = os.environ.get("OPENAI_API_KEY")


def main(dish: str):
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    output_parser = PydanticOutputParser(pydantic_object=Recipe)
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

    prompt_value = prompt_with_format_instructions.invoke({"dish", dish})
    print("=== role: system ===")
    print(prompt_value.messages[0].content)
    print("=== role: user ===")
    print(prompt_value.messages[1].content)
    print("=== role: assistant ===")


    # print(prompt_value)

    # messages = [
    #     SystemMessage("You are a helpful assistant."),
    #     HumanMessage("こんにちは")
    # ]
    #

    result = ""
    for chunk in model.stream(prompt_value):
        print(chunk.content, end="", flush=True)
        result += chunk.content

    recipe = output_parser.parse(result)
    print(recipe)


if __name__ == "__main__":
    main("オムライス")
