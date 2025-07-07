#!/usr/bin/env python3
"""
Create GitHub Repository Script

Creates a new GitHub repository for the Repo-Tools project.
"""
import os
import sys
from pathlib import Path

try:
    from github import Github, GithubException
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)

def create_github_repo():
    """Create a new GitHub repository."""
    # Load environment variables
    load_dotenv()
    
    # Get GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ Error: GITHUB_TOKEN not found in environment variables")
        print("Please set your GitHub token in .env file or environment")
        return False
    
    try:
        # Initialize GitHub client
        g = Github(token)
        user = g.get_user()
        
        print(f"✓ Authenticated as: {user.login}")
        
        # Repository details
        repo_name = "Repo-Tools"
        description = "Python scripts for managing GitHub repositories: list, backup, and privacy management tools"
        
        # Check if repository already exists
        try:
            existing_repo = user.get_repo(repo_name)
            print(f"⚠️  Repository '{repo_name}' already exists at: {existing_repo.html_url}")
            return True
        except GithubException as e:
            if e.status != 404:
                print(f"❌ Error checking existing repository: {e}")
                return False
        
        # Create the repository
        print(f"🔄 Creating repository '{repo_name}'...")
        
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=False,  # Making it public - change to True if you want it private
            has_issues=True,
            has_projects=False,
            has_wiki=False,
            auto_init=False  # We already have files
        )
        
        print(f"✅ Repository created successfully!")
        print(f"📍 Repository URL: {repo.html_url}")
        print(f"📍 Clone URL: {repo.clone_url}")
        print(f"📍 SSH URL: {repo.ssh_url}")
        
        return True
        
    except GithubException as e:
        print(f"❌ GitHub API Error: {e.data.get('message', str(e))}")
        return False
    except Exception as e:
        print(f"❌ Error creating repository: {str(e)}")
        return False

if __name__ == "__main__":
    success = create_github_repo()
    if success:
        print("\n🎉 Next steps:")
        print("1. Add the remote origin to your local repository")
        print("2. Push your code to the new repository")
        print("\nCommands to run:")
        print("git remote add origin https://github.com/YOUR_USERNAME/Repo-Tools.git")
        print("git branch -M main")
        print("git push -u origin main")
    else:
        sys.exit(1)
