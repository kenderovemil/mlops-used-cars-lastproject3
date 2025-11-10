#!/usr/bin/env python3
"""
Test script to validate the jobs review functions work correctly.
This tests the CSV and PDF generation functions with mock data.
"""

import os
import sys
import tempfile
from datetime import datetime

# Import the functions we want to test
sys.path.insert(0, os.path.dirname(__file__))
from review_jobs import save_to_csv, save_to_pdf, format_datetime, get_dataset_input

def test_format_datetime():
    """Test datetime formatting."""
    print("Testing format_datetime...")
    
    # Test with datetime object
    dt = datetime(2025, 11, 10, 15, 30, 45)
    result = format_datetime(dt)
    assert result == "2025-11-10 15:30:45", f"Expected '2025-11-10 15:30:45', got '{result}'"
    
    # Test with string
    result = format_datetime("2025-11-10 12:00:00")
    assert result == "2025-11-10 12:00:00", f"Expected '2025-11-10 12:00:00', got '{result}'"
    
    # Test with None
    result = format_datetime(None)
    assert result == "N/A", f"Expected 'N/A', got '{result}'"
    
    print("✅ format_datetime tests passed")

def test_csv_generation():
    """Test CSV file generation."""
    print("\nTesting CSV generation...")
    
    # Create mock job data
    mock_jobs = [
        {
            'Job ID': 'job_001',
            'Display Name': 'Test Job 1',
            'Status': 'Completed',
            'Dataset': 'azureml:test-data:1',
            'Start Time': '2025-11-10 10:00:00',
            'End Time': '2025-11-10 10:30:00'
        },
        {
            'Job ID': 'job_002',
            'Display Name': 'Test Job 2',
            'Status': 'Running',
            'Dataset': 'N/A',
            'Start Time': '2025-11-10 11:00:00',
            'End Time': 'N/A'
        }
    ]
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        tmp_path = tmp.name
    
    try:
        # Test CSV generation
        result = save_to_csv(mock_jobs, tmp_path)
        assert result == True, "CSV generation should return True"
        
        # Verify file exists
        assert os.path.exists(tmp_path), "CSV file should exist"
        
        # Verify file content
        with open(tmp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert 'Job ID' in content, "CSV should contain header"
            assert 'job_001' in content, "CSV should contain job data"
            assert 'Test Job 1' in content, "CSV should contain display name"
        
        print("✅ CSV generation tests passed")
        print(f"   Sample CSV file created at: {tmp_path}")
        
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def test_pdf_generation():
    """Test PDF file generation."""
    print("\nTesting PDF generation...")
    
    # Create mock job data
    mock_jobs = [
        {
            'Job ID': 'job_001',
            'Display Name': 'Test Job 1',
            'Status': 'Completed',
            'Dataset': 'azureml:test-data:1',
            'Start Time': '2025-11-10 10:00:00',
            'End Time': '2025-11-10 10:30:00'
        },
        {
            'Job ID': 'job_002',
            'Display Name': 'Test Job 2',
            'Status': 'Failed',
            'Dataset': 'azureml:test-data:2',
            'Start Time': '2025-11-10 11:00:00',
            'End Time': '2025-11-10 11:15:00'
        },
        {
            'Job ID': 'job_003',
            'Display Name': 'Test Job 3',
            'Status': 'Running',
            'Dataset': 'N/A',
            'Start Time': '2025-11-10 12:00:00',
            'End Time': 'N/A'
        }
    ]
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pdf') as tmp:
        tmp_path = tmp.name
    
    try:
        # Test PDF generation
        result = save_to_pdf(mock_jobs, tmp_path, "project_III_MLOPS")
        assert result == True, "PDF generation should return True"
        
        # Verify file exists
        assert os.path.exists(tmp_path), "PDF file should exist"
        
        # Verify file is not empty
        file_size = os.path.getsize(tmp_path)
        assert file_size > 0, f"PDF file should not be empty (size: {file_size} bytes)"
        
        # Verify it's a PDF file (check magic bytes)
        with open(tmp_path, 'rb') as f:
            header = f.read(4)
            assert header == b'%PDF', f"File should start with PDF magic bytes, got {header}"
        
        print("✅ PDF generation tests passed")
        print(f"   Sample PDF file created at: {tmp_path}")
        print(f"   File size: {file_size} bytes")
        
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def main():
    """Run all tests."""
    print("="*60)
    print("Running Jobs Review Script Tests")
    print("="*60)
    
    try:
        test_format_datetime()
        test_csv_generation()
        test_pdf_generation()
        
        print("\n" + "="*60)
        print("✅ All tests passed successfully!")
        print("="*60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
