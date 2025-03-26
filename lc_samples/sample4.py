from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

# Create a HumanMessagePromptTemplate directly from the template string
template_string = "Hello {name}"
human_message_template = HumanMessagePromptTemplate.from_template(template_string)

system_message_template = SystemMessagePromptTemplate.from_template("You are a helpful assistant.")


# Create the ChatPromptTemplate
prompts = ChatPromptTemplate.from_messages([
    system_message_template,
    human_message_template,
])

# Invoke the template with the required variables
texts = prompts.invoke({"name": "John"})

print(texts)