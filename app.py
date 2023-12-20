import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_description(repo_url):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"Generate a description for a GitHub repository.\n\nURL: {repo_url}\n\nDescription:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None
    )

    if response and response.choices:
        description = response.choices[0].text.strip()
        return description

    return None

def main():
    repo_url = input("Enter the GitHub repository URL: ")
    description = generate_description(repo_url)

    if description:
        print(f"Description: {description}")
    else:
        print("Failed to generate repository description.")

if __name__ == "__main__":
    main()