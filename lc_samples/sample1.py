import os
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

load_dotenv(dotenv_path="../.env")
api_key = os.environ.get("OPENAI_API_KEY")


def main():
    # model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}")
        ]
    )

    prompt_value = prompt.invoke({
        "chat_history": [
            HumanMessage("こんにちは！私はジョンといいます！"),
            AIMessage("こんにちは、ジョンさん！どのようにお手伝いできますか？")
        ],
        "input": "私の名前がわかりますか？"
    })

    print(prompt_value)

    # messages = [
    #     SystemMessage("You are a helpful assistant."),
    #     HumanMessage("こんにちは")
    # ]
    #
    # for chunk in model.stream(messages):
    #     print(chunk.content, end="", flush=True)


if __name__ == "__main__":
    main()
