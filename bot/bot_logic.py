from .tools import some_helper_function

def process_with_bot(user_input):
    import os

    #os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
    #os.environ["SERPAPI_API_KEY"] = userdata.get("SERPAPI_API_KEY")

    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    from langchain.agents import AgentExecutor, create_openai_tools_agent
    from langchain.memory import ConversationBufferMemory
    from langchain_openai import OpenAI
    from langchain_openai import ChatOpenAI
    from langchain.agents import Tool
    from langchain.globals import set_debug

    set_debug(False)

    from langchain_community.utilities import SerpAPIWrapper

    params = {
        "num": 10
    }

    search = SerpAPIWrapper(params=params)

    def search_with_prefix(query):
        prefix = "site:kolzchut.org.il"
        full_query = f"{prefix} {query}"

        try:
            results = search.run(full_query)
            return results
        except Exception as e:
            # Log the error or perform any necessary error handling
            print(f"Error occurred: {str(e)}")
            # Return the assistant's response or perform any desired action
            return "I'm sorry, but I encountered an error. How else may I assist you?"

    # You can create the tool to pass to an agent
    kolzchut_tool = Tool(
        name="kolzchut_repl",
        description="השתמש בכלי זה רק במקרה של שאלה בנושא זכויות עובד או אזרח",
        func=search_with_prefix,
    )

    tools = [
        kolzchut_tool
    ]

    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature="0")

    from langchain.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant"),
            ("user", "{input}"),
            ("assistant", "Sure, I can assist you with that."),
            ("assistant", "{agent_scratchpad}"),
        ]
    )

    agent = create_openai_tools_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    response = agent_executor.invoke({"input": user_input})

    return response