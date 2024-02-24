from typing import Tuple

from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

from langchain_core.prompts import PromptTemplate
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from output_parser import person_intel_parser, PersonIntel


def ice_breaker(name: str) -> Tuple[PersonIntel, str]:
    # Let the agent search for the given name and return the linkedIN url and get data from its scrape API
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    # Let the agent search for the given name and return the twitter url and get data from its scrape API
    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username, num_tweets=5)

    summary_template = """
            given the Linkedin information {linkedin_information} and twitter information {twitter_information} about a person from I want you to create:
            1. a short summary
            2. two interesting facts about them
            3. A topic that may interest them
            4. 2 creative Ice breakers to open a conversation with them 
            \n {format_instructions}
        """

    # Create prompt template
    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "twitter_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    # Create the LLM and chain objects
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # Let's pass the retrieved linkedIN and twitter data into prompt template variable ang get the response
    response = chain.invoke(
        input={"linkedin_information": linkedin_data, "twitter_information": tweets}
    )

    return person_intel_parser.parse(response["text"]), linkedin_data["profile_pic_url"]


if __name__ == "__main__":
    load_dotenv()
    print("Hello LangChain!")

    # The persona name that lookup to perform
    name = "Bishwanath Jha Klarna"

    result = ice_breaker(name=name)

    print(f"Result for {name} is: {result}")
