# GitHub Repository Tools

A collection of Python scripts to manage GitHub repositories using PyGithub and Rich for beautiful terminal output.

## Scripts

### 1. Repository Listing (`list_repos.py`)

Display a formatted table of your GitHub repositories with key details including:

- Repository name and description
- Primary language
- Star and fork counts
- Visibility (public/private)
- Fork status
- Last updated date
- Automatic sorting by stars (descending), then by last updated date

### 2. Privacy Manager (`set_repos_private.py`)

Automatically manage repository privacy and clean up forks:

- **Privacy Management**: Set public repositories with zero stars to private
- **Fork Management**: Identify and optionally delete zero-star forks
- **Smart Filtering**: Separates regular repos from forks
- **Safety Features**: Dry-run mode and confirmation prompts
- **Detailed Preview**: Shows what changes will be made before execution

### 3. Repository Backup (`backup_repos.py`)

Clone/download all your repositories to a local backup directory:

- **Complete Backup**: Backs up all public and private repositories
- **Organized Structure**: Separates repos into public/, private/, and forks/ directories
- **Update Existing**: Updates existing repositories instead of re-cloning
- **Progress Tracking**: Shows real-time progress with Rich progress bars
- **Flexible Paths**: Customizable backup directory location
- **Comprehensive Reporting**: Detailed summary of backup results

## Features

- **Rich Terminal Output**: Beautiful tables with color coding and icons
- **Secure Authentication**: Uses GitHub Personal Access Tokens via environment variables
- **Safe Operations**: Dry-run mode and confirmation prompts for destructive actions
- **Smart Sorting**: Repositories sorted by popularity and activity
- **Error Handling**: Graceful handling of API errors and rate limits
- **Progress Tracking**: Real-time progress indication for long-running operations

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd Repo-Tools
```

2. Install dependencies using uv:

```bash
uv pip install -r requirements.txt
```

3. Set up your GitHub token:

```bash
cp .env.example .env
# Edit .env and add your GitHub Personal Access Token
```

## Usage

### 1. List Repositories

```bash
python list_repos.py
```

This displays a table of all your repositories sorted by stars (highest first), then by last updated date. Shows:

- Repository name and description
- Primary language
- Visibility (public/private)
- Fork status
- Stars and forks count
- Last updated date
- Summary statistics

### 2. Manage Repository Privacy

```bash
python set_repos_private.py
```

This script will:

1. Scan all your repositories (public and private)
2. Separate regular repositories from forks
3. Identify public repositories with zero stars
4. Identify forks with zero stars
5. Show a preview of changes in organized tables
6. Ask for confirmation before making changes
7. Make zero-star public repositories private
8. Optionally delete zero-star forks (with confirmation)

**Note**: The script shows detailed previews before making any changes.

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

Dry-run mode (see what would be done without actually cloning):

```bash
python backup_repos.py --dry-run
```

This script will:

1. Create organized backup directory structure (public/, private/, forks/)
2. Clone all repositories to appropriate subdirectories
3. Update existing repositories instead of re-cloning
4. Show real-time progress with a progress bar
5. Provide detailed summary of backup results

**Directory Structure**:

```text
Backup/
├── public/          # Public repositories
├── private/         # Private repositories
└── forks/           # Forked repositories
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

```
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
- The script validates your token before making API calls
- Monitors API rate limits to prevent exceeding quotas

## License

MIT License - see LICENSE file for details.
