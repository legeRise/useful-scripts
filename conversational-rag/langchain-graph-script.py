
from langgraph.graph import START, StateGraph
from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState, StateGraph
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from custom_tools import CUSTOM_TOOLS
import constants 
llm = ChatGroq(model=constants.LLM_MODEL)
memory = MemorySaver()
config = {"configurable": {"thread_id": "abc123"}}




# Step 1: Generate an AIMessage that may include a tool-call to be sent.
def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = llm.bind_tools(CUSTOM_TOOLS)
    response = llm_with_tools.invoke(state["messages"])
    # MessagesState appends messages to state instead of overwriting
    return {"messages": [response]}


# Step 2: Execute the retrieval.
tools = ToolNode(CUSTOM_TOOLS)


# Step 3: Generate a response using the retrieved content.
def generate(state: MessagesState):
    """Generate answer."""
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        ""
        "You are an helpful assistant for question-answering"
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        f"{docs_content}"
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = llm.invoke(prompt)
    return {"messages": [response]}





workflow = StateGraph(MessagesState)  # a special type of graph(graph is empty at the beginnign)

# add nodes 
workflow.add_node(query_or_respond)  # node 1:   a function to decide whether to search the rag or directly respond
workflow.add_node(tools)  # node 2: available tools(functions) that llm will be calling(comes from last AI message)
workflow.add_node(generate)   # node 3: a function generate that generates the file response


# set entry_point of workflow, where the workflow will start from
workflow.set_entry_point("query_or_respond")  # as soon as user enters something(input) it passes through node one to decide whether to deal it directly or query the rag


workflow.add_conditional_edges(  # edge: shows the flow like after executing node1 where to go? This is a conditional edge 
    "query_or_respond",  #    the point where condition will execute  
    tools_condition,  # the actual condition 'tools_condition' which means if there are any tools in the response of conditon it goes there else ENDS
    {END: END, "tools": "tools"},
)
workflow.add_edge("tools", "generate")  # edge: tells that once tools have been executed response goes to generate and it utilizes that to ge the file answer
workflow.add_edge("generate", END) # last edge that tells that after generation is complete the flow ends

graph = workflow.compile(checkpointer=memory)




# from IPython.display import Image, display

# display(Image(graph.get_graph().draw_mermaid_png()))



while True:
    input_message = input("Ask Rag: ")
    for step in graph.stream(
        {"messages": [{"role": "user", "content": input_message}]},
        stream_mode="values",
        config = config
    ):
        step["messages"][-1].pretty_print()
