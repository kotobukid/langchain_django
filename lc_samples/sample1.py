from langchain_core.messages import SystemMessage, HumanMessage


def main():
    messages = [
        SystemMessage("You are a helpful assistant."),
        HumanMessage("こんにちは")
    ]

    print(messages)


if __name__ == "__main__":
    main()
