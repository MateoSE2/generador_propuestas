#!/usr/bin/env python3
"""
Randomizer Script
Copies a content folder to a randomized folder with UUID suffix.
If a randomized folder already exists, updates its content instead of creating a new one.

Usage:
    python randomizer.py <content_folder_path>
    
Examples:
    python randomizer.py Markezy/content
    # First run creates: Markezy/content-8f74df63-499a-4633-a041-fb502ed49dec
    # Second run updates: Markezy/content-8f74df63-499a-4633-a041-fb502ed49dec (same folder)
"""

import argparse
import shutil
import uuid
import os
import sys
import glob
import re
from pathlib import Path


def find_existing_randomized_folder(source_path):
    """
    Find if there's already a randomized folder with UUID suffix.
    
    Args:
        source_path (Path): Path to the source content folder
        
    Returns:
        Path or None: Path to existing randomized folder, or None if not found
    """
    parent_dir = source_path.parent
    folder_name = source_path.name
    
    # Look for folders with pattern: {folder_name}-{uuid}
    pattern = str(parent_dir / f"{folder_name}-*")
    existing_folders = glob.glob(pattern)
    
    # Filter to ensure they match UUID pattern (8-4-4-4-12 characters)
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    
    for folder_path in existing_folders:
        folder = Path(folder_path)
        if folder.is_dir():
            # Extract the suffix after the last dash
            parts = folder.name.split('-')
            if len(parts) >= 6:  # folder_name could have dashes, so we need at least 6 parts for UUID
                # Take last 5 parts as potential UUID (UUID has 4 dashes, so 5 parts)
                potential_uuid = '-'.join(parts[-5:])
                if re.match(uuid_pattern, potential_uuid):
                    return folder
    
    return None


def copy_content_to_existing_folder(source_path, destination_path):
    """
    Copy contents from source folder to existing destination folder.
    
    Args:
        source_path (Path): Source folder path
        destination_path (Path): Destination folder path
    """
    try:
        # Remove existing content in destination
        for item in destination_path.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        
        # Copy all contents from source to destination
        for item in source_path.iterdir():
            if item.is_file():
                shutil.copy2(item, destination_path)
            elif item.is_dir():
                shutil.copytree(item, destination_path / item.name)
        
        print(f"✅ Successfully updated existing randomized folder:")
        print(f"   From: {source_path}")
        print(f"   To:   {destination_path}")
        
    except Exception as e:
        raise RuntimeError(f"Failed to copy content to existing folder: {str(e)}")


def copy_content_folder(source_path):
    """
    Copy a content folder to a randomized folder with UUID suffix.
    If a randomized folder already exists, update its content instead of creating a new one.
    
    Args:
        source_path (str): Path to the source content folder
        
    Returns:
        str: Path to the randomized folder (existing or newly created)
    """
    # Convert to Path object for easier manipulation
    source = Path(source_path)
    
    # Check if source folder exists
    if not source.exists():
        raise FileNotFoundError(f"Source folder does not exist: {source_path}")
    
    if not source.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_path}")
    
    # Check if there's already a randomized folder
    existing_folder = find_existing_randomized_folder(source)
    
    if existing_folder:
        # Update existing randomized folder
        copy_content_to_existing_folder(source, existing_folder)
        return str(existing_folder)
    else:
        # Create new randomized folder (original behavior)
        random_uuid = str(uuid.uuid4())
        parent_dir = source.parent
        folder_name = source.name
        new_folder_name = f"{folder_name}-{random_uuid}"
        destination = parent_dir / new_folder_name
        
        try:
            shutil.copytree(source, destination)
            print(f"✅ Successfully created new randomized folder:")
            print(f"   From: {source}")
            print(f"   To:   {destination}")
            return str(destination)
        except Exception as e:
            raise RuntimeError(f"Failed to create new randomized folder: {str(e)}")


def main():
    """Main function to handle command line arguments and execute the copy operation."""
    parser = argparse.ArgumentParser(
        description="Copy a content folder to a randomized folder with UUID suffix. If randomized folder exists, update its content.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python randomizer.py Markezy/content
  python randomizer.py /path/to/content
  python randomizer.py ./content
  
Behavior:
  - First run: Creates new randomized folder (e.g., content-uuid)
  - Subsequent runs: Updates existing randomized folder content
        """
    )
    
    parser.add_argument(
        'content_path',
        help='Path to the content folder to copy'
    )
    
    args = parser.parse_args()
    
    try:
        # Execute the copy operation
        folder_path = copy_content_folder(args.content_path)
        print(f"\n🎯 Randomized folder: {folder_path}")
        
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