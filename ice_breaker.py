from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

from langchain_core.prompts import PromptTemplate
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    load_dotenv()
    print("Hello LangChain!")

    summary_template = """
        given the Linkedin information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

    # Create prompt template
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # Create the LLM and chain objects
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # Let the agent search for the given name and return the linkedIN url
    linkedin_profile_url = linkedin_lookup_agent(name="Bishwanath Jha Klarna")

    # Get the user data from the linkedIN scrape API
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)

    # Let's pass the retrieved linkedIN data into prompt template variable ang get the response
    response = chain.invoke(input={"information": linkedin_data})

    print(response.get("text"))
