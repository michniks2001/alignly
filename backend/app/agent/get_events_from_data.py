from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from typing import List, Tuple
from langchain_core.agents import AgentActionMessageLog, AgentFinish
import json
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.tools.retriever import create_retriever_tool
from langchain_community.retrievers import WikipediaRetriever
import dotenv
import os

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

retriever = WikipediaRetriever()

retriever_tool = create_retriever_tool(
    retriever,
    "state-of-union-retriever",
    "Query a retriever to get information about state of the union address",
)


class Response(BaseModel):
    """Final response to the question being asked"""
    event_date: List[str] = Field(description="The date the event will happen")
    event_title: List[str] = Field(description="The title of event")
    event_description: List[str] = Field(description="The description of event")

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

def transform_event_data(data):
    """
    Transform event data from parallel arrays format to a list of event dictionaries.
    
    Args:
        data (dict): Dictionary with 'event_date' and 'event_title' as parallel arrays
        
    Returns:
        list: List of dictionaries, each containing 'date' and 'title' for an event
    """
    return [
        {
            "date": date,
            "title": title,
            "description": description
        }
        for date, title, description in zip(data['event_date'], data['event_title'], data['event_description'])
    ]


def parse(output):
    # If no function was invoked, return to user
    if "function_call" not in output.additional_kwargs:
        return AgentFinish(return_values={"output": output.content}, log=output.content)

    # Parse out the function call
    function_call = output.additional_kwargs["function_call"]
    name = function_call["name"]
    inputs = json.loads(function_call["arguments"])

    # If the Response function was invoked, return to the user with the function inputs
    if name == "Response":
        return AgentFinish(return_values=inputs, log=str(function_call))
    # Otherwise, return an agent action
    else:
        return AgentActionMessageLog(
            tool=name, tool_input=inputs, log="", message_log=[output]
        )
    

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Any date should be written in a parsable format."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm = ChatOpenAI(temperature=0)

llm_with_tools = llm.bind_functions([retriever_tool, Response])

agent = (
    {
        "input": lambda x: x["input"],
        # Format agent scratchpad from intermediate steps
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | parse
)

agent_executor = AgentExecutor(tools=[retriever_tool], agent=agent, verbose=True)

data = agent_executor.invoke(
    # {"input": "what did the president say about ketanji brown jackson"},
    {"input": "You have homework due on the 21st of november 2024 and a test on the 22nd of november 2024"},
    return_only_outputs=True,
)

new_data = transform_event_data(data)


# def output_agent_results(agent_executor,note_data):
#     """
#     Output the results of the agent to the console.
    
#     Args:
#         data (dict): The data returned by the agent
#     """
#     data = agent_executor.invoke(
#         {"input":note_data},
#         return_only_outputs=True,
#     )

#     data = transform_event_data(data)
#     return data

def output_agent_results(agent_executor, note_data):
    """
    Output the results of the agent to the console.
    
    Args:
        data (dict): The data returned by the agent
    """
    try:
        data = agent_executor.invoke(
            {"input": note_data},
            return_only_outputs=True,
        )

        # Return empty dict if data is string
        if isinstance(data, str):
            return {}
            
        data = transform_event_data(data)
        return data
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        return {}


if __name__ == "__main__":
    resi = output_agent_results(agent_executor,"You have homework due on the 21st of november 2024 and a test on the 22nd of november 2024")

    x= 0

