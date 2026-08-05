from langchain.prompts import PromptTemplate

def prompt_sector(position: str, prompts: classmethod) -> dict:

    """ Select the prompt template based on the position """

    if position == 'Data Analyst':
        PROMPT = PromptTemplate(
            template=prompts.da_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}

    elif position == 'Software Engineer':
        PROMPT = PromptTemplate(
            template=prompts.swe_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}

    elif position == 'Marketing':
        PROMPT = PromptTemplate(
            template=prompts.marketing_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}

    elif position == 'Front End':
        PROMPT = PromptTemplate(
            template=prompts.front_end_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}

    elif position == 'Back End':
        PROMPT = PromptTemplate(
            template=prompts.back_end_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}

    elif position == 'Full Stack':
        PROMPT = PromptTemplate(
            template=prompts.full_stack_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}

    elif position == 'QA':
        PROMPT = PromptTemplate(
            template=prompts.qa_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}

    elif position == 'SWE Intern':
        PROMPT = PromptTemplate(
            template=prompts.swe_intern_template, input_variables=["context", "question"]
        )
        chain_type_kwargs = {"prompt": PROMPT}

    else:
        raise ValueError(f"Unsupported position: {position}")

    return chain_type_kwargs
