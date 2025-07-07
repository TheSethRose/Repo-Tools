#!/usr/bin/env python3
"""
GitHub Repository Management CLI

A comprehensive command-line interface for managing GitHub repositories.
Provides unified access to all repository management tools including listing,
privacy management, backup, and repository creation.

Usage:
    python main.py <command> [options]

Commands:
    list        List all your GitHub repositories with detailed information
    privacy     Manage repository privacy (make zero-star repos private, handle forks)
    backup      Backup all repositories to local directory
    create      Create a new GitHub repository
    help        Show detailed help for a specific command

Examples:
    python main.py list
    python main.py list --compact --limit 10
    python main.py privacy --dry-run
    python main.py backup --backup-path /custom/path --dry-run
    python main.py create --name "MyProject" --description "My awesome project"
    python main.py help backup

Environment Variables:
    GITHUB_TOKEN: GitHub Personal Access Token with 'repo' scope (required)
    BACKUP_PATH: Default backup directory path (optional, for backup command)

For detailed help on any command, use:
    python main.py help <command>
"""

import os
import sys
import argparse
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

try:
    from dotenv import load_dotenv
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Install with: pip install -r requirements.txt")
    sys.exit(1)


class GitHubCLI:
    """Main CLI class for GitHub repository management."""
    
    def __init__(self):
        self.console = Console()
        load_dotenv()
        
    def check_token(self) -> bool:
        """Check if GitHub token is available."""
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            self.console.print("[bold red]✗ GITHUB_TOKEN environment variable not set[/bold red]")
            self.console.print("\nPlease set your GitHub Personal Access Token:")
            self.console.print("1. Go to https://github.com/settings/tokens")
            self.console.print("2. Generate a new token with 'repo' scope")
            self.console.print("3. Set the token: export GITHUB_TOKEN='your_token_here'")
            self.console.print("\nOr add it to your .env file:")
            self.console.print("echo 'GITHUB_TOKEN=your_token_here' >> .env")
            return False
        return True
    
    def show_welcome(self):
        """Display welcome message and available commands."""
        title = Text("GitHub Repository Management CLI", style="bold blue")
        
        commands_table = Table(show_header=True, header_style="bold cyan")
        commands_table.add_column("Command", style="green", width=12)
        commands_table.add_column("Description", style="white")
        commands_table.add_column("Example", style="dim")
        
        commands_table.add_row(
            "list", 
            "List all repositories with details", 
            "main.py list --compact"
        )
        commands_table.add_row(
            "privacy", 
            "Manage repository privacy settings", 
            "main.py privacy --dry-run"
        )
        commands_table.add_row(
            "backup", 
            "Backup repositories to local directory", 
            "main.py backup --dry-run"
        )
        commands_table.add_row(
            "create", 
            "Create a new GitHub repository", 
            "main.py create --name 'MyRepo'"
        )
        commands_table.add_row(
            "help", 
            "Show detailed help for a command", 
            "main.py help backup"
        )
        
        panel_content = f"{title}\\n\\n{commands_table}"
        panel = Panel(
            commands_table,
            title="📚 Available Commands",
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print("\\n[dim]Use 'python main.py <command> --help' for detailed options.[/dim]")
    
    def show_command_help(self, command: str):
        """Show detailed help for a specific command."""
        help_info = {
            "list": {
                "description": "Display a formatted table of your GitHub repositories",
                "usage": "python main.py list [options]",
                "options": [
                    ("--compact", "Use compact table format (auto-enabled for >20 repos)"),
                    ("--limit N", "Limit to N repositories (default: all)"),
                ],
                "examples": [
                    "python main.py list",
                    "python main.py list --compact",
                    "python main.py list --limit 10",
                ]
            },
            "privacy": {
                "description": "Manage repository privacy and clean up zero-star repos/forks",
                "usage": "python main.py privacy [options]",
                "options": [
                    ("--dry-run", "Preview changes without making them (default)"),
                    ("--execute", "Actually perform the privacy changes"),
                ],
                "examples": [
                    "python main.py privacy",
                    "python main.py privacy --dry-run",
                    "python main.py privacy --execute",
                ]
            },
            "backup": {
                "description": "Clone and backup all repositories to local directory",
                "usage": "python main.py backup [options]",
                "options": [
                    ("--backup-path PATH", "Custom backup directory (default: ~/Developer/Github/Backup)"),
                    ("--dry-run", "Preview what would be backed up without cloning"),
                ],
                "examples": [
                    "python main.py backup",
                    "python main.py backup --dry-run",
                    "python main.py backup --backup-path /custom/path",
                ]
            },
            "create": {
                "description": "Create a new GitHub repository with custom settings",
                "usage": "python main.py create [options]",
                "options": [
                    ("--name NAME", "Repository name (interactive prompt if not provided)"),
                    ("--description DESC", "Repository description"),
                    ("--private", "Make repository private"),
                    ("--auto-init", "Initialize with README"),
                    ("--no-issues", "Disable issues"),
                    ("--enable-wiki", "Enable wiki"),
                    ("--enable-projects", "Enable projects"),
                    ("--setup-remote", "Set up git remote after creation"),
                ],
                "examples": [
                    "python main.py create",
                    "python main.py create --name 'MyProject' --description 'My awesome project'",
                    "python main.py create --name 'PrivateRepo' --private",
                    "python main.py create --name 'NewProject' --auto-init --enable-wiki",
                ]
            }
        }
        
        if command not in help_info:
            self.console.print(f"[red]Unknown command: {command}[/red]")
            self.console.print("Available commands: list, privacy, backup, create")
            return
        
        info = help_info[command]
        
        # Create help display
        self.console.print(f"[bold blue]{command.upper()} Command Help[/bold blue]\\n")
        self.console.print(f"[bold]Description:[/bold] {info['description']}\\n")
        self.console.print(f"[bold]Usage:[/bold] {info['usage']}\\n")
        
        if info['options']:
            self.console.print("[bold]Options:[/bold]")
            for option, desc in info['options']:
                self.console.print(f"  [cyan]{option:<20}[/cyan] {desc}")
            self.console.print()
        
        if info['examples']:
            self.console.print("[bold]Examples:[/bold]")
            for example in info['examples']:
                self.console.print(f"  [dim]{example}[/dim]")
    
    def run_list_command(self, args):
        """Execute the list repositories command."""
        try:
            from list_repos import GitHubRepoLister
            
            token = os.getenv('GITHUB_TOKEN')
            lister = GitHubRepoLister(token)
            
            if not lister.validate_token():
                sys.exit(1)
            
            # Parse arguments
            compact = getattr(args, 'compact', False)
            limit = getattr(args, 'limit', None)
            
            lister.display_repositories(limit=limit, compact=compact)
            
        except ImportError as e:
            self.console.print(f"[red]Error importing list_repos module: {e}[/red]")
            sys.exit(1)
    
    def run_privacy_command(self, args):
        """Execute the privacy management command."""
        try:
            from set_repos_private import GitHubPrivacyManager
            
            token = os.getenv('GITHUB_TOKEN')
            manager = GitHubPrivacyManager(token)
            
            if not manager.validate_token():
                sys.exit(1)
            
            # Default to dry-run unless --execute is specified
            dry_run = not getattr(args, 'execute', False)
            
            if dry_run:
                self.console.print("[bold blue]Running in DRY-RUN mode (no changes will be made)[/bold blue]")
                self.console.print("Use --execute to actually perform changes\\n")
            
            manager.run(dry_run=dry_run)
            
        except ImportError as e:
            self.console.print(f"[red]Error importing set_repos_private module: {e}[/red]")
            sys.exit(1)
    
    def run_backup_command(self, args):
        """Execute the backup repositories command."""
        try:
            from backup_repos import GitHubRepoBackup
            
            token = os.getenv('GITHUB_TOKEN')
            backup_path = getattr(args, 'backup_path', None) or os.getenv('BACKUP_PATH')
            dry_run = getattr(args, 'dry_run', False)
            
            backup_manager = GitHubRepoBackup(token, backup_path)
            
            if not backup_manager.validate_token():
                sys.exit(1)
            
            if not backup_manager.setup_backup_directories():
                sys.exit(1)
            
            # Get all repositories
            repos = backup_manager.get_all_repositories()
            if not repos:
                sys.exit(1)
            
            # Display backup summary
            backup_manager.display_backup_summary(repos)
            
            # Confirm action if not dry run
            if not dry_run:
                from rich.prompt import Confirm
                if not Confirm.ask(f"\\n🚀 Proceed with backing up {len(repos)} repositories?"):
                    backup_manager.console.print("Backup cancelled.")
                    sys.exit(0)
            
            # Perform backup
            backup_manager.backup_repositories(repos, dry_run)
            
        except ImportError as e:
            self.console.print(f"[red]Error importing backup_repos module: {e}[/red]")
            sys.exit(1)
    
    def run_create_command(self, args):
        """Execute the create repository command."""
        try:
            from create_github_repo import create_github_repository, setup_git_remote
            from rich.prompt import Confirm, Prompt
            
            token = os.getenv('GITHUB_TOKEN')
            
            # Get repository details
            repo_name = getattr(args, 'name', None)
            if not repo_name:
                repo_name = Prompt.ask("Repository name")
                if not repo_name:
                    self.console.print("[bold red]Repository name is required[/bold red]")
                    sys.exit(1)
            
            description = getattr(args, 'description', "")
            if not description and not getattr(args, 'name', None):
                description = Prompt.ask("Repository description (optional)", default="")
            
            private = getattr(args, 'private', False)
            if not getattr(args, 'private', False) and not getattr(args, 'name', None):
                private = Confirm.ask("Make repository private?", default=False)
            
            has_issues = not getattr(args, 'no_issues', False)
            has_wiki = getattr(args, 'enable_wiki', False)
            has_projects = getattr(args, 'enable_projects', False)
            auto_init = getattr(args, 'auto_init', False)
            setup_remote = getattr(args, 'setup_remote', False)
            
            # Display settings summary
            self.console.print(f"\\n[bold]Repository Settings:[/bold]")
            self.console.print(f"Name: {repo_name}")
            self.console.print(f"Description: {description or 'No description'}")
            self.console.print(f"Private: {private}")
            self.console.print(f"Initialize with README: {auto_init}")
            self.console.print(f"Issues: {has_issues}")
            self.console.print(f"Wiki: {has_wiki}")
            self.console.print(f"Projects: {has_projects}")
            
            if not Confirm.ask("\\nProceed with repository creation?", default=True):
                self.console.print("Repository creation cancelled.")
                sys.exit(0)
            
            # Create the repository
            if create_github_repository(
                token, repo_name, description, private,
                has_issues, has_wiki, has_projects, auto_init
            ):
                self.console.print("\\n[bold green]Repository created successfully![/bold green]")
                
                # Set up git remote if requested or auto-detected
                if setup_remote or (not auto_init and Confirm.ask("Set up git remote for this project?", default=True)):
                    if setup_git_remote(repo_name):
                        self.console.print("\\n[bold green]Git remote configured![/bold green]")
                        if not auto_init:
                            self.console.print("\\nNext steps:")
                            self.console.print("1. git add .")
                            self.console.print("2. git commit -m 'Initial commit'")
                            self.console.print("3. git push -u origin main")
                    else:
                        self.console.print("\\n[bold yellow]Repository created but git remote setup failed[/bold yellow]")
            else:
                self.console.print("\\n[bold red]Failed to create repository[/bold red]")
                sys.exit(1)
                
        except ImportError as e:
            self.console.print(f"[red]Error importing create_github_repo module: {e}[/red]")
            sys.exit(1)
    
    def run(self):
        """Main entry point for the CLI."""
        parser = argparse.ArgumentParser(
            description="GitHub Repository Management CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py list --compact
  python main.py privacy --dry-run
  python main.py backup --backup-path /custom/path
  python main.py create --name "MyProject" --private
  python main.py help backup

For detailed help: python main.py help <command>
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # List command
        list_parser = subparsers.add_parser('list', help='List all repositories')
        list_parser.add_argument('--compact', action='store_true', help='Use compact table format')
        list_parser.add_argument('--limit', type=int, help='Limit number of repositories shown')
        
        # Privacy command  
        privacy_parser = subparsers.add_parser('privacy', help='Manage repository privacy')
        privacy_parser.add_argument('--execute', action='store_true', help='Execute changes (default is dry-run)')
        
        # Backup command
        backup_parser = subparsers.add_parser('backup', help='Backup repositories')
        backup_parser.add_argument('--backup-path', help='Custom backup directory path')
        backup_parser.add_argument('--dry-run', action='store_true', help='Preview without actually backing up')
        
        # Create command
        create_parser = subparsers.add_parser('create', help='Create a new repository')
        create_parser.add_argument('--name', help='Repository name')
        create_parser.add_argument('--description', help='Repository description', default="")
        create_parser.add_argument('--private', action='store_true', help='Make repository private')
        create_parser.add_argument('--auto-init', action='store_true', help='Initialize with README')
        create_parser.add_argument('--no-issues', action='store_true', help='Disable issues')
        create_parser.add_argument('--enable-wiki', action='store_true', help='Enable wiki')
        create_parser.add_argument('--enable-projects', action='store_true', help='Enable projects')
        create_parser.add_argument('--setup-remote', action='store_true', help='Set up git remote after creation')
        
        # Help command
        help_parser = subparsers.add_parser('help', help='Show detailed help for a command')
        help_parser.add_argument('topic', nargs='?', help='Command to get help for')
        
        args = parser.parse_args()
        
        # Handle no command provided
        if not args.command:
            self.show_welcome()
            return
        
        # Handle help command
        if args.command == 'help':
            if args.topic:
                self.show_command_help(args.topic)
            else:
                self.show_welcome()
            return
        
        # Check for GitHub token before running commands
        if not self.check_token():
            sys.exit(1)
        
        # Route to appropriate command handler
        if args.command == 'list':
            self.run_list_command(args)
        elif args.command == 'privacy':
            self.run_privacy_command(args)
        elif args.command == 'backup':
            self.run_backup_command(args)
        elif args.command == 'create':
            self.run_create_command(args)
        else:
            self.console.print(f"[red]Unknown command: {args.command}[/red]")
            self.show_welcome()


if __name__ == "__main__":
    cli = GitHubCLI()
    cli.run()
