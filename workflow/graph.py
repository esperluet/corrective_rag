import logging
from langchain.schema import Document
from langgraph.graph import START, END, StateGraph

from utils.types import GraphState
from generation.chains import (
    get_rag_chain,
    get_grading_chain,
    get_rewrite_web_search_chain,
)
from langchain_community.tools.tavily_search import TavilySearchResults


def retrieve(state: GraphState) -> GraphState:
    """
    Step 1: Retrieves documents using the retriever defined in the state.

    Args:
        state (GraphState): The current graph state.

    Returns:
        GraphState: Updated state with retrieved documents.
    """
    question = state["question"]
    retriever = state["retriever"]
    documents = retriever.retrieve(question)
    steps = state["steps"] + ["retrieve_documents"]

    return {**state, "documents": documents, "steps": steps}


def grade_documents(state: GraphState) -> GraphState:
    """
    Step 2: Evaluates the relevance of retrieved documents using the grading chain.
    If documents are not relevant, sets 'search' to "Yes".

    Args:
        state (GraphState): The current graph state.

    Returns:
        GraphState: Updated state with filtered documents and a search flag.
    """
    question = state["question"]
    documents = state["documents"]
    steps = state["steps"] + ["grade_document_retrieval"]

    grading_chain = get_grading_chain()

    filtered_docs = []
    search_needed = "No"

    for doc in documents:
        # Calls the grading chain to determine relevance
        result = grading_chain(question, doc.page_content)
        if result.get("score") == "yes":
            filtered_docs.append(doc)
        else:
            search_needed = "Yes"
        
        score = result.get("score")
        logging.warning(f"Grading step :  Result {result}; Grading score is : {score} - search_needed : {search_needed}?")

    logging.warning(f"Grading step \n Nb relevants docs : {len(filtered_docs)}. -  nb irrelevants docs :   {len(documents) - len(filtered_docs)}")
    return {**state, "documents": filtered_docs, "search": search_needed, "steps": steps}


def decide_to_generate(state: GraphState) -> str:
    """
    Conditional decision:
    - If 'search' = "Yes", proceed to the "web_search" node.
    - Otherwise, proceed to "generate".

    Args:
        state (GraphState): The current graph state.

    Returns:
        str: Next node to execute.
    """
    return "search" if state["search"] == "Yes" else "generate"


def rewrite_web_search_query(state: GraphState) -> GraphState:
    """
    Step 3 (if needed): Rewrites the search query before performing a web search.

    Args:
        state (GraphState): The current graph state.

    Returns:
        GraphState: Updated state with rewritten search query.
    """
    question = state["question"]
    steps = state["steps"] + ["rewrite_web_search_query"]

    rewrite_web_search_chain = get_rewrite_web_search_chain()

    try:
        result = rewrite_web_search_chain(question=question)
        web_search_query = result['query_search']
    except Exception as e:
        logging.warning(f"Query rewriting failed: {e}. Falling back to original question.")
        web_search_query = question

    logging.warning(f"User query rewriting for web search performed ; Initial version : {question} ; rewrite version : {result}")

    return {**state, "web_search_query": web_search_query, "steps": steps}


def web_search(state: GraphState) -> GraphState:
    """
    Step 4 (if needed): Performs a web search using TavilySearch.

    Args:
        state (GraphState): The current graph state.

    Returns:
        GraphState: Updated state with additional web search documents.
    """
    web_search_query = state["web_search_query"]
    documents = state["documents"]
    steps = state["steps"] + ["web_search"]

    tavily_tool = TavilySearchResults(k=3)
    results = tavily_tool.invoke({"query": web_search_query})

    logging.warning(f"Performing web search with query: {web_search_query}")

    new_documents = [
        Document(page_content=r["content"], metadata={"url": r["url"]}) for r in results
    ]
    documents.extend(new_documents)

    return {**state, "documents": documents, "steps": steps}


def generate_answer(state: GraphState) -> GraphState:
    """
    Step 5: Generates the final answer using a RAG chain.

    Args:
        state (GraphState): The current graph state.

    Returns:
        GraphState: Updated state with the generated response.
    """
    question = state["question"]
    documents = state["documents"]
    steps = state["steps"] + ["generate_answer"]

    # Concatenates retrieved documents
    docs_text = "\n".join(d.page_content for d in documents)
    rag_chain = get_rag_chain()
    answer = rag_chain(question, docs_text)

    return {**state, "generation": answer, "steps": steps}


# Graph Construction
workflow = StateGraph(GraphState)

# Define nodes
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("rewrite_web_search_query", rewrite_web_search_query)
workflow.add_node("web_search", web_search)
workflow.add_node("generate", generate_answer)

# Define graph structure
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "search": "rewrite_web_search_query",
        "generate": "generate",
    },
)
workflow.add_edge("rewrite_web_search_query", "web_search")
workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", END)

# Compile
custom_graph = workflow.compile()


def run_workflow(question: str, retriever=None) -> GraphState:
    """
    Runs the entire workflow by creating the initial state.

    Args:
        question (str): The input question.
        retriever (optional): The document retriever.

    Returns:
        GraphState: The final state after executing the workflow.
    """
    initial_state: GraphState = {
        "question": question,
        "generation": "",
        "web_search_query": question,
        "search": "No",
        "documents": [],
        "steps": [],
        "retriever": retriever,
    }

    return custom_graph.invoke(initial_state)
