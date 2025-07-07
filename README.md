# GitHub Repository Tools

A comprehensive collection of Python scripts to manage GitHub repositories with a unified CLI interface. Built with PyGithub and Rich for beautiful terminal output, these tools help automate common repository management tasks including listing, privacy management, backup, and repository creation.

## ✨ Features

- **🎯 Unified CLI** - Single entry point for all repository operations
- **📊 Repository Listing** - Beautiful tables with comprehensive repository details
- **🔒 Privacy Management** - Automated privacy settings and fork cleanup
- **💾 Complete Backup** - Clone and organize all repositories locally
- **🚀 Repository Creation** - Dynamic repository creation with full customization
- **🛡️ Safe Operations** - Dry-run modes and confirmation prompts
- **🎨 Rich UI** - Beautiful terminal interface with colors and progress bars
- **⚡ Fast & Efficient** - Optimized for performance with progress tracking

## ⚡ Quick Start

Get started in 3 simple steps:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your GitHub token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# 3. Use the unified CLI
python main.py list                    # List all repositories
python main.py privacy                 # Preview privacy changes (dry-run)
python main.py backup --dry-run        # Preview backup operation
python main.py create --name "MyRepo"  # Create a new repository
python main.py help backup             # Get detailed help for any command
```

## 🎯 Main CLI Interface

The `main.py` script provides a unified command-line interface for all repository management operations with beautiful Rich formatting and comprehensive help.

### Available Commands

| Command   | Description                              | Example Usage                              |
|-----------|------------------------------------------|--------------------------------------------|
| `list`    | List all repositories with details      | `python main.py list --compact`           |
| `privacy` | Manage repository privacy settings      | `python main.py privacy --execute`        |
| `backup`  | Backup repositories to local directory  | `python main.py backup --dry-run`         |
| `create`  | Create a new GitHub repository          | `python main.py create --name "MyRepo"`   |
| `help`    | Show detailed help for any command      | `python main.py help privacy`             |

### Command Examples

#### Repository Listing

```bash
# List all repositories with full details
python main.py list

# Compact view for large repository collections (auto-enabled for >20 repos)
python main.py list --compact

# Limit to first 10 repositories
python main.py list --limit 10
```

#### Privacy Management

```bash
# Preview privacy changes (safe, no actual changes made)
python main.py privacy

# Execute privacy changes (make zero-star public repos private)
python main.py privacy --execute
```

#### Repository Backup

```bash
# Preview backup operation without cloning
python main.py backup --dry-run

# Backup to default location (~/Developer/Github/Backup)
python main.py backup

# Backup to custom location
python main.py backup --backup-path /custom/backup/path
```

#### Repository Creation

```bash
# Interactive mode (prompts for all details)
python main.py create

# Create with specific parameters
python main.py create --name "MyProject" --description "My awesome project"

# Create private repository with wiki enabled
python main.py create --name "PrivateRepo" --private --enable-wiki

# Create and initialize with README
python main.py create --name "NewProject" --auto-init --setup-remote
```

#### Getting Help

```bash
# Show all available commands
python main.py

# Get detailed help for specific commands
python main.py help backup
python main.py help create
python main.py help privacy
```

## 📁 Individual Scripts (Advanced Usage)

For advanced users, automation, or integration purposes, individual scripts are available in the `/scripts` directory. Each script can be run independently with its own command-line interface.

### scripts/list_repos.py

**Comprehensive Repository Listing with Rich Formatting**

Display a beautiful table of your GitHub repositories with detailed information:

- Repository name, description, and primary language
- Star and fork counts with visual indicators
- Visibility status (public/private) with clear icons
- Fork status identification
- Last updated timestamps
- Automatic sorting by popularity (stars) and activity
- Summary statistics and totals
- Automatic compact mode for large repository collections (>20 repos)

```bash
# Basic usage
python scripts/list_repos.py

