import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv(dotenv_path="../.env")
api_key = os.environ.get("OPENAI_API_KEY")


def main():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = PromptTemplate.from_template("""以下の料理のレシピを教えて下さい。
    
    料理名: {dish}""")

    prompt_value = prompt.invoke({"dish": "カレー"})

    print(prompt_value.text)

    # messages = [
    #     SystemMessage("You are a helpful assistant."),
    #     HumanMessage("こんにちは")
    # ]
    #
    # for chunk in model.stream(messages):
    #     print(chunk.content, end="", flush=True)


if __name__ == "__main__":
    main()
