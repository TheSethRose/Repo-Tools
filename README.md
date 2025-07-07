# GitHub Repository Tools

A comprehensive collection of Python scripts to manage GitHub repositories using PyGithub and Rich for beautiful terminal output. These tools help automate common repository management tasks including listing, privacy management, backup, and repository creation.

## Scripts

### 1. Repository Listing (`list_repos.py`)

Display a formatted table of your GitHub repositories with comprehensive details:

- Repository name and description
- Primary language
- Star and fork counts
- Visibility (public/private)
- Fork status with visual indicators
- Last updated date
- Automatic sorting by stars (descending), then by last updated date
- Summary statistics with totals

### 2. Privacy Manager (`set_repos_private.py`)

Automatically manage repository privacy and clean up forks:

- **Privacy Management**: Set public repositories with zero stars to private
- **Fork Management**: Identify and optionally delete zero-star forks with user confirmation
- **Smart Filtering**: Separates regular repositories from forks for appropriate handling
- **Safety Features**: Dry-run mode and confirmation prompts for all destructive actions
- **Detailed Preview**: Shows organized tables of what changes will be made before execution
- **Error Handling**: Graceful handling of API errors and rate limits

### 3. Repository Backup (`backup_repos.py`)

Clone and backup all your repositories to a local directory:

- **Complete Backup**: Backs up all public and private repositories
- **Organized Structure**: Separates repos into `public/`, `private/`, and `forks/` directories
- **Smart Updates**: Updates existing repositories instead of re-cloning
- **Progress Tracking**: Real-time progress bars with Rich UI
- **Flexible Paths**: Customizable backup directory location via command line or environment
- **Dry Run Mode**: Preview what would be backed up without actually cloning
- **Comprehensive Reporting**: Detailed summary of backup results and statistics

### 4. Repository Creator (`create_github_repo.py`)

Dynamic GitHub repository creation tool with full customization:

- **Interactive Mode**: Prompts for repository details if not provided via command line
- **Command Line Options**: Full support for all GitHub repository settings
- **Repository Settings**: Configure privacy, issues, wiki, projects, and auto-initialization
- **Git Integration**: Automatically set up git remotes for existing projects
- **Validation**: Checks for existing repositories before creation
- **Rich Output**: Beautiful terminal interface with status updates and confirmations

## Features

- **Rich Terminal Output**: Beautiful tables with color coding and icons
- **Secure Authentication**: Uses GitHub Personal Access Tokens via environment variables
- **Safe Operations**: Dry-run mode and confirmation prompts for destructive actions
- **Smart Sorting**: Repositories sorted by popularity and activity
- **Error Handling**: Graceful handling of API errors and rate limits
- **Progress Tracking**: Real-time progress indication for long-running operations

## Usage

### 1. List Repositories

```bash
python list_repos.py
```

Displays a comprehensive table of all your repositories sorted by stars (highest first), then by last updated date. Shows:

- Repository name and description
- Primary language
- Visibility (public/private) with visual indicators
- Fork status
- Stars and forks count
- Last updated date
- Summary statistics and totals

### 2. Manage Repository Privacy

```bash
python set_repos_private.py
```

This script will:

1. Scan all your repositories (public and private)
2. Separate regular repositories from forks for appropriate handling
3. Identify public repositories with zero stars
4. Identify forks with zero stars
5. Show detailed preview tables of proposed changes
6. Ask for confirmation before making any changes
7. Make zero-star public repositories private
8. Optionally delete zero-star forks (with explicit confirmation)

**Note**: The script provides detailed previews and requires confirmation before making destructive changes.

### 3. Backup Repositories

```bash
python backup_repos.py
```

Basic backup to default location (`~/Developer/Github/Backup`):

```bash
python backup_repos.py
```

Backup to custom location:

```bash
python backup_repos.py --backup-path /path/to/backup
```

Dry-run mode (preview what would be backed up without actually cloning):

```bash
python backup_repos.py --dry-run
```

This script will:

1. Create organized backup directory structure (`public/`, `private/`, `forks/`)
2. Clone all repositories to appropriate subdirectories
3. Update existing repositories instead of re-cloning
4. Show real-time progress with Rich progress bars
5. Provide detailed summary of backup results and statistics

### 4. Create New Repository

```bash
python create_github_repo.py
```

Interactive mode (prompts for all details):

```bash
python create_github_repo.py
```

With command-line arguments:

```bash
python create_github_repo.py --name "MyProject" --description "My awesome project"
python create_github_repo.py --name "PrivateRepo" --private
python create_github_repo.py --name "NewProject" --auto-init --enable-wiki
```

Available options:

- `--name`: Repository name
- `--description`: Repository description
- `--private`: Make repository private
- `--auto-init`: Initialize with README
- `--no-issues`: Disable issues
- `--enable-wiki`: Enable wiki
- `--enable-projects`: Enable projects
- `--setup-remote`: Set up git remote after creation

**Directory Structure for Backups**:

```text
Backup/
├── public/          # Public repositories
├── private/         # Private repositories
└── forks/           # Forked repositories
```

## Installation

1. Clone this repository:

```bash
git clone https://github.com/TheSethRose/Repo-Tools.git
cd Repo-Tools
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your GitHub token:

```bash
cp .env.example .env
# Edit .env and add your GitHub Personal Access Token
```

## Environment Variables

The scripts use the following environment variables:

- `GITHUB_TOKEN`: GitHub Personal Access Token (required)
- `BACKUP_PATH`: Default backup directory path (optional, for backup_repos.py)

Set these in your `.env` file:

```bash
cp .env.example .env
# Edit .env and add your values
```

## Setup GitHub Token

1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select the `repo` scope for full repository access
4. Copy the generated token
5. Set it in your environment:

   ```bash
   export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
   ```

## Requirements

- Python 3.8+
- GitHub Personal Access Token with `repo` scope

## Dependencies

- `PyGithub`: GitHub API client
- `rich`: Terminal formatting and tables
- `python-dotenv`: Environment variable management

## Example Output

```text
                                    GitHub Repositories                                    
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Repository        ┃ Description                           ┃ Language ┃ Visibility ┃ Stars ┃ Forks ┃ Last Updated    ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ awesome-project   │ My awesome Python project            │ Python   │ 🌐 Public  │    42 │     8 │ 2 days ago      │
│ private-work      │ Private repository for work stuff    │ Go       │ 🔒 Private │     0 │     0 │ 1 week ago      │
└───────────────────┴───────────────────────────────────────┴──────────┴────────────┴───────┴───────┴─────────────────┘

Summary:
• Total repositories: 2
• Total stars: 42
• Total forks: 8
• Public: 1, Private: 1
```

## Security

- Never commit your GitHub token to version control
- Use environment variables or secure secret management
- The scripts validate your token before making API calls
- Monitor API rate limits to prevent exceeding quotas

## License

MIT License - see LICENSE file for details.
