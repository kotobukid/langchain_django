from langchain_community.document_loaders import GitLoader
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv(dotenv_path="../.env")


def file_filter(file_path: str) -> bool:
    return file_path.endswith(".mdx")


def main():
    loader = GitLoader(
        clone_url="https://github.com/langchain-ai/langchain.git",
        repo_path="./langchain",
        branch="master",
        file_filter=file_filter
    )

    raw_docs = loader.load()
    # print(len(raw_docs))

    for doc in raw_docs:
        print(doc.metadata)
        print(doc.page_content)
        print("=" * 100)

    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    #
    # query = "crates.ioからデータを読み込むためのDocumentLoaderはありますか？"
    #
    # vector = embeddings.embed_query(query)
    # print(len(vector))
    # print(vector)
    #
    # db = Chroma.from_documents(raw_docs, embeddings)
    #
    # retriever = db.as_retriever()
    # context_docs = retriever.invoke(query)
    #
    # print(f"len = {len(context_docs)}")
    #
    # first_doc = context_docs[0]
    # print(f"metadata = {first_doc.metadata}")
    # print(first_doc.page_content)


if __name__ == "__main__":
    main()
