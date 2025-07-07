#!/usr/bin/env python3
"""
GitHub Repository Listing Tool

A simple script to list your GitHub repositories in a formatted table.
Displays key repository information including name, description, language,
visibility (public/private), fork status, stars, forks, and last updated date.

Usage:
    python list_repos.py

Environment Variables:
    GITHUB_TOKEN: GitHub Personal Access Token (required)

Example:
    export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
    python list_repos.py
"""

import os
import sys
from datetime import datetime
from typing import List, Optional

try:
    from github import Github, GithubException
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)


class GitHubRepoLister:
    """GitHub repository listing utility."""
    
    def __init__(self, token: str):
        """Initialize with GitHub token."""
        self.github = Github(token)
        self.console = Console()
    
    def validate_token(self) -> bool:
        """Validate the GitHub token and check rate limits."""
        try:
            user = self.github.get_user()
            rate_limit = self.github.get_rate_limit()
            
            # Check if we have sufficient API calls remaining
            if rate_limit.core.remaining < 10:
                self.console.print(
                    f"[yellow]Warning: Only {rate_limit.core.remaining} API calls remaining. "
                    f"Resets at {rate_limit.core.reset}[/yellow]"
                )
            
            self.console.print(f"[green]Authenticated as: {user.login}[/green]")
            return True
            
        except GithubException as e:
            self.console.print(f"[red]Authentication failed: {e.data['message']}[/red]")
            return False
    
    def get_repositories(self, limit: Optional[int] = None) -> List:
        """Fetch user repositories sorted by stars, then by last updated date."""
        try:
            repos = []
            user = self.github.get_user()
            
            # Get all repositories for the authenticated user
            repo_count = 0
            for repo in user.get_repos(sort="updated", direction="desc"):
                if limit and repo_count >= limit:
                    break
                    
                repos.append({
                    'name': repo.name,
                    'description': repo.description or "",
                    'language': repo.language or "None",
                    'private': repo.private,
                    'fork': repo.fork,
                    'stars': repo.stargazers_count,
                    'forks': repo.forks_count,
                    'updated': repo.updated_at,
                    'created': repo.created_at,
                    'url': repo.html_url
                })
                repo_count += 1
            
            # Sort by stars (descending) first, then by updated date (descending)
            repos.sort(key=lambda x: (-x['stars'], -x['updated'].timestamp()))
            
            return repos
            
        except GithubException as e:
            self.console.print(f"[red]Error fetching repositories: {e.data['message']}[/red]")
            return []
    
    def format_date(self, date: datetime) -> str:
        """Format datetime for display."""
        now = datetime.now(date.tzinfo)
        diff = now - date
        
        if diff.days == 0:
            return "Today"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif diff.days < 365:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
    
    def create_table(self, repos: List, compact: bool = False) -> Table:
        """Create a Rich table from repository data."""
        if compact:
            return self._create_compact_table(repos)
        else:
            return self._create_detailed_table(repos)
    
    def _create_compact_table(self, repos: List) -> Table:
        """Create a compact table for many repositories."""
        table = Table(title="GitHub Repositories", show_header=True, header_style="bold blue", 
                     box=None, show_lines=False)
        
        # Add columns with better spacing
        table.add_column("Repository", style="cyan bold", min_width=25, max_width=30)
        table.add_column("Language", style="green", justify="center", min_width=10)
        table.add_column("⭐", justify="right", style="yellow", min_width=4)
        table.add_column("🍴", justify="right", style="blue", min_width=4)
        table.add_column("Type", justify="center", min_width=10)
        table.add_column("Updated", style="magenta", min_width=12)
        
        # Add rows
        for repo in repos:
            # Format repository type (visibility + fork status)
            if repo['private']:
                visibility = "🔒 Private"
            else:
                visibility = "🌐 Public"
            
            if repo['fork']:
                repo_type = f"{visibility}\n� Fork"
            else:
                repo_type = visibility
            
            table.add_row(
                repo['name'],
                repo['language'],
                str(repo['stars']),
                str(repo['forks']),
                repo_type,
                self.format_date(repo['updated'])
            )
        
        return table
    
    def _create_detailed_table(self, repos: List) -> Table:
        """Create a detailed table with descriptions."""
        table = Table(title="GitHub Repositories", show_header=True, header_style="bold blue")
        
        # Add columns with improved widths
        table.add_column("Repository", style="cyan bold", min_width=20, max_width=25)
        table.add_column("Description", style="white", min_width=30, max_width=45)
        table.add_column("Language", style="green", justify="center", min_width=10)
        table.add_column("⭐", justify="right", style="yellow", min_width=4)
        table.add_column("🍴", justify="right", style="blue", min_width=4)
        table.add_column("Type", justify="center", min_width=12)
        table.add_column("Updated", style="magenta", min_width=12)
        
        # Add rows
        for repo in repos:
            # Format repository type (visibility + fork status)
            if repo['private']:
                visibility = "🔒 Private"
            else:
                visibility = "🌐 Public"
            
            if repo['fork']:
                repo_type = f"{visibility}\n🍴 Fork"
            else:
                repo_type = visibility
            
            # Smart description truncation - preserve word boundaries
            description = repo['description']
            if len(description) > 42:  # Reduced to accommodate wider Type column
                words = description.split()
                truncated = ""
                for word in words:
                    if len(truncated + word + " ") <= 39:
                        truncated += word + " "
                    else:
                        break
                description = truncated.strip() + "..."
            
            table.add_row(
                repo['name'],
                description,
                repo['language'],
                str(repo['stars']),
                str(repo['forks']),
                repo_type,
                self.format_date(repo['updated'])
            )
        
        return table
    
    def display_repositories(self, limit: Optional[int] = None, compact: bool = False):
        """Main method to fetch and display repositories."""
        self.console.print("[bold]Fetching GitHub repositories...[/bold]")
        
        repos = self.get_repositories(limit)
        
        if not repos:
            self.console.print("[yellow]No repositories found or unable to fetch repositories.[/yellow]")
            return
        
        # Auto-select compact mode for many repos
        if len(repos) > 20 and not compact:
            self.console.print(f"[dim]Found {len(repos)} repositories. Using compact view...[/dim]\n")
            compact = True
        
        table = self.create_table(repos, compact)
        self.console.print(table)
        
        # Display summary with better formatting
        total_stars = sum(repo['stars'] for repo in repos)
        total_forks = sum(repo['forks'] for repo in repos)
        
        self.console.print(f"\n[bold cyan]Repository Summary[/bold cyan]")
        self.console.print(f"📊 Total repositories: [yellow]{len(repos)}[/yellow]")
        self.console.print(f"⭐ Total stars: [yellow]{total_stars:,}[/yellow]")
        self.console.print(f"🍴 Total forks: [yellow]{total_forks:,}[/yellow]")
        
        private_count = sum(1 for repo in repos if repo['private'])
        public_count = len(repos) - private_count
        fork_count = sum(1 for repo in repos if repo['fork'])
        original_count = len(repos) - fork_count
        
        self.console.print(f"🌐 Public: [green]{public_count}[/green] | 🔒 Private: [red]{private_count}[/red]")
        self.console.print(f"📝 Original: [blue]{original_count}[/blue] | 🍴 Forks: [yellow]{fork_count}[/yellow]")
        
        # Show language breakdown
        languages = {}
        for repo in repos:
            lang = repo['language']
            if lang != "None":
                languages[lang] = languages.get(lang, 0) + 1
        
        if languages:
            top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
            lang_str = " | ".join([f"{lang}: {count}" for lang, count in top_languages])
            self.console.print(f"💻 Top languages: [dim]{lang_str}[/dim]")


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()
    
    # Get GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        console = Console()
        console.print("[red]Error: GITHUB_TOKEN environment variable not set[/red]")
        console.print("Please set your GitHub Personal Access Token:")
        console.print("1. Go to https://github.com/settings/tokens")
        console.print("2. Generate a new token with 'repo' scope")
        console.print("3. Set the token: export GITHUB_TOKEN='your_token_here'")
        sys.exit(1)
    
    # Create lister and validate token
    lister = GitHubRepoLister(token)
    
    if not lister.validate_token():
        sys.exit(1)
    
    # Display repositories
    try:
        # You can add a limit here if desired, e.g., lister.display_repositories(limit=20)
        lister.display_repositories()
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console = Console()
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
