#!/usr/bin/env python3
"""
GitHub Repository Backup Tool

A script to clone/download all your GitHub repositories (public and private) 
to a local backup directory. The script organizes repositories by type 
(public/private) and handles both regular repositories and forks.

Usage:
    python backup_repos.py [--backup-path /path/to/backup] [--dry-run]

Arguments:
    --backup-path: Custom backup directory path (optional)
    --dry-run: Show what would be done without actually cloning

Environment Variables:
    GITHUB_TOKEN: GitHub Personal Access Token with 'repo' scope (required)
    BACKUP_PATH: Default backup directory path (optional)

Default backup path: ~/Developer/Github/Backup

Example:
    export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
    python backup_repos.py
    
    # Or with custom path
    python backup_repos.py --backup-path /Users/username/MyBackup
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from github import Github, GithubException
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.prompt import Confirm
    from rich.text import Text
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)


class GitHubRepoBackup:
    """GitHub repository backup utility."""
    
    def __init__(self, token: str, backup_path: Optional[str] = None):
        """Initialize with GitHub token and backup path."""
        self.github = Github(token)
        self.console = Console()
        self.backup_path = Path(backup_path) if backup_path else Path.home() / "Developer" / "Github" / "Backup"
        
    def validate_token(self) -> bool:
        """Validate the GitHub token and check permissions."""
        try:
            user = self.github.get_user()
            rate_limit = self.github.get_rate_limit()
            
            self.console.print(f"✓ Authenticated as: [bold green]{user.login}[/bold green]")
            self.console.print(f"✓ Rate limit: {rate_limit.core.remaining}/{rate_limit.core.limit}")
            
            return True
        except GithubException as e:
            self.console.print(f"[bold red]✗ GitHub API Error:[/bold red] {e.data.get('message', str(e))}")
            return False
        except Exception as e:
            self.console.print(f"[bold red]✗ Error validating token:[/bold red] {str(e)}")
            return False
    
    def setup_backup_directories(self) -> bool:
        """Create backup directory structure."""
        try:
            # Create main backup directory
            self.backup_path.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories for organization
            (self.backup_path / "public").mkdir(exist_ok=True)
            (self.backup_path / "private").mkdir(exist_ok=True)
            (self.backup_path / "forks").mkdir(exist_ok=True)
            
            self.console.print(f"✓ Backup directory ready: [bold blue]{self.backup_path}[/bold blue]")
            return True
        except Exception as e:
            self.console.print(f"[bold red]✗ Error creating backup directories:[/bold red] {str(e)}")
            return False
    
    def get_all_repositories(self) -> List[Dict[str, Any]]:
        """Get all repositories with metadata."""
        try:
            repos = []
            user = self.github.get_user()
            
            self.console.print("📦 Fetching repository list...")
            
            for repo in user.get_repos(type='all'):
                repos.append({
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description or '',
                    'private': repo.private,
                    'fork': repo.fork,
                    'clone_url': repo.clone_url,
                    'ssh_url': repo.ssh_url,
                    'html_url': repo.html_url,
                    'stars': repo.stargazers_count,
                    'forks': repo.forks_count,
                    'language': repo.language,
                    'updated_at': repo.updated_at,
                    'size': repo.size,
                    'archived': repo.archived,
                    'default_branch': repo.default_branch
                })
            
            return repos
        except GithubException as e:
            self.console.print(f"[bold red]✗ GitHub API Error:[/bold red] {e.data.get('message', str(e))}")
            return []
        except Exception as e:
            self.console.print(f"[bold red]✗ Error fetching repositories:[/bold red] {str(e)}")
            return []
    
    def display_backup_summary(self, repos: List[Dict[str, Any]]) -> None:
        """Display backup summary table."""
        if not repos:
            self.console.print("[yellow]No repositories found to backup.[/yellow]")
            return
        
        # Categorize repositories
        public_repos = [r for r in repos if not r['private'] and not r['fork']]
        private_repos = [r for r in repos if r['private'] and not r['fork']]
        forks = [r for r in repos if r['fork']]
        
        # Create summary table
        table = Table(title="📊 Backup Summary")
        table.add_column("Category", style="cyan")
        table.add_column("Count", justify="right", style="magenta")
        table.add_column("Details", style="white")
        
        table.add_row("Public Repos", str(len(public_repos)), "Regular public repositories")
        table.add_row("Private Repos", str(len(private_repos)), "Regular private repositories")
        table.add_row("Forks", str(len(forks)), "Forked repositories")
        table.add_row("Total", str(len(repos)), "All repositories")
        
        self.console.print(table)
        self.console.print(f"\n📁 Backup location: [bold blue]{self.backup_path}[/bold blue]")
    
    def get_backup_subdirectory(self, repo: Dict[str, Any]) -> Path:
        """Determine the appropriate backup subdirectory for a repository."""
        if repo['fork']:
            return self.backup_path / "forks"
        elif repo['private']:
            return self.backup_path / "private"
        else:
            return self.backup_path / "public"
    
    def clone_repository(self, repo: Dict[str, Any], dry_run: bool = False) -> bool:
        """Clone a single repository."""
        repo_name = repo['name']
        backup_dir = self.get_backup_subdirectory(repo)
        repo_path = backup_dir / repo_name
        
        # Skip if already exists and is a git repository
        if repo_path.exists() and (repo_path / ".git").exists():
            self.console.print(f"⏭️  [yellow]Skipping {repo_name} (already exists)[/yellow]")
            return True
        
        if dry_run:
            self.console.print(f"📋 [cyan]Would clone:[/cyan] {repo['full_name']} → {repo_path}")
            return True
        
        try:
            # Use HTTPS clone URL with token for authentication
            clone_url = repo['clone_url']
            if clone_url.startswith('https://github.com/'):
                # Insert token into URL for authentication
                token = os.getenv('GITHUB_TOKEN')
                clone_url = clone_url.replace('https://github.com/', f'https://{token}@github.com/')
            
            # Clone the repository
            cmd = ['git', 'clone', clone_url, str(repo_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.console.print(f"✅ [green]Cloned:[/green] {repo_name}")
                return True
            else:
                self.console.print(f"❌ [red]Failed to clone {repo_name}:[/red] {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            self.console.print(f"❌ [red]Timeout cloning {repo_name}[/red]")
            return False
        except Exception as e:
            self.console.print(f"❌ [red]Error cloning {repo_name}:[/red] {str(e)}")
            return False
    
    def update_repository(self, repo: Dict[str, Any], dry_run: bool = False) -> bool:
        """Update an existing repository."""
        repo_name = repo['name']
        backup_dir = self.get_backup_subdirectory(repo)
        repo_path = backup_dir / repo_name
        
        if not repo_path.exists() or not (repo_path / ".git").exists():
            return False
        
        if dry_run:
            self.console.print(f"📋 [cyan]Would update:[/cyan] {repo_name}")
            return True
        
        try:
            # Pull latest changes
            cmd = ['git', '-C', str(repo_path), 'pull', '--ff-only']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.console.print(f"🔄 [blue]Updated:[/blue] {repo_name}")
                return True
            else:
                self.console.print(f"⚠️  [yellow]Could not update {repo_name}:[/yellow] {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            self.console.print(f"❌ [red]Timeout updating {repo_name}[/red]")
            return False
        except Exception as e:
            self.console.print(f"❌ [red]Error updating {repo_name}:[/red] {str(e)}")
            return False
    
    def backup_repositories(self, repos: List[Dict[str, Any]], dry_run: bool = False) -> None:
        """Backup all repositories with progress tracking."""
        if not repos:
            self.console.print("[yellow]No repositories to backup.[/yellow]")
            return
        
        successful = 0
        failed = 0
        updated = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            
            backup_task = progress.add_task("Backing up repositories...", total=len(repos))
            
            for repo in repos:
                repo_name = repo['name']
                backup_dir = self.get_backup_subdirectory(repo)
                repo_path = backup_dir / repo_name
                
                progress.update(backup_task, description=f"Processing {repo_name}...")
                
                # Check if repository already exists
                if repo_path.exists() and (repo_path / ".git").exists():
                    if self.update_repository(repo, dry_run):
                        updated += 1
                    else:
                        failed += 1
                else:
                    if self.clone_repository(repo, dry_run):
                        successful += 1
                    else:
                        failed += 1
                
                progress.update(backup_task, advance=1)
        
        # Display final summary
        self.console.print("\n📊 Backup Complete!")
        summary_table = Table(title="Backup Results")
        summary_table.add_column("Status", style="cyan")
        summary_table.add_column("Count", justify="right", style="magenta")
        
        summary_table.add_row("✅ Newly cloned", str(successful))
        summary_table.add_row("🔄 Updated", str(updated))
        summary_table.add_row("❌ Failed", str(failed))
        summary_table.add_row("📦 Total processed", str(len(repos)))
        
        self.console.print(summary_table)
        
        if failed > 0:
            self.console.print(f"\n⚠️  [yellow]{failed} repositories failed to backup. Check the logs above for details.[/yellow]")


def main():
    """Main function."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Backup GitHub repositories')
    parser.add_argument('--backup-path', type=str, help='Custom backup directory path')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without actually cloning')
    args = parser.parse_args()
    
    # Get GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Please set your GitHub Personal Access Token in .env file or environment")
        sys.exit(1)
    
    # Get backup path
    backup_path = args.backup_path or os.getenv('BACKUP_PATH')
    
    # Initialize backup manager
    backup_manager = GitHubRepoBackup(token, backup_path)
    
    # Validate token
    if not backup_manager.validate_token():
        sys.exit(1)
    
    # Setup backup directories
    if not backup_manager.setup_backup_directories():
        sys.exit(1)
    
    # Get all repositories
    repos = backup_manager.get_all_repositories()
    if not repos:
        sys.exit(1)
    
    # Display backup summary
    backup_manager.display_backup_summary(repos)
    
    # Confirm action if not dry run
    if not args.dry_run:
        if not Confirm.ask(f"\n🚀 Proceed with backing up {len(repos)} repositories?"):
            backup_manager.console.print("Backup cancelled.")
            sys.exit(0)
    
    # Perform backup
    backup_manager.backup_repositories(repos, args.dry_run)


if __name__ == "__main__":
    main()
