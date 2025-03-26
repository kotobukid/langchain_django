from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
from .models import DesignedPrompt
from langchain_openai import ChatOpenAI
from typing import List, Dict
import re

load_dotenv(dotenv_path="../.env")


def trim_template_string(template_string: str) -> str:
    """
    テンプレート文字列の {key} 内に存在する不必要なスペースを削除する。
    例: { item1 } → {item1}
    """
    # 正規表現で { } 内のスペースを削除
    template_string = re.sub(r"{\s*(\w+)\s*}", r"{\1}", template_string)
    return template_string


def query_pattern1(dp: DesignedPrompt, input_data: dict) -> List[Dict[str, str]]:
    # DesignedPromptからテンプレート取得
    template_string = trim_template_string(dp.template)

    # HumanMessagePromptTemplateに基づきメッセージテンプレートを生成
    human_message_template = HumanMessagePromptTemplate.from_template(template_string)

    # input_dataをテンプレートに埋め込む
    try:
        rendered_human_message = human_message_template.format(**input_data)
    except KeyError as e:
        raise ValueError(f"Missing key in input_data: {e}")
    print("Rendered Human Message:", rendered_human_message)

    # Systemメッセージを作成
    system_message = SystemMessagePromptTemplate.from_template("You are a helpful assistant. Answer in japanese.")
    system_message_gal = SystemMessagePromptTemplate.from_template(
        "You are a playful assistant. Respond with a fun, friendly, and 'neko-chan' style tone in Japanese."
    )

    # ChatPromptTemplateを作成
    chat_prompt = ChatPromptTemplate.from_messages([
        system_message,
        HumanMessagePromptTemplate.from_template(rendered_human_message.content)
    ])
    chat_prompt_gal = ChatPromptTemplate.from_messages([
        system_message_gal,
        HumanMessagePromptTemplate.from_template(rendered_human_message.content)
    ])

    # LLMと出力パーサーを設定
    # llm0 = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    llm2 = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

    output_parser = StrOutputParser()

    # 分岐処理カスタム関数を定義
    def pass_through(prompt: str) -> dict:
        """そのままのプロンプトで処理"""
        return {"query": prompt}

    def like_gal(prompt: str) -> dict:
        """ギャルっぽい口調を生成"""
        return {"query": f"ノリノリなギャル語でよろ～☆ 質問文: {prompt}"}

    def like_kitten(prompt: str) -> dict:
        """猫語っぽい口調を生成"""
        return {"query": f"超カワな猫ちゃん語でさ、めっちゃフレンドリーに答えてほしいの♡ 質問文: {prompt}"}

    # Runnable定義
    gal_runnable = (
            pass_through  # 入力をそのまま渡す
            | RunnableLambda(like_gal)  # ギャルメッセージ生成
            | chat_prompt_gal  # ギャルメッセージをプロンプト内に挿入
            | llm2  # プロンプトからLLMで処理
            | output_parser  # LLMの出力を解析
            | RunnableLambda(lambda result: {"style": "gal", "text": result})
    )

    pass_through_runnable = (
            pass_through  # 入力をそのまま渡す
            | chat_prompt  # 標準メッセージ（人間のメッセージ）をプロンプト内に挿入
            | llm2  # プロンプトからLLMで処理
            | output_parser  # LLMの出力を解析
            | RunnableLambda(lambda result: {"style": "normal", "text": result})
    )

    # 並列処理Runnable作成
    parallel_runnable = RunnableParallel(
        gal=gal_runnable,
        normal=pass_through_runnable
    )

    runnable_input = rendered_human_message

    # 入力データに対して並列処理を実行
    results = parallel_runnable.invoke(runnable_input.content)

    # 処理結果を返す
    return list(results.values())