# The script automatically uses compact view for >20 repositories
# Shows comprehensive details for smaller collections
```

**Key Features:**

- Smart table formatting based on repository count
- Color-coded visibility and fork indicators
- Comprehensive summary statistics
- Real-time data from GitHub API

### scripts/set_repos_private.py

**Intelligent Privacy Management and Fork Cleanup**

Automatically manage repository privacy settings and clean up unnecessary forks:

**Privacy Management:**

- Identifies public repositories with zero stars
- Converts them to private with user confirmation
- Preserves popular repositories (with stars) as public
- Handles API rate limiting gracefully

**Fork Management:**

- Separates regular repositories from forks
- Identifies zero-star forks for potential cleanup
- Provides detailed preview of proposed changes
- Requires explicit confirmation for destructive actions

**Safety Features:**

- Dry-run mode by default (shows what would be changed)
- Detailed preview tables before any modifications
- User confirmation prompts for all destructive operations
- Comprehensive error handling and recovery

```bash
# Preview changes (safe, default mode)
python scripts/set_repos_private.py

# The script runs in dry-run mode by default - no changes are made
# Shows detailed tables of what would be modified
```

**Smart Filtering:**

- Automatically excludes forks from privacy changes
- Handles repositories and forks separately
- Respects repository relationships and dependencies

### scripts/backup_repos.py

**Complete Repository Backup Solution**

Clone and backup all your repositories to a local directory with intelligent organization:

**Backup Features:**

- **Complete Coverage**: Backs up all public, private, and forked repositories
- **Smart Organization**: Automatically organizes repos into `public/`, `private/`, and `forks/` directories
- **Intelligent Updates**: Updates existing repositories instead of re-cloning
- **Progress Tracking**: Real-time progress bars with Rich UI showing current operations
- **Flexible Configuration**: Customizable backup directory via command line or environment variables
- **Dry Run Support**: Preview what would be backed up without actually cloning
- **Comprehensive Reporting**: Detailed summary of backup results and statistics

**Directory Structure:**

```text
Backup/
├── public/          # Public repositories
├── private/         # Private repositories
└── forks/           # Forked repositories
```

```bash
# Basic backup to default location
python scripts/backup_repos.py

# Backup to custom location
python scripts/backup_repos.py --backup-path /path/to/backup

# Preview mode (shows what would be backed up)
python scripts/backup_repos.py --dry-run
```

**Advanced Features:**

- Automatic detection of existing repositories
- Git pull for updates instead of full re-clone
- Comprehensive error handling and retry logic
- Network interruption recovery
- Detailed logging and progress reporting

### scripts/create_github_repo.py

**Dynamic Repository Creation Tool**

Create new GitHub repositories with full customization and automation support:

**Creation Features:**

- **Interactive Mode**: Prompts for repository details when not provided via command line
- **Command Line Support**: Full parameter support for automation and scripting
- **Complete Settings**: Configure privacy, issues, wiki, projects, and auto-initialization
- **Git Integration**: Automatically set up git remotes for existing local projects
- **Validation**: Checks for existing repositories and handles conflicts gracefully
- **Rich Output**: Beautiful terminal interface with status updates and confirmations

**Available Options:**

- `--name`: Repository name (required)
- `--description`: Repository description
- `--private`: Make repository private
- `--auto-init`: Initialize with README file
- `--no-issues`: Disable GitHub Issues
- `--enable-wiki`: Enable repository wiki
- `--enable-projects`: Enable GitHub Projects
- `--setup-remote`: Automatically configure git remote after creation

```bash
# Interactive mode (prompts for all details)
python scripts/create_github_repo.py

# Create with specific parameters
python scripts/create_github_repo.py --name "MyProject" --description "My awesome project"

# Create private repository with additional features
python scripts/create_github_repo.py --name "PrivateRepo" --private --enable-wiki

# Create and set up git remote for existing project
python scripts/create_github_repo.py --name "ExistingProject" --setup-remote
```

**Smart Features:**

- Detects existing repositories and provides helpful information
- Automatically configures git remotes based on your GitHub username
- Validates repository names and settings before creation
- Provides complete repository URLs (HTTPS, SSH, Git) after creation
- Handles GitHub API errors gracefully with clear error messages

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

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Git (for repository operations)
- GitHub Personal Access Token with `repo` scope

### Installation Steps

1. **Clone the repository:**

```bash
git clone https://github.com/TheSethRose/Repo-Tools.git
cd Repo-Tools
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up your GitHub token:**

