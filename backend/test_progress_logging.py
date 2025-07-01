#!/usr/bin/env python3
"""
Test script for progress logging system
Tests the progress logging functionality without running the full server
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import ProgressLogger, simulate_analysis_with_progress

async def test_progress_logging():
    """Test the progress logging system"""
    print("🧪 Testing Progress Logging System")
    print("=" * 50)
    
    # Initialize progress logger
    logger = ProgressLogger()
    
    # Test session ID
    test_session_id = "test-session-123"
    
    # Test 1: Basic progress logging
    print("\n1. Testing basic progress logging...")
    await logger.log_progress(
        session_id=test_session_id,
        step="Testing",
        message="This is a test log entry",
        step_number=1,
        total_steps=3
    )
    
    # Test 2: Simulate full analysis
    print("\n2. Testing full analysis simulation...")
    await simulate_analysis_with_progress(test_session_id, "show me a bar chart", "chart")
    
    # Test 3: Verify logs were written to file
    print("\n3. Verifying log file creation...")
    log_file = logger.get_log_file_path(test_session_id)
    
    if os.path.exists(log_file):
        print(f"✅ Log file created: {log_file}")
        
        with open(log_file, 'r') as f:
            logs = json.load(f)
        
        print(f"✅ Found {len(logs)} log entries")
        
        # Display some log entries
        for i, log in enumerate(logs[:3]):
            print(f"   Log {i+1}: {log['step']} - {log['message'][:50]}...")
    else:
        print(f"❌ Log file not found: {log_file}")
    
    # Test 4: Test memory retrieval
    print("\n4. Testing memory retrieval...")
    memory_logs = logger.get_progress_logs(test_session_id)
    print(f"✅ Retrieved {len(memory_logs)} logs from memory")
    
    # Test 5: Test notifications
    print("\n5. Testing notification system...")
    logger.add_notification(test_session_id, "Test completed!")
    notification = logger.get_notifications(test_session_id)
    
    if notification:
        print(f"✅ Notification created: {notification['message']}")
        print(f"   Read status: {notification['read']}")
        
        # Mark as read
        logger.mark_notification_read(test_session_id)
        updated_notification = logger.get_notifications(test_session_id)
        print(f"   After marking read: {updated_notification['read']}")
    else:
        print("❌ Notification not found")
    
    # Test 6: Test different response types
    print("\n6. Testing different response types...")
    
    response_types = ["chart", "file", "text"]
    for response_type in response_types:
        test_session = f"test-{response_type}-session"
        print(f"   Testing {response_type} response...")
        await simulate_analysis_with_progress(test_session, f"test {response_type}", response_type)
        
        logs = logger.get_progress_logs(test_session)
        print(f"   ✅ {response_type}: {len(logs)} steps logged")
    
    print("\n" + "=" * 50)
    print("✅ Progress logging system test completed!")
    print("\nGenerated files:")
    
    # List all log files
    for file in os.listdir(logger.logs_dir):
        if file.endswith('_progress.json'):
            file_path = os.path.join(logger.logs_dir, file)
            file_size = os.path.getsize(file_path)
            print(f"   {file} ({file_size} bytes)")

if __name__ == "__main__":
    asyncio.run(test_progress_logging()) 