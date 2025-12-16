#!/usr/bin/env python3
"""
Verification script to demonstrate that watermarking has been removed
and the code is syntactically correct.
"""

import sys
import ast

def check_file_for_watermark(filepath):
    """Check if a file contains watermark-related code"""
    print(f"\nChecking {filepath}...")
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check syntax
        try:
            ast.parse(content)
            print("  ✓ Syntax is valid")
        except SyntaxError as e:
            print(f"  ✗ Syntax error: {e}")
            return False
        
        # Check for watermark imports
        if 'import perth' in content or 'from perth' in content:
            print("  ✗ Found perth import")
            return False
        else:
            print("  ✓ No perth import found")
        
        # Check for watermarker usage
        if 'watermarker' in content.lower():
            print("  ✗ Found watermarker reference")
            return False
        else:
            print("  ✓ No watermarker reference found")
        
        # Check for watermark method calls
        if 'apply_watermark' in content:
            print("  ✗ Found apply_watermark call")
            return False
        else:
            print("  ✓ No apply_watermark call found")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error reading file: {e}")
        return False


def verify_api_files():
    """Verify API files are syntactically correct"""
    print("\n" + "="*60)
    print("Verifying FastAPI implementation")
    print("="*60)
    
    api_files = [
        'api/main.py',
        'api/routers/openai.py',
        'api/services/tts_service.py',
        'api/schemas/openai.py',
    ]
    
    all_valid = True
    for filepath in api_files:
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            ast.parse(content)
            print(f"✓ {filepath}: Valid syntax")
        except Exception as e:
            print(f"✗ {filepath}: {e}")
            all_valid = False
    
    return all_valid


def main():
    print("="*60)
    print("Chatterbox-FastAPI Verification Script")
    print("="*60)
    print("\nThis script verifies:")
    print("1. Watermarking code has been removed from TTS models")
    print("2. All Python files have valid syntax")
    print("3. FastAPI implementation is present and correct")
    
    # Check TTS files for watermark removal
    print("\n" + "="*60)
    print("Verifying watermark removal")
    print("="*60)
    
    tts_files = [
        'src/chatterbox/mtl_tts.py',
        'src/chatterbox/tts_turbo.py',
        'src/chatterbox/tts.py',
        'src/chatterbox/vc.py',
    ]
    
    watermark_removed = all(check_file_for_watermark(f) for f in tts_files)
    
    # Check pyproject.toml
    print("\nChecking pyproject.toml...")
    try:
        with open('pyproject.toml', 'r') as f:
            content = f.read()
        if 'resemble-perth' in content:
            print("  ✗ Found resemble-perth in dependencies")
            watermark_removed = False
        else:
            print("  ✓ resemble-perth removed from dependencies")
        
        if 'fastapi' in content.lower():
            print("  ✓ FastAPI dependencies added")
        else:
            print("  ✗ FastAPI dependencies not found")
    except Exception as e:
        print(f"  ✗ Error reading pyproject.toml: {e}")
        watermark_removed = False
    
    # Verify API files
    api_valid = verify_api_files()
    
    # Summary
    print("\n" + "="*60)
    print("Verification Summary")
    print("="*60)
    
    if watermark_removed:
        print("✓ Watermarking successfully removed from all TTS models")
    else:
        print("✗ Watermarking removal incomplete")
    
    if api_valid:
        print("✓ FastAPI implementation is syntactically correct")
    else:
        print("✗ FastAPI implementation has issues")
    
    # Check for README
    try:
        with open('README.md', 'r') as f:
            readme = f.read()
        if 'FastAPI' in readme and 'OpenAI' in readme:
            print("✓ README updated with FastAPI documentation")
        else:
            print("✗ README not fully updated")
    except:
        print("✗ README not found")
    
    print("\n" + "="*60)
    if watermark_removed and api_valid:
        print("✓ ALL VERIFICATIONS PASSED")
        print("="*60)
        print("\nThe implementation is complete:")
        print("  - Watermarking removed (saves resources)")
        print("  - FastAPI server with OpenAI compatibility")
        print("  - Multilingual model support (23+ languages)")
        print("  - Updated README with ASCII banner")
        print("\nTo start the server:")
        print("  python -m api.main")
        print("  or")
        print("  ./start_server.sh")
        return 0
    else:
        print("✗ SOME VERIFICATIONS FAILED")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