```bash
cp .env.example .env
# Edit .env and add your GitHub Personal Access Token
```

Or set the environment variable directly:

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

### Verify Installation

Test your setup by running:

```bash
# Check if everything is working
python main.py list --limit 5

# If successful, you should see your repositories listed
```

## 🔐 Environment Variables

The tools use the following environment variables for configuration:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GITHUB_TOKEN` | GitHub Personal Access Token with `repo` scope | ✅ Yes | None |
| `BACKUP_PATH` | Default backup directory path (for backup operations) | ❌ No | `~/Developer/Github/Backup` |

### Setting up Environment Variables

**Option 1: Using .env file (Recommended)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env file and add your token
echo 'GITHUB_TOKEN=ghp_your_token_here' >> .env
echo 'BACKUP_PATH=/custom/backup/path' >> .env
```

**Option 2: Export directly**

```bash
export GITHUB_TOKEN="ghp_your_token_here"
export BACKUP_PATH="/custom/backup/path"
```

**Option 3: Add to shell profile**

```bash
# Add to ~/.zshrc, ~/.bashrc, or ~/.bash_profile
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.zshrc
```

- `GITHUB_TOKEN`: GitHub Personal Access Token (required)
- `BACKUP_PATH`: Default backup directory path (optional, for backup_repos.py)

Set these in your `.env` file:

```bash
cp .env.example .env
# Edit .env and add your values
```

## 🔐 GitHub Token Setup

### Creating Your GitHub Token

1. **Navigate to GitHub Settings**
   - Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
   - Click "Generate new token (classic)"

2. **Configure Token Permissions**
   - **Name**: Give your token a descriptive name (e.g., "Repo-Tools CLI")
   - **Expiration**: Choose an appropriate expiration (90 days recommended)
   - **Scopes**: Select the `repo` scope for full repository access

