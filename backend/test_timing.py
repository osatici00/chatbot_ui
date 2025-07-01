#!/usr/bin/env python3
"""
Test script to verify the 15-second timing with 6 progress steps
"""

import asyncio
import time
from datetime import datetime

# Add the current directory to the Python path
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import simulate_analysis_with_progress, ProgressLogger

async def test_timing():
    """Test that the progress takes exactly 15 seconds with 6 steps"""
    print("🕐 Testing 15-second Progress Timing")
    print("=" * 50)
    
    # Initialize progress logger
    logger = ProgressLogger()
    
    # Test session ID
    test_session_id = "timing-test-session"
    
    print(f"Starting test at: {datetime.now().strftime('%H:%M:%S')}")
    start_time = time.time()
    
    # Run the simulation
    await simulate_analysis_with_progress(test_session_id, "test query", "chart")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"Completed test at: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Total time: {total_time:.2f} seconds")
    
    # Check if timing is correct (15 seconds ± 0.5 seconds tolerance)
    if 14.5 <= total_time <= 15.5:
        print("✅ Timing is correct! (~15 seconds)")
    else:
        print(f"❌ Timing is incorrect! Expected ~15 seconds, got {total_time:.2f} seconds")
    
    # Check progress logs
    logs = logger.get_progress_logs(test_session_id)
    print(f"\n📋 Progress Steps ({len(logs)} total):")
    
    expected_steps = [
        "Scanning databases",
        "Analyzing", 
        "Fetching relevant data",
        "Writing code",
        "Executing code",
        "Preparing response",
        "Completed"
    ]
    
    for i, log in enumerate(logs):
        step_time = datetime.fromisoformat(log['timestamp'])
        print(f"  {i+1}. {log['step']} - {step_time.strftime('%H:%M:%S')}")
        
        if i < len(expected_steps) and log['step'] == expected_steps[i]:
            print(f"     ✅ Correct step")
        else:
            print(f"     ❌ Expected: {expected_steps[i] if i < len(expected_steps) else 'Unknown'}")
    
    print(f"\n🎯 Expected 6 main steps + 1 completion = 7 total")
    if len(logs) == 7:
        print("✅ Correct number of steps!")
    else:
        print(f"❌ Wrong number of steps! Got {len(logs)}, expected 7")
    
    print("\n" + "=" * 50)
    print("⏱️  Timing test complete!")

if __name__ == "__main__":
    asyncio.run(test_timing()) 