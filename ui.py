import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_repo_description(repo_url):
    openai.api_key = openai_api_key

    prompt = f"Describe the repository at {repo_url}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )

    if response['choices'][0]['finish_reason'] == 'stop':
        description = response['choices'][0]['text']
        return description
    else:
        return None

def main():
    st.title("GitHub Repository Description Generator")

    # Repository input
    repo_url = st.text_input("Enter the GitHub repository URL")
    if repo_url:
        description = generate_repo_description(repo_url)
        if description:
            st.subheader("Repository Description")
            st.write(description)
        else:
            st.error("Failed to generate repository description")

if __name__ == "__main__":
    main()