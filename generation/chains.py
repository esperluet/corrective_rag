import logging
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from generation.llm_manager import get_llm
from generation.prompts import RAG_PROMPT, GRADING_PROMPT, SEARCH_REWRITE_PROMPT


def get_rag_chain():
    """
    Constructs a function for executing the RAG (Retrieval-Augmented Generation) logic.

    Returns:
        function: A callable that takes a question and documents as input, returning the generated response.
    """
    llm = get_llm()

    def rag_chain(question: str, documents: str) -> str:
        """
        Generates a response based on the provided question and retrieved documents.

        Args:
            question (str): The input question.
            documents (str): Concatenated content of the retrieved documents.

        Returns:
            str: The generated response.
        """
        try:
            rag_pipeline = RAG_PROMPT | llm | StrOutputParser()
            return rag_pipeline.invoke({'question': question, 'documents': documents})
        except Exception as e:
            logging.error(f"Error in RAG chain: {e}")
            return "An error occurred while generating the response."

    return rag_chain


def get_grading_chain():
    """
    Constructs a function for evaluating document relevance using the grading logic.

    Returns:
        function: A callable that takes a question and a fact as input, returning a dictionary with a relevance score.
    """
    llm = get_llm(output_format="json")

    def grading_chain(question: str, fact: str) -> dict:
        """
        Evaluates the relevance of a given document (fact) in relation to the question.

        Args:
            question (str): The question being asked.
            fact (str): A document or text passage to evaluate.

        Returns:
            dict: A dictionary containing a relevance score: {"score": "yes"} or {"score": "no"}.
        """
        try:
            retrieval_grader = GRADING_PROMPT | llm | JsonOutputParser()
            return retrieval_grader.invoke({'question': question, 'fact': fact})
        except Exception as e:
            logging.warning(f"Error in grading chain: {e}. Defaulting to 'no'.")
            return {"score": "no"}

    return grading_chain


def get_rewrite_web_search_chain():
    """
    Constructs a function for refining the web search query before executing a web search.

    Returns:
        function: A callable that takes a question as input and returns a refined search query.
    """
    llm = get_llm(output_format="json")

    def rewrite_web_search_chain(question: str) -> dict:
        """
        Rewrites a given question into a refined web search query.

        Args:
            question (str): The original user question.

        Returns:
            dict: A dictionary containing the rewritten query: {"query_search": <rewritten_query>}.
        """
        try:
            rewrite_pipeline = SEARCH_REWRITE_PROMPT | llm | JsonOutputParser()
            return rewrite_pipeline.invoke({'question': question})
        except Exception as e:
            logging.warning(f"Error in web search query rewriting: {e}. Using original question.")
            return {"query_search": question}

    return rewrite_web_search_chain
