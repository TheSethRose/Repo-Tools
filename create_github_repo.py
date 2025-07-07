#!/usr/bin/env python3
"""
GitHub Repository Creation Script

Creates a new GitHub repository for the Repo-Tools project.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

try:
    from github import Github, GithubException
    from rich.console import Console
    from rich.prompt import Confirm
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)


def create_github_repository(
    token: str,
    repo_name: str = "Repo-Tools",
    description: str = "Python scripts for managing GitHub repositories - listing, privacy management, and backup tools",
    private: bool = False
) -> bool:
    """Create a new GitHub repository."""
    console = Console()
    
    try:
        # Initialize GitHub client
        github = Github(token)
        user = github.get_user()
        
        console.print(f"Creating repository: [bold blue]{repo_name}[/bold blue]")
        console.print(f"Description: {description}")
        console.print(f"Private: {private}")
        
        # Check if repository already exists
        try:
            existing_repo = user.get_repo(repo_name)
            console.print(f"[bold yellow]Repository '{repo_name}' already exists![/bold yellow]")
            console.print(f"URL: {existing_repo.html_url}")
            return True
        except GithubException as e:
            if e.status != 404:
                raise e
            # Repository doesn't exist, which is what we want
            pass
        
        # Create the repository
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=private,
            has_issues=True,
            has_wiki=False,
            has_downloads=True,
            has_projects=False,
            auto_init=False  # We already have local files
        )
        
        console.print(f"✓ Repository created successfully!")
        console.print(f"URL: [bold green]{repo.html_url}[/bold green]")
        console.print(f"Clone URL: {repo.clone_url}")
        console.print(f"SSH URL: {repo.ssh_url}")
        
        return True
        
    except GithubException as e:
        console.print(f"[bold red]✗ GitHub API Error:[/bold red] {e.data.get('message', str(e))}")
        return False
    except Exception as e:
        console.print(f"[bold red]✗ Error creating repository:[/bold red] {str(e)}")
        return False


def setup_git_remote(repo_name: str = "Repo-Tools") -> bool:
    """Set up git remote for the new repository."""
    console = Console()
    
    try:
        # Get GitHub username from git config
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            check=True
        )
        username = result.stdout.strip()
        
        if not username:
            console.print("[bold red]✗ Could not determine GitHub username from git config[/bold red]")
            return False
        
        # Add remote origin
        remote_url = f"git@github.com:{username}/{repo_name}.git"
        
        # Check if remote already exists
        try:
            subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                check=True
            )
            console.print("[bold yellow]Remote 'origin' already exists[/bold yellow]")
            
            # Ask if user wants to update it
            if Confirm.ask("Update remote origin URL?"):
                subprocess.run(
                    ["git", "remote", "set-url", "origin", remote_url],
                    check=True
                )
                console.print(f"✓ Updated remote origin to: {remote_url}")
            return True
            
        except subprocess.CalledProcessError:
            # Remote doesn't exist, add it
            subprocess.run(
                ["git", "remote", "add", "origin", remote_url],
                check=True
            )
            console.print(f"✓ Added remote origin: {remote_url}")
            return True
            
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]✗ Git command failed:[/bold red] {e}")
        return False
    except Exception as e:
        console.print(f"[bold red]✗ Error setting up git remote:[/bold red] {str(e)}")
        return False


def main():
    """Main function to create GitHub repository and set up remote."""
    console = Console()
    
    # Load environment variables
    load_dotenv()
    
    # Get GitHub token
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        console.print("[bold red]✗ GITHUB_TOKEN environment variable not set[/bold red]")
        console.print("Please set your GitHub Personal Access Token:")
        console.print("export GITHUB_TOKEN='your_token_here'")
        sys.exit(1)
    
    console.print("[bold blue]GitHub Repository Creation[/bold blue]")
    console.print("=" * 40)
    
    # Ask user for repository details
    repo_name = "Repo-Tools"
    description = "Python scripts for managing GitHub repositories - listing, privacy management, and backup tools"
    
    console.print(f"Repository name: {repo_name}")
    console.print(f"Description: {description}")
    
    # Ask if repository should be private
    private = Confirm.ask("Make repository private?", default=False)
    
    # Create the repository
    if create_github_repository(token, repo_name, description, private):
        console.print("\n[bold green]Repository created successfully![/bold green]")
        
        # Set up git remote
        if setup_git_remote(repo_name):
            console.print("\n[bold green]Git remote configured![/bold green]")
            console.print("\nNext steps:")
            console.print("1. git add .")
            console.print("2. git commit -m 'Initial commit: GitHub repository management tools'")
            console.print("3. git push -u origin main")
        else:
            console.print("\n[bold yellow]Repository created but git remote setup failed[/bold yellow]")
            console.print("You can manually add the remote with:")
            console.print(f"git remote add origin git@github.com:YOUR_USERNAME/{repo_name}.git")
    else:
        console.print("\n[bold red]Failed to create repository[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
