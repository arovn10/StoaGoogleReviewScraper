#!/usr/bin/env python3
"""
Output Management Utility
Helps manage and clean up old JSON output files from the scraper.
"""

import os
import glob
import json
from datetime import datetime, timedelta
import argparse

def list_outputs():
    """List all output files with details."""
    outputs_dir = "data/outputs"
    if not os.path.exists(outputs_dir):
        print("❌ Outputs directory not found: data/outputs")
        return
    
    files = glob.glob(os.path.join(outputs_dir, "*.json"))
    
    if not files:
        print("📁 No output files found in data/outputs/")
        return
    
    print(f"📁 Found {len(files)} output files:")
    print("=" * 80)
    
    for filepath in sorted(files, key=os.path.getmtime, reverse=True):
        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        
        # Try to extract info from filename
        if filename.startswith("google_reviews_"):
            file_type = "📊 Full Reviews"
        elif filename.startswith("summary_"):
            file_type = "📋 Summary"
        else:
            file_type = "❓ Unknown"
        
        print(f"{file_type:12} | {filename}")
        print(f"{'':12} | Size: {file_size:,} bytes | Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)

def show_file_info(filename):
    """Show detailed information about a specific output file."""
    filepath = os.path.join("data/outputs", filename)
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filename}")
        return
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📄 File: {filename}")
        print("=" * 50)
        
        if "metadata" in data:
            metadata = data["metadata"]
            print(f"📊 Scraper Version: {metadata.get('scraper_version', 'N/A')}")
            print(f"🕐 Scraped At: {metadata.get('scraped_at', 'N/A')}")
            print(f"🏢 Properties: {metadata.get('total_properties', 'N/A')}")
            print(f"📝 Reviews: {metadata.get('total_reviews', 'N/A')}")
            print(f"📍 Properties: {', '.join(metadata.get('properties_processed', []))}")
        
        elif "scraping_summary" in data:
            summary = data["scraping_summary"]
            print(f"📊 Scraper Version: {summary.get('scraper_version', 'N/A')}")
            print(f"🕐 Timestamp: {summary.get('timestamp', 'N/A')}")
            print(f"🏢 Properties: {summary.get('total_properties', 'N/A')}")
            print(f"📝 Reviews: {summary.get('total_reviews', 'N/A')}")
            
            if "properties" in summary:
                print("\n🏢 Property Breakdown:")
                for prop_name, prop_data in summary["properties"].items():
                    print(f"  {prop_name}: {prop_data.get('review_count', 0)} reviews")
        
        file_size = os.path.getsize(filepath)
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        print(f"\n📁 File Size: {file_size:,} bytes")
        print(f"🕐 Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")

def cleanup_old_files(days_old=30):
    """Remove output files older than specified days."""
    outputs_dir = "data/outputs"
    if not os.path.exists(outputs_dir):
        print("❌ Outputs directory not found: data/outputs")
        return
    
    cutoff_date = datetime.now() - timedelta(days=days_old)
    files = glob.glob(os.path.join(outputs_dir, "*.json"))
    
    old_files = []
    for filepath in files:
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        if mod_time < cutoff_date:
            old_files.append(filepath)
    
    if not old_files:
        print(f"✅ No files older than {days_old} days found")
        return
    
    print(f"🗑️ Found {len(old_files)} files older than {days_old} days:")
    for filepath in old_files:
        filename = os.path.basename(filepath)
        mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        print(f"  {filename} (modified: {mod_time.strftime('%Y-%m-%d')})")
    
    response = input(f"\n❓ Delete these {len(old_files)} old files? (y/N): ")
    if response.lower() == 'y':
        deleted_count = 0
        for filepath in old_files:
            try:
                os.remove(filepath)
                deleted_count += 1
                print(f"🗑️ Deleted: {os.path.basename(filepath)}")
            except Exception as e:
                print(f"❌ Error deleting {os.path.basename(filepath)}: {str(e)}")
        
        print(f"✅ Deleted {deleted_count} old files")
    else:
        print("❌ Cleanup cancelled")

def main():
    parser = argparse.ArgumentParser(description='Manage scraper output files')
    parser.add_argument('action', choices=['list', 'info', 'cleanup'], 
                       help='Action to perform')
    parser.add_argument('--file', help='Filename for info action')
    parser.add_argument('--days', type=int, default=30, 
                       help='Days old for cleanup (default: 30)')
    
    args = parser.parse_args()
    
    if args.action == 'list':
        list_outputs()
    elif args.action == 'info':
        if not args.file:
            print("❌ Please specify a filename with --file")
            return
        show_file_info(args.file)
    elif args.action == 'cleanup':
        cleanup_old_files(args.days)

if __name__ == "__main__":
    main() 