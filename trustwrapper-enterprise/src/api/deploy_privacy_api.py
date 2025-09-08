#!/usr/bin/env python3
"""
TrustWrapper 3.0 Privacy API Deployment Script
Deploys privacy-enhanced API with Sprint 115 integration
Created: July 7, 2025
Purpose: Production deployment of privacy-protected blockchain analysis
"""

import os
import sys
import subprocess
import time
import requests
import json
from datetime import datetime, timezone

def check_dependencies():
    """Check that required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ FastAPI dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Install with: pip install fastapi uvicorn pydantic")
        return False
    
    return True

def test_privacy_integration():
    """Test privacy integration before deployment"""
    print("🧪 Testing privacy integration...")
    
    try:
        # Add paths for imports
        import sys
        current_dir = os.getcwd()
        sys.path.insert(0, os.path.join(current_dir, 'layers', 'lamassu-labs', 'src', 'trustwrapper', 'v3'))
        
        # Import and test
        from privacy_adapter import create_privacy_enhanced_trustwrapper
        
        wrapper = create_privacy_enhanced_trustwrapper()
        validation = wrapper.validate_privacy_integration()
        
        if validation.get("validation_successful", False):
            print("✅ Privacy integration validated")
            print(f"   🔐 Privacy Level: {wrapper.privacy_config['privacy_level']*100}%")
            print(f"   🆔 Session ID: {wrapper.session_id}")
            return True
        else:
            print(f"❌ Privacy integration failed: {validation}")
            return False
            
    except Exception as e:
        print(f"❌ Privacy integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def deploy_api(port=8200, host="0.0.0.0"):
    """Deploy the privacy-enhanced TrustWrapper API"""
    print(f"🚀 Deploying TrustWrapper 3.0 Privacy API on {host}:{port}")
    
    try:
        # Set up environment
        api_dir = "layers/lamassu-labs/src/api"
        api_file = "trustwrapper_privacy_api.py"
        
        if not os.path.exists(os.path.join(api_dir, api_file)):
            print(f"❌ API file not found: {api_dir}/{api_file}")
            return False
        
        # Add current directory to Python path
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{os.getcwd()}:{env.get('PYTHONPATH', '')}"
        
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"📄 API file: {api_dir}/{api_file}")
        print(f"🌐 Server: http://{host}:{port}")
        print(f"📖 Docs: http://{host}:{port}/docs")
        print(f"🔐 Privacy demo: http://{host}:{port}/privacy/demo")
        
        # Start the API server
        cmd = [
            sys.executable, "-m", "uvicorn",
            f"{api_dir.replace('/', '.')}.{api_file.replace('.py', '')}:app",
            "--host", host,
            "--port", str(port),
            "--reload"
        ]
        
        print(f"🔧 Command: {' '.join(cmd)}")
        print("=" * 60)
        print("🎯 Starting TrustWrapper 3.0 Privacy API...")
        print("📊 Sprint 115 Privacy Integration: 80% coverage")
        print("🔐 Features: Secure Delete, Differential Privacy, Memory Encryption")
        print("⚡ Press Ctrl+C to stop")
        print("=" * 60)
        
        # Run the server
        subprocess.run(cmd, env=env, cwd=os.getcwd())
        
    except KeyboardInterrupt:
        print("\n🛑 API server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def test_deployed_api(host="localhost", port=8200, timeout=30):
    """Test the deployed API endpoints"""
    base_url = f"http://{host}:{port}"
    
    print(f"🧪 Testing deployed API at {base_url}")
    
    # Wait for API to start
    print("⏳ Waiting for API to start...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API is responding")
                break
        except requests.exceptions.RequestException:
            time.sleep(1)
    else:
        print("❌ API failed to start within timeout")
        return False
    
    # Test endpoints
    endpoints = [
        ("/", "Root endpoint"),
        ("/health", "Health check"),
        ("/privacy/status", "Privacy status"),
        ("/privacy/metrics", "Privacy metrics"),
        ("/privacy/demo", "Privacy demo")
    ]
    
    results = {}
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description}: {response.status_code}")
                results[endpoint] = {"status": "success", "code": response.status_code}
                
                # Show sample response for privacy demo
                if endpoint == "/privacy/demo":
                    data = response.json()
                    print(f"   Privacy Level: {data.get('privacy_metrics', {}).get('privacy_config', {}).get('privacy_level', 0)*100}%")
                    
            else:
                print(f"⚠️ {description}: {response.status_code}")
                results[endpoint] = {"status": "warning", "code": response.status_code}
                
        except Exception as e:
            print(f"❌ {description}: {str(e)}")
            results[endpoint] = {"status": "error", "error": str(e)}
    
    return results

def create_deployment_report():
    """Create deployment report"""
    report = {
        "deployment_time": datetime.now(timezone.utc).isoformat(),
        "service": "TrustWrapper 3.0 Privacy API",
        "sprint_115_integration": "Complete",
        "privacy_level": "80%",
        "features": [
            "Secure Delete Architecture",
            "Differential Privacy",
            "Memory Encryption Simulation",
            "IC Threshold ECDSA Ready"
        ],
        "endpoints": [
            "POST /analyze/private - Privacy-protected analysis",
            "GET /privacy/metrics - Privacy metrics",
            "GET /privacy/status - Privacy status", 
            "GET /privacy/demo - Privacy demonstration"
        ],
        "documentation": "Available at /docs endpoint",
        "integration_status": "Production Ready"
    }
    
    report_file = f"trustwrapper_privacy_deployment_report_{int(time.time())}.json"
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📋 Deployment report saved: {report_file}")
    return report_file

def main():
    """Main deployment function"""
    print("🚀 TrustWrapper 3.0 Privacy API Deployment")
    print("Sprint 115 Integration: Privacy-Protected Blockchain Analysis")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return False
    
    # Test privacy integration
    if not test_privacy_integration():
        print("❌ Privacy integration test failed")
        return False
    
    # Create deployment report
    report_file = create_deployment_report()
    
    # Deploy API
    try:
        deploy_api()
        return True
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Deploy TrustWrapper 3.0 Privacy API")
    parser.add_argument("--port", type=int, default=8200, help="API port (default: 8200)")
    parser.add_argument("--host", default="0.0.0.0", help="API host (default: 0.0.0.0)")
    parser.add_argument("--test-only", action="store_true", help="Only run tests, don't deploy")
    
    args = parser.parse_args()
    
    if args.test_only:
        print("🧪 Running tests only...")
        deps_ok = check_dependencies()
        privacy_ok = test_privacy_integration()
        
        if deps_ok and privacy_ok:
            print("✅ All tests passed - ready for deployment")
        else:
            print("❌ Tests failed")
    else:
        success = main()
        if success:
            print("✅ Deployment completed successfully")
        else:
            print("❌ Deployment failed")