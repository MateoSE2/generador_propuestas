#!/usr/bin/env python3
"""
Randomizer Script
Copies a content folder to a new folder with a random UUID suffix.

Usage:
    python randomizer.py <content_folder_path>
    
Example:
    python randomizer.py Markezy/content
    # Creates: Markezy/content-8f74df63-499a-4633-a041-fb502ed49dec
"""

import argparse
import shutil
import uuid
import os
import sys
from pathlib import Path


def copy_content_folder(source_path):
    """
    Copy a content folder to a new folder with UUID suffix.
    
    Args:
        source_path (str): Path to the source content folder
        
    Returns:
        str: Path to the newly created folder
    """
    # Convert to Path object for easier manipulation
    source = Path(source_path)
    
    # Check if source folder exists
    if not source.exists():
        raise FileNotFoundError(f"Source folder does not exist: {source_path}")
    
    if not source.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_path}")
    
    # Generate a random UUID
    random_uuid = str(uuid.uuid4())
    
    # Create the new folder name with UUID suffix
    parent_dir = source.parent
    folder_name = source.name
    new_folder_name = f"{folder_name}-{random_uuid}"
    destination = parent_dir / new_folder_name
    
    # Copy the entire folder
    try:
        shutil.copytree(source, destination)
        print(f"✅ Successfully copied folder:")
        print(f"   From: {source}")
        print(f"   To:   {destination}")
        return str(destination)
    except Exception as e:
        raise RuntimeError(f"Failed to copy folder: {str(e)}")


def main():
    """Main function to handle command line arguments and execute the copy operation."""
    parser = argparse.ArgumentParser(
        description="Copy a content folder to a new folder with random UUID suffix",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python randomizer.py Markezy/content
  python randomizer.py /path/to/content
  python randomizer.py ./content
        """
    )
    
    parser.add_argument(
        'content_path',
        help='Path to the content folder to copy'
    )
    
    args = parser.parse_args()
    
    try:
        # Execute the copy operation
        new_folder_path = copy_content_folder(args.content_path)
        print(f"\n🎯 New folder created: {new_folder_path}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except NotADirectoryError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 