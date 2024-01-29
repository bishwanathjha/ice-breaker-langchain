from langchain.agents import Tool, initialize_agent, AgentType, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    template = """given the full name {name_of_person} I want you to get a link to their Linkedin profile page.
                Your answer should contain only a URL"""

    tools_for_agent = [
        Tool(
            name="Crawl google for Linkedin profile page",
            func=get_profile_url,
            description="useful for when you need to get the linkedin page url ",
        )
    ]

    # Initialize and use an agent with the custom tool
    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    linkedin_profile_url = agent.run(prompt_template.format_prompt(name_of_person=name))
    return linkedin_profile_url
