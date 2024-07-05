from langchain_community.llms import Ollama

def generate_job_description(input_data):
    # Load the Ollama model (replace with the actual model setup)
    llm = Ollama(model="llama2")
    
    
        
        # Build a prompt (structure is important for LLaMA)
    prompt = (
        f"Job Title: {input_data['title']}\n"
        f"Requirements: {input_data['requirements']}\n"
        f"work_location: {input_data['work_location']}\n"
        f"seniority : {input_data['work_location']}\n"
        f"Please write a job description based on the information above."
    )
    

    
    generated_text = llm.invoke(prompt)
    return (generated_text)