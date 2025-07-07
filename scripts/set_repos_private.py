#!/usr/bin/env python3
"""
GitHub Repository Privacy Manager

A script to automatically set public repositories with zero stars to private.
This helps clean up your GitHub profile by hiding less popular repositories.

The script excludes forked repositories to avoid potential issues with upstream
repository management.

Usage:
    python set_repos_private.py

Environment Variables:
    GITHUB_TOKEN: GitHub Personal Access Token with 'repo' scope (required)

Example:
    export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
    python set_repos_private.py
"""
import os
import sys
from typing import List, Dict, Any

try:
    from github import Github, GithubException
    from rich.console import Console
    from rich.table import Table
    from rich.prompt import Confirm
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)


class GitHubPrivacyManager:
    """GitHub repository privacy management utility."""
    
    def __init__(self, token: str):
        """Initialize with GitHub token."""
        self.github = Github(token)
        self.console = Console()
    
    def validate_token(self) -> bool:
        """Validate the GitHub token and check permissions."""
        try:
            user = self.github.get_user()
            rate_limit = self.github.get_rate_limit()
            
            # Check if we have sufficient API calls remaining
            if rate_limit.core.remaining < 20:
                self.console.print(
                    f"[yellow]Warning: Only {rate_limit.core.remaining} API calls remaining. "
                    f"Resets at {rate_limit.core.reset}[/yellow]"
                )
            
            self.console.print(f"[green]Authenticated as: {user.login}[/green]")
            return True
            
        except GithubException as e:
            self.console.print(f"[red]Authentication failed: {e.data['message']}[/red]")
            return False
    
    def find_zero_star_public_repos(self) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Find public repositories with zero stars, separating regular repos from forks."""
        try:
            repos = []
            forks = []
            user = self.github.get_user()
            
            self.console.print("[bold]Scanning repositories for zero-star public repos...[/bold]")
            
            for repo in user.get_repos():
                # Check if repo is public and has zero stars
                if not repo.private and repo.stargazers_count == 0:
                    repo_data = {
                        'name': repo.name,
                        'description': repo.description or "No description",
                        'language': repo.language or "None",
                        'forks': repo.forks_count,
                        'updated': repo.updated_at,
                        'created': repo.created_at,
                        'url': repo.html_url,
                        'repo_obj': repo  # Keep reference for modification
                    }
                    
                    if repo.fork:
                        # Add upstream repository info for forks
                        try:
                            parent = repo.parent
                            repo_data['parent_name'] = parent.full_name if parent else "Unknown"
                        except:
                            repo_data['parent_name'] = "Unknown"
                        forks.append(repo_data)
                    else:
                        repos.append(repo_data)
            
            # Sort both lists by most recently updated first
            repos.sort(key=lambda x: x['updated'], reverse=True)
            forks.sort(key=lambda x: x['updated'], reverse=True)
            
            return repos, forks
            
        except GithubException as e:
            self.console.print(f"[red]Error fetching repositories: {e.data['message']}[/red]")
            return [], []
    
    def display_candidates(self, repos: List[Dict[str, Any]]) -> None:
        """Display repositories that would be made private."""
        if not repos:
            self.console.print("[green]No public repositories with zero stars found![/green]")
            self.console.print("[dim]Note: Forks are automatically excluded from processing[/dim]")
            return
        
        table = Table(title="Public Repositories with Zero Stars (Excluding Forks)", show_header=True, header_style="bold red")
        
        table.add_column("Repository", style="cyan bold", min_width=20)
        table.add_column("Description", style="white", min_width=30, max_width=50)
        table.add_column("Language", style="green", justify="center", min_width=10)
        table.add_column("Forks", justify="right", style="blue", min_width=5)
        table.add_column("Last Updated", style="magenta", min_width=12)
        
        for repo in repos:
            # Smart description truncation
            description = repo['description']
            if len(description) > 47:
                words = description.split()
                truncated = ""
                for word in words:
                    if len(truncated + word + " ") <= 44:
                        truncated += word + " "
                    else:
                        break
                description = truncated.strip() + "..."
            
            # Format date
            updated = self._format_date(repo['updated'])
            
            table.add_row(
                repo['name'],
                description,
                repo['language'],
                str(repo['forks']),
                updated
            )
        
        self.console.print(table)
        self.console.print(f"\n[bold yellow]Found {len(repos)} public repositories with zero stars[/bold yellow]")
        self.console.print("[dim]Note: Forks are automatically excluded from processing[/dim]")
    
    def _format_date(self, date) -> str:
        """Format datetime for display."""
        from datetime import datetime
        
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
    
    def display_forks(self, forks: List[Dict[str, Any]]) -> None:
        """Display fork repositories that would be deleted."""
        if not forks:
            return
        
        table = Table(title="Forked Repositories with Zero Stars", show_header=True, header_style="bold yellow")
        
        table.add_column("Repository", style="cyan bold", min_width=20)
        table.add_column("Parent Repository", style="white", min_width=25)
        table.add_column("Description", style="white", min_width=30, max_width=40)
        table.add_column("Language", style="green", justify="center", min_width=10)
        table.add_column("Last Updated", style="magenta", min_width=12)
        
        for fork in forks:
            # Smart description truncation
            description = fork['description']
            if len(description) > 37:
                words = description.split()
                truncated = ""
                for word in words:
                    if len(truncated + word + " ") <= 34:
                        truncated += word + " "
                    else:
                        break
                description = truncated.strip() + "..."
            
            # Format date
            updated = self._format_date(fork['updated'])
            
            table.add_row(
                fork['name'],
                fork['parent_name'],
                description,
                fork['language'],
                updated
            )
        
        self.console.print(table)
        self.console.print(f"\n[bold yellow]Found {len(forks)} forked repositories with zero stars[/bold yellow]")
        self.console.print("[dim]Note: Forks will be deleted (not made private) if you proceed[/dim]")
    
    def handle_forks(self, forks: List[Dict[str, Any]]) -> None:
        """Handle zero-star fork repositories by deleting them."""
        if not forks:
            return
        
        # Confirm deletion of forks
        self.console.print(f"\n[bold red]WARNING: This will delete {len(forks)} forked repositories![/bold red]")
        self.console.print("Deleted repositories:")
        self.console.print("  • Cannot be recovered without contacting GitHub Support")
        self.console.print("  • Will lose all issues, pull requests, and other data")
        self.console.print("  • Will lose connection to the upstream repository")
        
        if not Confirm.ask("\nDo you want to delete these forked repositories?", default=False):
            self.console.print("[yellow]Skipping fork deletion[/yellow]")
            return
        
        # Process fork deletions
        success_count = 0
        error_count = 0
        
        self.console.print(f"\n[bold red]Deleting {len(forks)} forked repositories...[/bold red]")
        
        try:
            for i, fork in enumerate(forks, 1):
                self.console.print(f"[dim]({i}/{len(forks)})[/dim] Deleting {fork['name']}...")
                
                try:
                    # Delete the forked repository
                    fork['repo_obj'].delete()
                    self.console.print(f"[green]✓[/green] Deleted {fork['name']}")
                    success_count += 1
                    
                except GithubException as e:
                    error_msg = e.data.get('message', str(e))
                    if 'Resource not accessible by personal access token' in error_msg:
                        self.console.print(f"[red]✗[/red] Failed to delete {fork['name']}: Token lacks required permissions")
                        self.console.print(f"[yellow]  Please ensure your token has 'delete_repo' scope[/yellow]")
                    else:
                        self.console.print(f"[red]✗[/red] Failed to delete {fork['name']}: {error_msg}")
                    error_count += 1
                
                except Exception as e:
                    self.console.print(f"[red]✗[/red] Unexpected error deleting {fork['name']}: {e}")
                    error_count += 1
                    
        except KeyboardInterrupt:
            self.console.print(f"\n[yellow]Operation interrupted by user[/yellow]")
            self.console.print(f"[green]✓ Successfully deleted: {success_count}[/green]")
            if error_count > 0:
                self.console.print(f"[red]✗ Failed: {error_count}[/red]")
            return
        
        # Summary
        self.console.print(f"\n[bold]Fork deletion completed:[/bold]")
        self.console.print(f"[green]✓ Successfully deleted: {success_count}[/green]")
        if error_count > 0:
            self.console.print(f"[red]✗ Failed: {error_count}[/red]")
    
    def make_repositories_private(self, repos: List[Dict[str, Any]], dry_run: bool = True) -> None:
        """Make the specified repositories private."""
        if not repos:
            return
        
        if dry_run:
            self.console.print("\n[bold blue]DRY RUN MODE - No changes will be made[/bold blue]")
            self.console.print("These repositories would be made private:")
            for repo in repos:
                self.console.print(f"  • {repo['name']}")
            return
        
        # Confirm action
        self.console.print(f"\n[bold red]WARNING: This will make {len(repos)} repositories private![/bold red]")
        self.console.print("Private repositories have the following limitations:")
        self.console.print("  • Won't be visible to the public")
        self.console.print("  • Won't appear in search results")
        self.console.print("  • May affect GitHub Pages if enabled")
        
        if not Confirm.ask("\nDo you want to proceed?", default=False):
            self.console.print("[yellow]Operation cancelled[/yellow]")
            return
        
        # Process repositories
        success_count = 0
        error_count = 0
        
        self.console.print(f"\n[bold green]Processing {len(repos)} repositories...[/bold green]")
        
        try:
            for i, repo in enumerate(repos, 1):
                self.console.print(f"[dim]({i}/{len(repos)})[/dim] Processing {repo['name']}...")
                
                try:
                    # Make repository private
                    repo['repo_obj'].edit(private=True)
                    self.console.print(f"[green]✓[/green] Made {repo['name']} private")
                    success_count += 1
                    
                except GithubException as e:
                    error_msg = e.data.get('message', str(e))
                    if 'Resource not accessible by personal access token' in error_msg:
                        self.console.print(f"[red]✗[/red] Failed to make {repo['name']} private: Token lacks required permissions")
                        self.console.print(f"[yellow]  Please ensure your token has 'repo' scope (full control of private repositories)[/yellow]")
                    elif 'Validation Failed' in error_msg:
                        # Check for common reasons why validation might fail
                        repo_obj = repo['repo_obj']
                        reasons = []
                        
                        if repo_obj.has_pages:
                            reasons.append("has GitHub Pages enabled")
                        if hasattr(repo_obj, 'template') and repo_obj.template:
                            reasons.append("is a template repository")
                        
                        if reasons:
                            reason_text = ", ".join(reasons)
                            self.console.print(f"[red]✗[/red] Failed to make {repo['name']} private: Repository {reason_text}")
                        else:
                            self.console.print(f"[red]✗[/red] Failed to make {repo['name']} private: {error_msg}")
                            self.console.print(f"[yellow]  This may be due to branch protection rules, GitHub Pages, or other repository settings[/yellow]")
                    else:
                        self.console.print(f"[red]✗[/red] Failed to make {repo['name']} private: {error_msg}")
                    error_count += 1
                
                except Exception as e:
                    self.console.print(f"[red]✗[/red] Unexpected error with {repo['name']}: {e}")
                    error_count += 1
                    
        except KeyboardInterrupt:
            self.console.print(f"\n[yellow]Operation interrupted by user[/yellow]")
            self.console.print(f"[green]✓ Successfully made private: {success_count}[/green]")
            if error_count > 0:
                self.console.print(f"[red]✗ Failed: {error_count}[/red]")
            return
        
        # Summary
        self.console.print(f"\n[bold]Operation completed:[/bold]")
        self.console.print(f"[green]✓ Successfully made private: {success_count}[/green]")
        if error_count > 0:
            self.console.print(f"[red]✗ Failed: {error_count}[/red]")
    
    def run(self, dry_run: bool = True) -> None:
        """Main method to find and process zero-star public repositories."""
        # Find candidates
        repos, forks = self.find_zero_star_public_repos()
        
        # Display what was found
        self.display_candidates(repos)
        self.display_forks(forks)
        
        if repos:
            # Process repositories
            self.make_repositories_private(repos, dry_run=dry_run)
        
        if forks and not dry_run:
            # Handle forks separately
            self.handle_forks(forks)
        
        self.console.print("\n[bold cyan]Privacy management complete![/bold cyan]")


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
    
    # Create manager and validate token
    manager = GitHubPrivacyManager(token)
    
    if not manager.validate_token():
        sys.exit(1)
    
    # Run the privacy management
    try:
        console = Console()
        
        # First run in dry-run mode to show what would happen
        console.print("[bold]Running in preview mode...[/bold]")
        manager.run(dry_run=True)
        
        # Ask if user wants to proceed with actual changes
        if Confirm.ask("\nDo you want to proceed with making these repositories private?", default=False):
            console.print("\n[bold]Making changes...[/bold]")
            manager.run(dry_run=False)
        else:
            console.print("[yellow]No changes made[/yellow]")
            
    except KeyboardInterrupt:
        console = Console()
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console = Console()
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