3. **Save Your Token**
   - Copy the generated token immediately (you won't see it again)
   - Store it securely in your password manager

4. **Set the Environment Variable**

```bash
# Option 1: Export directly (temporary)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Option 2: Add to shell profile (permanent)
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.zshrc

# Option 3: Use .env file (recommended for development)
echo 'GITHUB_TOKEN=ghp_your_token_here' >> .env
```

### Token Security Best Practices

- **Never commit tokens to version control**
- **Use environment variables or secure secret management**
- **Regularly rotate your tokens (every 90 days)**
- **Use the minimum required scopes**
- **Monitor token usage in GitHub settings**

## 💻 System Requirements

| Requirement | Minimum Version | Recommended |
|-------------|----------------|-------------|
| **Python** | 3.8+ | 3.10+ |
| **Git** | 2.20+ | Latest |
| **Operating System** | macOS 10.15+, Ubuntu 18.04+, Windows 10+ | Latest |
| **Internet Connection** | Required for GitHub API | Stable broadband |

## 📦 Dependencies

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **PyGithub** | ^1.59.0 | GitHub API client library |
| **rich** | ^13.0.0 | Beautiful terminal formatting and progress bars |
| **python-dotenv** | ^1.0.0 | Environment variable management |

### Installation

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install PyGithub rich python-dotenv
```

## 📸 Example Output

### Repository List View

```text
                               GitHub Repositories                              
 
 Repository                      Language     ⭐    🍴     Type     Updated      
 MCP-Server-Starter             TypeScript    26     6  🌐 Public   3 days ago   
 DevRules                         Shell       22     4  🌐 Public   2 weeks ago  
 AI-File-Organizer-Agent          Python      16     2  🌐 Public   3 days ago   
 Agent-Chat                       Python      16     0  🌐 Public   3 months ago 
 Fetch-Browser                  TypeScript    10     2  🌐 Public   1 week ago   

Repository Summary
📊 Total repositories: 116
⭐ Total stars: 151
🍴 Total forks: 23
🌐 Public: 25 | 🔒 Private: 91
```

### Privacy Management Preview

```text
                   Public Repositories with Zero Stars (Excluding Forks)                    
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━┓
┃ Repository           ┃ Description                           ┃  Language  ┃ Forks ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━┩
│ Repo-Tools           │ Python scripts for managing GitHub...│   Python   │     0 │
│ Make-Columns         │ No description                        │ PowerShell │     0 │
└──────────────────────┴───────────────────────────────────────┴────────────┴───────┘

DRY RUN MODE - No changes will be made
These repositories would be made private:
  • Repo-Tools
  • Make-Columns
```

### Backup Progress

```text
📊 Backup Summary                    
┏━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Category      ┃ Count ┃ Details                      ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Public Repos  │    25 │ Regular public repositories  │
│ Private Repos │    91 │ Regular private repositories │
│ Forks         │     0 │ Forked repositories          │
│ Total         │   116 │ All repositories             │
└───────────────┴───────┴──────────────────────────────┘
```

## 🔒 Security & Best Practices

### Token Security

- **Never commit your GitHub token to version control**
- **Use environment variables or secure secret management systems**
- **Regularly rotate your tokens (every 90 days recommended)**
- **Monitor token usage in GitHub Settings**
- **Use the minimum required scopes (only `repo` for this tool)**

### API Rate Limiting

- **GitHub API Rate Limits**: 5,000 requests per hour for authenticated users
- **The tools automatically handle rate limiting** with exponential backoff
- **Monitor your rate limit usage** in the tool output
- **Consider using GitHub Enterprise** for higher rate limits if needed

### Safe Operations

- **All destructive operations have confirmation prompts**
- **Dry-run modes are available for testing**
- **Comprehensive error handling and recovery**
- **Detailed logging for troubleshooting**

## 🐛 Troubleshooting

### Common Issues

#### Authentication Problems

**Issue**: "GITHUB_TOKEN environment variable not set"

**Solution**:
```bash
# Check if token is set
echo $GITHUB_TOKEN

# Set the token
export GITHUB_TOKEN="your_token_here"

# Make it permanent
echo 'export GITHUB_TOKEN="your_token_here"' >> ~/.zshrc
```

#### Rate Limiting

**Issue**: "API rate limit exceeded"

**Solution**:
- Wait for rate limit reset (shown in error message)
- The tool automatically retries with exponential backoff
- Consider running operations in smaller batches

#### Network Issues

**Issue**: Connection timeouts or network errors

**Solution**:
```bash
# Test GitHub connectivity
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Check your internet connection
ping github.com

# Try running with verbose output
python main.py list --help
```

#### Repository Access Issues

**Issue**: "Repository not found" or permission errors

**Solution**:
- Verify your token has `repo` scope
- Check if repository exists and you have access
- Ensure token hasn't expired

### Getting Help

1. **Check the built-in help**: `python main.py help <command>`
2. **Run with verbose output** to see detailed error messages
3. **Check GitHub Status**: [status.github.com](https://status.github.com)
4. **Review GitHub API documentation**: [docs.github.com/en/rest](https://docs.github.com/en/rest)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/Repo-Tools.git
cd Repo-Tools

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Set up pre-commit hooks
pre-commit install  # If using pre-commit
```

### Making Changes

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes** following the existing code style
3. **Test thoroughly** with your own repositories (use dry-run modes)
4. **Update documentation** if needed
5. **Commit with descriptive messages**
6. **Open a pull request** with detailed description

### Code Guidelines

- **Follow PEP 8** for Python code formatting
- **Use type hints** for all function parameters and return values
- **Add comprehensive docstrings** for all public functions
- **Include error handling** for all API calls
- **Test with various repository configurations**
- **Maintain backward compatibility** when possible

### Reporting Issues

When reporting bugs, please include:

- **Operating System** and Python version
- **Exact command** that caused the issue
- **Complete error message** (with sensitive info redacted)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**

## 📄 License

MIT License

Copyright (c) 2025 Seth Rose

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🌟 Acknowledgments

- **PyGithub** - Excellent Python library for GitHub API
- **Rich** - Amazing library for beautiful terminal interfaces
- **GitHub** - For providing a comprehensive API
- **Contributors** - Thank you to everyone who has contributed to this project

## 📞 Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/TheSethRose/Repo-Tools/issues)
- **Discussions**: [Community discussions and Q&A](https://github.com/TheSethRose/Repo-Tools/discussions)
- **Documentation**: This README and built-in help commands

---

**Happy Repository Management! 🚀**
