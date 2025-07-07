#!/usr/bin/env python3
"""
GitHub Repository Creation Script

A dynamic script to create new GitHub repositories from the command line.
Supports custom repository names, descriptions, and various GitHub settings.

Usage:
    python create_github_repo.py [options]

Arguments:
    --name: Repository name (optional, interactive prompt if not provided)
    --description: Repository description (optional)
    --private: Make repository private (default: False)
    --auto-init: Initialize with README (default: False for existing projects)
    --has-issues: Enable issues (default: True)
    --has-wiki: Enable wiki (default: False)
    --has-projects: Enable projects (default: False)

Examples:
    # Interactive mode
    python create_github_repo.py
    
    # With parameters
    python create_github_repo.py --name "MyProject" --description "My awesome project" --private
    
    # Initialize new project with README
    python create_github_repo.py --name "NewProject" --auto-init
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

try:
    from github import Github, GithubException
    from rich.console import Console
    from rich.prompt import Confirm, Prompt
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)


def create_github_repository(
    token: str,
    repo_name: str,
    description: str = "",
    private: bool = False,
    has_issues: bool = True,
    has_wiki: bool = False,
    has_projects: bool = False,
    auto_init: bool = False
) -> bool:
    """Create a new GitHub repository with specified settings."""
    console = Console()
    
    try:
        # Initialize GitHub client
        github = Github(token)
        user = github.get_user()
        
        console.print(f"Creating repository: [bold blue]{repo_name}[/bold blue]")
        console.print(f"Description: {description or 'No description'}")
        console.print(f"Private: {private}")
        console.print(f"Issues: {has_issues}, Wiki: {has_wiki}, Projects: {has_projects}")
        
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
            has_issues=has_issues,
            has_wiki=has_wiki,
            has_downloads=True,
            has_projects=has_projects,
            auto_init=auto_init
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
    """Main function to create GitHub repository with command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Create a new GitHub repository",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_github_repo.py --name "MyProject" --description "My awesome project"
  python create_github_repo.py --name "PrivateRepo" --private
  python create_github_repo.py --name "NewProject" --auto-init
        """
    )
    
    parser.add_argument("--name", help="Repository name")
    parser.add_argument("--description", help="Repository description", default="")
    parser.add_argument("--private", action="store_true", help="Make repository private")
    parser.add_argument("--auto-init", action="store_true", help="Initialize with README")
    parser.add_argument("--no-issues", action="store_true", help="Disable issues")
    parser.add_argument("--enable-wiki", action="store_true", help="Enable wiki")
    parser.add_argument("--enable-projects", action="store_true", help="Enable projects")
    parser.add_argument("--setup-remote", action="store_true", help="Set up git remote after creation")
    
    args = parser.parse_args()
    
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
    
    # Get repository details interactively if not provided
    repo_name = args.name
    if not repo_name:
        repo_name = Prompt.ask("Repository name")
        if not repo_name:
            console.print("[bold red]Repository name is required[/bold red]")
            sys.exit(1)
    
    description = args.description
    if not description and not args.auto_init:
        description = Prompt.ask("Repository description", default="")
    
    # Configure repository settings
    private = args.private
    if not args.private:
        private = Confirm.ask("Make repository private?", default=False)
    
    has_issues = not args.no_issues
    has_wiki = args.enable_wiki
    has_projects = args.enable_projects
    auto_init = args.auto_init
    
    # Display settings summary
    console.print(f"\n[bold]Repository Settings:[/bold]")
    console.print(f"Name: {repo_name}")
    console.print(f"Description: {description or 'No description'}")
    console.print(f"Private: {private}")
    console.print(f"Initialize with README: {auto_init}")
    console.print(f"Issues: {has_issues}")
    console.print(f"Wiki: {has_wiki}")
    console.print(f"Projects: {has_projects}")
    
    if not Confirm.ask("\nProceed with repository creation?", default=True):
        console.print("Repository creation cancelled.")
        sys.exit(0)
    
    # Create the repository
    if create_github_repository(
        token, repo_name, description, private, 
        has_issues, has_wiki, has_projects, auto_init
    ):
        console.print("\n[bold green]Repository created successfully![/bold green]")
        
        # Optionally set up git remote for existing projects
        if args.setup_remote or (not auto_init and Confirm.ask("Set up git remote for this project?", default=True)):
            if setup_git_remote(repo_name):
                console.print("\n[bold green]Git remote configured![/bold green]")
                if not auto_init:
                    console.print("\nNext steps:")
                    console.print("1. git add .")
                    console.print("2. git commit -m 'Initial commit'")
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
