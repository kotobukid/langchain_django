from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from sample2 import Recipe

load_dotenv(dotenv_path="../.env")


def main(dish: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm.bind(
        response_format={"type": "json_object"}
    )

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

    chain = prompt_with_format_instructions | llm.with_structured_output(Recipe)

    ai_message = chain.invoke({"dish": dish})

    print(ai_message)


if __name__ == "__main__":
    main("カレーうどん")
