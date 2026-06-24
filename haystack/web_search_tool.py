#
# API key is required from https://serper.dev/
# In .env file, set API key to SERPERDEV_API_KEY=

from haystack.tools import ComponentTool
from haystack.components.websearch import SerperDevWebSearch
from haystack.components.generators.utils import print_streaming_chunk
from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage, Document

def doc_to_string(documents) -> str:
    result_str = ""
    for document in documents:
        result_str += f"Content for {document.meta['link']}: {document.content}\n\n"
    return result_str

search_tool = ComponentTool(
    component=SerperDevWebSearch(top_k=5),
    name="web_search_tool",
    description="Search the web",
    outputs_to_string={"source": "documents", "handler": doc_to_string}, 
    outputs_to_state={"documents": {"source": "documents"}}
)

agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    system_prompt="""
    You are a helpful AI assistant that has access to internet.
    Keep your answer concise and use the tools that you're provided with to answer the user's questions.
    """,
    tools=[search_tool],
    state_schema={"documents":{"type":list[Document]}}, 
    streaming_callback=print_streaming_chunk 
)

agent_results = agent.run(messages=[ChatMessage.from_user("What are the common side effects of hyaluronic acid?")])
print(agent_results)

print(agent_results["documents"])
