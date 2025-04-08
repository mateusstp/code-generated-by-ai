#!/usr/bin/env python3
"""
Gmail Reader - A script to read emails from Gmail without using Google Cloud Console

This script uses IMAP to connect directly to Gmail servers and fetch emails.
"""

import os
import imaplib
import email
from email.header import decode_header
import re
import getpass
import html2text
from dateutil import parser as date_parser
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Gmail IMAP settings
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Default mailbox
DEFAULT_MAILBOX = "INBOX"

# Default search limit
DEFAULT_SEARCH_LIMIT = 10

class GmailReader:
    def __init__(self):
        self.mail = None
        self.email_address = None
        self.password = None
        
    def connect(self, email_address=None, password=None):
        """
        Connect to Gmail using IMAP
        
        Args:
            email_address: Gmail email address
            password: Gmail password or App Password if 2FA is enabled
            
        Returns:
            bool: True if connection successful, False otherwise
        """
        # Use provided credentials or environment variables or prompt user
        self.email_address = email_address or os.getenv('GMAIL_EMAIL')
        self.password = password or os.getenv('GMAIL_PASSWORD')
        
        if not self.email_address:
            self.email_address = input("Enter your Gmail address: ")
        
        if not self.password:
            self.password = getpass.getpass("Enter your Gmail password or App Password: ")
        
        try:
            # Create an IMAP4 class with SSL
            self.mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            
            # Authenticate
            self.mail.login(self.email_address, self.password)
            return True
        except Exception as e:
            print(f"Error connecting to Gmail: {e}")
            if 'Invalid credentials' in str(e):
                print("\nNOTE: If you have 2-Factor Authentication enabled, "
                      "you need to use an App Password instead of your Gmail password.")
                print("Create one at: https://myaccount.google.com/apppasswords")
            return False
    
    def disconnect(self):
        """
        Disconnect from Gmail
        """
        if self.mail:
            try:
                self.mail.close()
                self.mail.logout()
            except:
                pass  # Ignore errors during logout
    
    def list_mailboxes(self):
        """
        List all available mailboxes/folders
        
        Returns:
            list: List of mailbox names
        """
        if not self.mail:
            print("Not connected to Gmail!")
            return []
        
        try:
            status, mailboxes = self.mail.list()
            if status != 'OK':
                return []
            
            # Parse mailbox names
            mailbox_list = []
            for mailbox in mailboxes:
                # Decode the mailbox name
                parts = mailbox.decode().split(' "/" ')
                if len(parts) == 2:
                    mailbox_list.append(parts[1].replace('"', ''))
            
            return mailbox_list
        except Exception as e:
            print(f"Error listing mailboxes: {e}")
            return []
    
    def select_mailbox(self, mailbox="INBOX"):
        """
        Select a mailbox/folder
        
        Args:
            mailbox: Name of the mailbox to select
            
        Returns:
            int: Number of messages in the mailbox or -1 if failed
        """
        if not self.mail:
            print("Not connected to Gmail!")
            return -1
        
        try:
            status, data = self.mail.select(mailbox)
            if status == 'OK':
                return int(data[0])
            else:
                print(f"Error selecting mailbox '{mailbox}': {data[0].decode() if data else 'Unknown error'}")
                return -1
        except Exception as e:
            print(f"Error selecting mailbox: {e}")
            return -1
    
    def search_emails(self, criteria="ALL", limit=10):
        """
        Search for emails based on criteria
        
        Args:
            criteria: Search criteria (e.g., 'ALL', 'UNSEEN', 'FROM "someone@example.com"')
            limit: Maximum number of emails to return
            
        Returns:
            list: List of email IDs
        """
        if not self.mail:
            print("Not connected to Gmail!")
            return []
        
        try:
            status, data = self.mail.search(None, criteria)
            if status != 'OK':
                print(f"Search failed: {data[0].decode() if data else 'Unknown error'}")
                return []
            
            # Get all email IDs
            email_ids = data[0].split()
            
            # Return the most recent emails up to the limit
            # IMAP returns messages in ascending order (oldest first)
            return [email_id.decode() for email_id in reversed(email_ids[:limit])]
        except Exception as e:
            print(f"Error searching emails: {e}")
            return []
    
    def get_email(self, email_id):
        """
        Retrieve an email by ID
        
        Args:
            email_id: Email ID
            
        Returns:
            dict: Email content with subject, from, date, and body
        """
        if not self.mail:
            print("Not connected to Gmail!")
            return {}
        
        try:
            status, data = self.mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                print(f"Failed to fetch email: {data[0].decode() if data else 'Unknown error'}")
                return {}
            
            # Parse the email
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Decode subject
            subject = decode_header(msg["Subject"])
            if subject[0][1] is not None:
                subject = subject[0][0].decode(subject[0][1])
            else:
                subject = subject[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
            
            # Get sender
            from_header = decode_header(msg.get("From", ""))
            if from_header[0][1] is not None:
                sender = from_header[0][0].decode(from_header[0][1])
            else:
                sender = from_header[0][0]
                if isinstance(sender, bytes):
                    sender = sender.decode()
            
            # Get date
            date_str = msg.get("Date", "")
            try:
                date = date_parser.parse(date_str).strftime("%Y-%m-%d %H:%M:%S")
            except:
                date = date_str
            
            # Get body
            body = self._get_email_body(msg)
            
            return {
                "id": email_id,
                "subject": subject,
                "from": sender,
                "date": date,
                "body": body
            }
        except Exception as e:
            print(f"Error getting email: {e}")
            return {}
    
    def _get_email_body(self, msg):
        """
        Extract the body from an email message
        
        Args:
            msg: Email message object
            
        Returns:
            str: Email body
        """
        # Initialize body
        body = ""
        
        # Check if the email is multipart
        if msg.is_multipart():
            # Iterate through parts
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Skip attachments
                if "attachment" in content_disposition:
                    continue
                
                # Get the body if it's text/plain or text/html
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode()
                    break
                elif content_type == "text/html" and "attachment" not in content_disposition and not body:
                    # Convert HTML to text if no plain text version is found
                    html = part.get_payload(decode=True).decode()
                    h = html2text.HTML2Text()
                    h.ignore_links = False
                    body = h.handle(html)
        else:
            # Not multipart, just get the payload
            content_type = msg.get_content_type()
            if content_type == "text/plain":
                body = msg.get_payload(decode=True).decode()
            elif content_type == "text/html":
                # Convert HTML to text
                html = msg.get_payload(decode=True).decode()
                h = html2text.HTML2Text()
                h.ignore_links = False
                body = h.handle(html)
        
        return body
        
    def get_attachments(self, email_id):
        """
        Get attachments from an email
        
        Args:
            email_id: Email ID
            
        Returns:
            list: List of dictionaries with attachment details (filename, content_type, size, index)
        """
        if not self.mail:
            print("Not connected to Gmail!")
            return []
        
        try:
            status, data = self.mail.fetch(email_id, '(RFC822)')
            if status != 'OK':
                print(f"Failed to fetch email: {data[0].decode() if data else 'Unknown error'}")
                return []
            
            # Parse the email
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            attachments = []
            attachment_index = 0
            
            # Check for attachments
            for part in msg.walk():
                content_disposition = str(part.get("Content-Disposition"))
                
                # Check if it's an attachment
                if "attachment" in content_disposition:
                    filename = part.get_filename()
                    
                    # If no filename, create a default one
                    if not filename:
                        filename = f"attachment_{attachment_index}.bin"
                    
                    # Get content type and size
                    content_type = part.get_content_type()
                    payload = part.get_payload(decode=True)
                    size = len(payload) if payload else 0
                    
                    # Format size for display
                    size_str = self._format_size(size)
                    
                    # Add attachment details to list
                    attachments.append({
                        "index": attachment_index,
                        "filename": filename,
                        "content_type": content_type,
                        "size": size,
                        "size_str": size_str,
                        "part": part  # Store the part for later download
                    })
                    
                    attachment_index += 1
            
            return attachments
        except Exception as e:
            print(f"Error getting attachments: {e}")
            return []
    
    def download_attachment(self, email_id, attachment_index, output_dir="."):
        """
        Download a specific attachment from an email
        
        Args:
            email_id: Email ID
            attachment_index: Index of the attachment to download
            output_dir: Directory to save the attachment to
            
        Returns:
            str: Path to the downloaded file or None if failed
        """
        # Get the attachments
        attachments = self.get_attachments(email_id)
        
        # Check if the attachment index is valid
        if not attachments or attachment_index < 0 or attachment_index >= len(attachments):
            print(f"Invalid attachment index: {attachment_index}")
            return None
        
        # Get the attachment
        attachment = attachments[attachment_index]
        
        try:
            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Get the filename and payload
            filename = attachment["filename"]
            part = attachment["part"]
            payload = part.get_payload(decode=True)
            
            # Sanitize the filename to avoid path traversal
            filename = os.path.basename(filename)
            
            # Create the full path
            filepath = os.path.join(output_dir, filename)
            
            # Check if file already exists and create a unique name if needed
            if os.path.exists(filepath):
                base, ext = os.path.splitext(filename)
                filepath = os.path.join(output_dir, f"{base}_{email_id}{ext}")
            
            # Write the file
            with open(filepath, 'wb') as f:
                f.write(payload)
            
            return filepath
        except Exception as e:
            print(f"Error downloading attachment: {e}")
            return None
    
    def _format_size(self, size_bytes):
        """
        Format file size in a human-readable way
        
        Args:
            size_bytes: Size in bytes
            
        Returns:
            str: Formatted size string
        """
        # Define unit suffixes
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
        
        # Handle zero size
        if size_bytes == 0:
            return '0 B'
        
        # Calculate appropriate suffix
        i = 0
        while size_bytes >= 1024 and i < len(suffixes) - 1:
            size_bytes /= 1024.0
            i += 1
        
        # Format with appropriate precision
        if i == 0:  # Bytes don't need decimal places
            return f"{int(size_bytes)} {suffixes[i]}"
        else:
            return f"{size_bytes:.2f} {suffixes[i]}"


def print_email_list(emails, gmail_reader):
    """
    Print a list of emails with details
    """
    if not emails:
        print("No emails found.")
        return
    
    print(f"\nFound {len(emails)} emails:\n" + "-"*50)
    
    for email_id in emails:
        email_data = gmail_reader.get_email(email_id)
        
        print(f"\nMessage ID: {email_id}")
        print(f"Subject: {email_data.get('subject', 'No subject')}")
        print(f"From: {email_data.get('from', 'Unknown sender')}")
        print(f"Date: {email_data.get('date', 'Unknown date')}")
        print("\nPreview:")
        body = email_data.get('body', 'No body')
        print(body[:200] + '...' if len(body) and len(body) > 200 else body)
        print("-"*50)

def main():
    """
    Main function to run the Gmail reader script
    """
    print("Gmail Reader - A script to read emails from Gmail without Google Cloud Console")
    print("-" * 75)
    
    gmail = GmailReader()
    
    print("Connecting to Gmail...")
    if not gmail.connect():
        return
    
    print("Successfully connected to Gmail!")
    
    # Select INBOX by default
    msg_count = gmail.select_mailbox(DEFAULT_MAILBOX)
    if msg_count >= 0:
        print(f"INBOX selected with {msg_count} messages")
    
    # Track the current email ID for attachment operations
    current_email_id = None
    
    while True:
        print("\n" + "-"*50)
        print("Options:")
        print("1. List mailboxes/folders")
        print("2. Select a mailbox/folder")
        print("3. List recent emails")
        print("4. Search emails")
        print("5. Read a specific email")
        print("6. Download attachments from an email")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            mailboxes = gmail.list_mailboxes()
            print("\nAvailable mailboxes:")
            for i, mailbox in enumerate(mailboxes, 1):
                print(f"{i}. {mailbox}")
        
        elif choice == '2':
            mailbox = input("Enter mailbox name (default: INBOX): ").strip() or DEFAULT_MAILBOX
            msg_count = gmail.select_mailbox(mailbox)
            if msg_count >= 0:
                print(f"Mailbox '{mailbox}' selected with {msg_count} messages")
        
        elif choice == '3':
            max_results = input(f"How many recent emails to list? (default: {DEFAULT_SEARCH_LIMIT}): ")
            max_results = int(max_results) if max_results.strip().isdigit() else DEFAULT_SEARCH_LIMIT
            
            print(f"\nFetching {max_results} recent emails...")
            emails = gmail.search_emails(limit=max_results)
            print_email_list(emails, gmail)
        
        elif choice == '4':
            print("\nSearch options:")
            print("1. By sender")
            print("2. By subject")
            print("3. By date (SINCE or BEFORE date)")
            print("4. Only unread emails")
            print("5. Custom IMAP search")
            
            search_choice = input("Enter your search choice (1-5): ")
            
            criteria = ""
            if search_choice == '1':
                sender = input("Enter sender email: ")
                criteria = f'FROM "{sender}"'
            elif search_choice == '2':
                subject = input("Enter subject text: ")
                criteria = f'SUBJECT "{subject}"'
            elif search_choice == '3':
                date_type = input("Search for emails SINCE or BEFORE a date? (S/B): ").upper()
                date_str = input("Enter date (YYYY-MM-DD): ")
                if date_type == 'S':
                    criteria = f'SINCE "{date_str}"'
                else:
                    criteria = f'BEFORE "{date_str}"'
            elif search_choice == '4':
                criteria = "UNSEEN"
            elif search_choice == '5':
                criteria = input("Enter custom IMAP search criteria: ")
            else:
                print("Invalid choice!")
                continue
            
            max_results = input(f"Maximum number of results (default: {DEFAULT_SEARCH_LIMIT}): ")
            max_results = int(max_results) if max_results.strip().isdigit() else DEFAULT_SEARCH_LIMIT
            
            print(f"\nSearching for emails matching '{criteria}'...")
            emails = gmail.search_emails(criteria=criteria, limit=max_results)
            print_email_list(emails, gmail)
        
        elif choice == '5':
            email_id = input("Enter the email ID: ")
            if not email_id:
                print("Email ID cannot be empty!")
                continue
            
            print(f"\nFetching email with ID: {email_id}...")
            email_data = gmail.get_email(email_id)
            
            if email_data:
                # Store the current email ID for attachment operations
                current_email_id = email_id
                
                print("\n" + "-"*50)
                print(f"Subject: {email_data.get('subject', 'No subject')}")
                print(f"From: {email_data.get('from', 'Unknown sender')}")
                print(f"Date: {email_data.get('date', 'Unknown date')}")
                
                # Check for attachments
                attachments = gmail.get_attachments(email_id)
                if attachments:
                    print("\nAttachments:")
                    for att in attachments:
                        print(f"  [{att['index']}] {att['filename']} ({att['size_str']}, {att['content_type']})")
                    print("\nTo download attachments, use option 6 from the main menu.")
                
                print("\nBody:")
                print(email_data.get('body', 'No body'))
                print("-"*50)
            else:
                print("Could not fetch the email. Please check the email ID.")
        
        elif choice == '6':
            # Handle attachment download
            if not current_email_id:
                email_id = input("Enter the email ID: ")
                if not email_id:
                    print("Email ID cannot be empty!")
                    continue
                current_email_id = email_id
            
            # Get attachments for the email
            attachments = gmail.get_attachments(current_email_id)
            
            if not attachments:
                print(f"No attachments found for email ID: {current_email_id}")
                continue
                
            # Display attachments
            print(f"\nAttachments for email ID {current_email_id}:")
            for att in attachments:
                print(f"  [{att['index']}] {att['filename']} ({att['size_str']}, {att['content_type']})")
                
            # Ask which attachment to download
            attachment_index = input("\nEnter the index of the attachment to download (or 'all' for all attachments): ")
            
            # Ask for download directory
            download_dir = input("Enter download directory (default: current directory): ").strip() or "."
            
            if attachment_index.lower() == 'all':
                # Download all attachments
                downloaded_files = []
                for att in attachments:
                    filepath = gmail.download_attachment(current_email_id, att['index'], download_dir)
                    if filepath:
                        downloaded_files.append(filepath)
                
                if downloaded_files:
                    print(f"\nSuccessfully downloaded {len(downloaded_files)} attachments to {download_dir}:")
                    for filepath in downloaded_files:
                        print(f"  - {os.path.basename(filepath)}")
                else:
                    print("Failed to download attachments.")
            else:
                # Download a specific attachment
                try:
                    index = int(attachment_index)
                    filepath = gmail.download_attachment(current_email_id, index, download_dir)
                    if filepath:
                        print(f"\nSuccessfully downloaded {os.path.basename(filepath)} to {download_dir}")
                    else:
                        print("Failed to download attachment.")
                except ValueError:
                    print("Invalid attachment index. Please enter a number or 'all'.")
        
        elif choice == '7':
            print("\nDisconnecting from Gmail...")
            gmail.disconnect()
            print("Exiting Gmail Reader. Goodbye!")
            break
        
        else:
            print("\nInvalid choice! Please select a number between 1 and 7.")

if __name__ == "__main__":
    main()
