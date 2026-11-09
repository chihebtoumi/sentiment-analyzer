import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel

load_dotenv()


def build_chain():
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        temperature=0,
    )
    parser = StrOutputParser()

    sentiment_template = ChatPromptTemplate.from_template(
        "In a single word, either 'positive', 'negative' or 'neutral', "
        "provide the overall sentiment of the following piece of text: {text}"
    )
    main_topic_template = ChatPromptTemplate.from_template(
        "Identify and state, as concisely as possible, the main topic of the "
        "following piece of text. Only provide the main topic and no other "
        "helpful comments. Text: {text}"
    )
    followup_template = ChatPromptTemplate.from_template(
        "What is an appropriate and interesting followup question that would "
        "help me learn more about the provided text? Only supply the question. "
        "Text: {text}"
    )

    prep = RunnableLambda(lambda text: {"text": text})

    parallel = RunnableParallel(
        {
            "statement": RunnableLambda(lambda x: x["text"]),
            "sentiment": sentiment_template | llm | parser,
            "main_topic": main_topic_template | llm | parser,
            "followup": followup_template | llm | parser,
        }
    )
    return prep | parallel