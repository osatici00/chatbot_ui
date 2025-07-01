#!/usr/bin/env python3
"""
Test script to verify all response types are working properly
"""
import requests
import json

def test_all_response_types():
    """Test that all response types work correctly"""
    
    url = "http://localhost:8001/api/query"
    
    # Test queries matching the frontend examples exactly
    test_cases = [
        # Chart examples - user's exact queries
        {
            "query": "Show me a revenue chart by region",
            "expected_type": "chart",
            "description": "📊 Bar Chart Example"
        },
        {
            "query": "Create a customer satisfaction trend line", 
            "expected_type": "chart",
            "description": "📈 Line Chart Example"
        },
        {
            "query": "Display support ticket distribution pie chart",
            "expected_type": "chart", 
            "description": "🥧 Pie Chart Example"
        },
        {
            "query": "Generate a scatter plot of order value vs satisfaction",
            "expected_type": "chart",
            "description": "⚫ Scatter Plot Example"
        },
        # Other response types
        {
            "query": "Analyze customer insights and provide summary",
            "expected_type": "text",
            "description": "📄 Text Analysis Example"
        },
        {
            "query": "Export sales data to Excel spreadsheet",
            "expected_type": "file",
            "description": "📥 Excel Download Example"
        },
        {
            "query": "Check processing status of my request",
            "expected_type": "progress",
            "description": "⏳ Progress Status Example"
        }
    ]
    
    print("🧪 Testing All Response Types with Exact Frontend Examples...")
    print("=" * 70)
    
    success_count = 0
    total_count = len(test_cases)
    
    for test_case in test_cases:
        query = test_case["query"]
        expected_type = test_case["expected_type"]
        description = test_case["description"]
        
        print(f"\n{description}")
        print(f"   Query: '{query}'")
        print(f"   Expected: {expected_type}")
        
        try:
            response = requests.post(url, json={
                "user_query": query,
                "user_email": "test@example.com"
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                actual_type = data.get('response_type')
                
                if actual_type == expected_type:
                    print(f"   ✅ PASS: Got {actual_type}")
                    success_count += 1
                    
                    # Show additional details based on response type
                    if actual_type == "chart" and data.get('chart_data'):
                        chart_data = data['chart_data']
                        print(f"   📊 Chart Type: {chart_data.get('type')}")
                        print(f"   📝 Title: {chart_data.get('title')}")
                    elif actual_type == "file" and data.get('file_info'):
                        file_info = data['file_info']
                        print(f"   📁 File: {file_info.get('filename')}")
                        print(f"   📐 Size: {file_info.get('file_size')}")
                    elif actual_type == "progress" and data.get('progress'):
                        progress = data['progress']
                        print(f"   ⏳ Step: {progress.get('current_step')}")
                        print(f"   📊 Progress: {progress.get('percentage')}%")
                    elif actual_type == "text":
                        content = data.get('response_content', '')
                        print(f"   📄 Content Length: {len(content)} chars")
                else:
                    print(f"   ❌ FAIL: Expected {expected_type}, got {actual_type}")
                    
            else:
                print(f"   ❌ FAIL: HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ FAIL: Cannot connect to API")
            break
        except Exception as e:
            print(f"   ❌ FAIL: {e}")
    
    print("\n" + "=" * 70)
    print(f"🎯 Results: {success_count}/{total_count} tests passed")
    
    if success_count == total_count:
        print("🎉 All response types working perfectly!")
        print("✨ Frontend examples will trigger correct response types!")
    else:
        print("⚠️  Some response types need attention")
    
    return success_count == total_count

def test_health_check():
    """Test that the API is running"""
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            return True
        else:
            print("❌ API Health Check: FAILED")
            return False
    except:
        print("❌ API Health Check: FAILED (Connection Error)")
        return False

if __name__ == "__main__":
    print("🚀 ChatGPT UI Demo - Frontend Example Response Type Test")
    print("=" * 70)
    
    if test_health_check():
        test_all_response_types()
    else:
        print("\n💡 Start the backend server first:")
        print("   python app.py") 