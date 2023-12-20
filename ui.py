import streamlit as st
import openai
import os
from dotenv import load_dotenv
import requests

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def get_repository_info(repo_url):
    # Parse repository owner and name from URL
    parts = repo_url.split('/')
    owner = parts[-2]
    repo_name = parts[-1].replace('.git', '')  # Remove .git if present

    # Make API request to get repository details
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}")
    if response.status_code != 200:
        return None
    repository_info = response.json()

    return {
        'name': repository_info['name'],
        'description': generate_repo_description(repo_url),
        'clone_url': repository_info['clone_url'],
        'stars': repository_info['stargazers_count'],
        'forks': repository_info['forks_count'],
        'watchers': repository_info['watchers_count'],
        'size': repository_info['size'],
        'last_edit_date': repository_info['pushed_at'],
        'commits': repository_info['default_branch'],
        'contributors': get_repository_contributors(owner, repo_name)
    }


def get_repository_contributors(owner, repo_name):
    # Make API request to get repository contributors
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo_name}/contributors")
    if response.status_code != 200:
        return None
    contributors = response.json()

    return contributors


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
        repository_info = get_repository_info(repo_url)
        if repository_info:
            st.subheader("Repository Information")
            st.write(f"Name: {repository_info['name']}")
            st.write(f"Description: {repository_info['description']}")
            st.write(f"Clone URL: {repository_info['clone_url']}")
            st.write(f"Stars: {repository_info['stars']}")
            st.write(f"Forks: {repository_info['forks']}")
            st.write(f"Watchers: {repository_info['watchers']}")
            st.write(f"Size: {repository_info['size']} KB")
            st.write(f"Last Edit Date: {repository_info['last_edit_date']}")
            st.write(f"Number of Commits: {repository_info['commits']}")
            contributors = repository_info['contributors']
            if contributors:
                st.write("Contributors: ")
                for contributor in contributors:
                    st.write(f"- {contributor['login']}")
            else:
                st.write("Contributors: None")
        else:
            st.error("Failed to fetch repository details")
    else:
        st.warning("Please enter a repository URL")


if __name__ == "__main__":
    main()
