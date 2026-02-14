#!/usr/bin/env python3
"""
Diagnostic script to test the Exoplanet website setup
"""

import os
import sys

def check_files():
    """Check if all required files exist"""
    print("=" * 60)
    print("FILE STRUCTURE CHECK")
    print("=" * 60)
    
    files_to_check = [
        'app.py',
        'templates/index.html',
        'static/styles.css',
        'static/app.js',
        'Random_Forest_model.joblib',
        'scaler.joblib'
    ]
    
    all_exist = True
    for file_path in files_to_check:
        exists = os.path.exists(file_path)
        status = "[OK]" if exists else "[MISSING]"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False
    
    return all_exist

def test_flask_app():
    """Test if Flask app can load"""
    print("\n" + "=" * 60)
    print("FLASK APP CHECK")
    print("=" * 60)
    
    try:
        from app import app
        print("[OK] Flask app imports successfully")
        
        with app.test_client() as client:
            # Test root route
            response = client.get('/')
            if response.status_code == 200:
                print("[OK] Root route (/) is working")
                # Check if it's HTML
                if b'<html' in response.data.lower():
                    print("[OK] Returns HTML content")
                else:
                    print("[ERROR] Does not return HTML content")
                    print(f"  Response: {response.data[:100]}")
            else:
                print(f"[ERROR] Root route returned status {response.status_code}")
            
            # Test static files
            static_response = client.get('/static/styles.css')
            if static_response.status_code == 200:
                print("[OK] Static CSS file is accessible")
            else:
                print(f"[ERROR] Static CSS returned status {static_response.status_code}")
            
            # Test API
            api_response = client.get('/health')
            if api_response.status_code == 200:
                print("[OK] API health endpoint is working")
            else:
                print(f"[ERROR] API health returned status {api_response.status_code}")
                
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def check_template_syntax():
    """Check if template syntax is correct"""
    print("\n" + "=" * 60)
    print("TEMPLATE SYNTAX CHECK")
    print("=" * 60)
    
    try:
        with open('templates/index.html', 'r') as f:
            content = f.read()
        
        # Check for url_for usage
        if '{{ url_for' in content:
            print("[OK] Template uses Flask url_for syntax")
        else:
            print("[ERROR] Template does not use Flask url_for syntax")
        
        # Check for static references
        if 'static/' in content or "filename='" in content:
            print("[OK] Static file references found")
        
        # Check file size
        size = len(content)
        print(f"[OK] Template size: {size} bytes")
        
    except Exception as e:
        print(f"[ERROR] Error reading template: {e}")
        return False
    
    return True

def main():
    print("\n" + "=" * 60)
    print("EXOPLANET WEBSITE DIAGNOSTIC TOOL")
    print("=" * 60 + "\n")
    
    files_ok = check_files()
    template_ok = check_template_syntax()
    flask_ok = test_flask_app()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if files_ok and template_ok and flask_ok:
        print("[OK] All checks passed! The website should be working.")
        print("\nTo start the server:")
        print("  python app.py")
        print("\nThen visit: http://localhost:5000")
    else:
        print("[ERROR] Some checks failed. Please review the errors above.")
        
        if not files_ok:
            print("\nMissing files. Make sure you have:")
            print("  - templates/index.html")
            print("  - static/styles.css")
            print("  - static/app.js")
        
        print("\nTroubleshooting steps:")
        print("  1. Ensure you're in the correct directory")
        print("  2. Check that Flask is installed: pip install flask flask-cors")
        print("  3. Clear browser cache: Ctrl+Shift+R")
        print("  4. Check browser console (F12) for JavaScript errors")
        print("  5. Try the test route: http://localhost:5000/test")

if __name__ == '__main__':
    main()
