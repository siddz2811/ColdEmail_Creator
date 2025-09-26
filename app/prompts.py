from langchain_core.prompts import PromptTemplate

extract_prompt = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM WEBSITE:
    {page_data}
    ### INSTRUCTION:
    The scraped text is from the career's page of a website.
    Your job is to extract the job postings and return them in JSON format containing the
    following keys: `role`, `experience`, `skills` and `description`.
    Only return the valid JSON.
    ### VALID JSON (NO PREAMBLE):
    """
)

email_prompt = PromptTemplate.from_template(
    """
    ### JOB DESCRIPTION:
    {job_description}

    ### PORTFOLIO LINKS:
    {link_list}

    ### REFERENCE ABOUT YOURSELF:
    {user_prompt}

    ### INSTRUCTION:
    Write a cold email to the client regarding the job mentioned above, describing the capability of yourself in fulfilling their needs.
    Use the info in the 'REFERENCE ABOUT YOURSELF' section to personalize the email.
    ### EMAIL (NO PREAMBLE):
    """
)