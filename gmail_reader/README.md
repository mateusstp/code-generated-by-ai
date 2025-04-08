# Gmail Reader

## Introduction

Gmail Reader is a Python tool that allows you to read, search, and manage your Gmail emails directly from the command line using the IMAP protocol. It provides a simple interface to interact with your Gmail account without requiring any Google Cloud Console setup or complex API configuration.

Key benefits:
- **No Google Cloud setup required** - Direct IMAP connection to Gmail
- **Simple authentication** - Use your Gmail credentials or App Password
- **Feature-rich** - Browse folders, search emails, read messages
- **Privacy-focused** - Your credentials stay local, no third-party services

## Setup

### 1. Python Environment

The project uses a Python virtual environment created with `uv`:

> **What is uv?** `uv` (sometimes called Ultraviolet) is a modern Python package installer and virtual environment manager written in Rust. It's significantly faster than traditional tools like `pip` and provides more reliable dependency resolution. It works as a drop-in replacement for `pip` in most cases.

```bash
# Activate the virtual environment
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
# Make sure you've activated the virtual environment first
uv pip install -r requirements.txt
```

### 3. Gmail Account Configuration

For the script to access your Gmail account, you need to:

1. Enable IMAP in your Gmail settings:
   - Go to Gmail > Settings > See all settings > Forwarding and POP/IMAP
   - Enable IMAP access
   - Save changes

2. If you have 2-Factor Authentication (2FA) enabled (recommended), you need to create an App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select 'Mail' as the app and your device
   - Generate and copy the 16-character password
   - Use this App Password instead of your regular Gmail password when prompted by the script

3. If you don't have 2FA enabled, you need to allow less secure apps:
   - Go to https://myaccount.google.com/lesssecureapps
   - Enable "Allow less secure apps" (Note: Google may phase this option out, so using 2FA with App Passwords is recommended)

## Usage

After setting up the environment and your Gmail account:

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run the script
python gmail_reader.py
```

When running the script, you'll be prompted to enter your Gmail address and password (or App Password if you're using 2FA).

### Storing Credentials (Optional)

To avoid typing your credentials each time, you can store them in a `.env` file in the project directory:

1. Copy the provided `temp_env` template file to create your `.env` file:
   ```bash
   cp temp_env .env
   ```

2. Edit the `.env` file and replace the placeholder values with your actual Gmail credentials:

```
GMAIL_EMAIL=your.email@gmail.com
GMAIL_PASSWORD=your_password_or_app_password
```

**Important Security Note:** The `.env` file contains sensitive information. Make sure it's:
- Not shared publicly or committed to version control
- Only readable by your user account (`chmod 600 .env`)

The script will automatically read these credentials when it starts.

## Getting Started Guide

### Quick Start Example

1. First, make sure your environment is activated:
   ```bash
   source .venv/bin/activate
   ```

2. Run the script:
   ```bash
   python gmail_reader.py
   ```

3. When prompted, enter your Gmail credentials or create a `.env` file beforehand

4. Once connected, you'll see a menu with options. Here's a simple walkthrough:
   - Select option `1` to see all available mailboxes
   - Select option `2` to choose a mailbox (e.g., INBOX)
   - Select option `3` to view your 10 most recent emails
   - Select option `4` to search for specific emails
   - Select option `5` to read a full email (you'll need the email ID shown in listings)
   - Select option `6` to download attachments from an email
   - Select option `7` to exit the program

### Example: Searching for Emails

To search for emails from a specific sender:
1. Choose option `4` (Search emails)
2. Select option `1` (By sender)
3. Enter the sender's email address
4. Specify how many results you want to see

You'll then see a list of matching emails that you can read by selecting option `5` and entering the email ID.

## Features

### 1. Mailbox Management
- **List all mailboxes**: View all available Gmail folders/labels
- **Select a mailbox**: Switch between different folders like Inbox, Sent, Drafts, or custom labels

### 2. Email Viewing
- **List recent emails**: See the most recent emails in the selected mailbox
- **Read full email content**: View the complete content of any email including subject, sender, date, and body
- **View and download attachments**: See attachment information and download them to your local system

### 3. Advanced Search
- **Search by sender**: Find all emails from a specific email address
- **Search by subject**: Find emails containing specific words in the subject
- **Search by date**: Find emails before or after a specific date
- **Search unread emails**: Quickly find all unread messages
- **Custom IMAP search**: Use advanced IMAP search criteria for complex queries

## Troubleshooting

### Login Issues
- **Authentication Failed**: If you see an authentication error:
  - Double-check your email and password
  - If using 2FA, make sure you're using an App Password, not your regular password
  - Confirm that IMAP is enabled in your Gmail settings

### Connection Problems
- **Connection Timeout**: If the connection times out:
  - Check your internet connection
  - Ensure that your network allows IMAP connections to Gmail (port 993)
  - Some networks (especially corporate ones) might block IMAP connections

### Email Reading Issues
- **Missing Email Content**: If email content appears incomplete or malformatted:
  - Some complex HTML emails might not render perfectly in text format

### Attachment Issues
- **Cannot Download Attachments**: If you encounter issues downloading attachments:
  - Make sure you have write permissions to the download directory
  - Very large attachments may take longer to download
  - Ensure the email actually has attachments before trying to download

## Dependencies

- python-dotenv==1.0.0 - For loading environment variables from .env file
- python-dateutil==2.9.0 - For parsing email dates in various formats
- html2text==2020.1.16 - For converting HTML emails to readable text format
