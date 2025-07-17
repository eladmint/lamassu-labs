#!/usr/bin/env python3
"""
Activate Custom Interface on Ziggurat Satellite
Override the default Juno template with our monitoring dashboard
"""

import asyncio
<<<<<<< HEAD
=======
import json
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
import sys
from pathlib import Path

# Add parent directories to path for imports
<<<<<<< HEAD
sys.path.append(
    str(Path(__file__).parent.parent.parent / "agent_forge" / "ziggurat-intelligence")
)
=======
sys.path.append(str(Path(__file__).parent.parent.parent / "agent_forge" / "ziggurat-intelligence"))
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752

from integrations.icp_client import ICPClient


async def activate_monitoring_interface():
    """Activate the custom monitoring interface on the Ziggurat satellite."""
<<<<<<< HEAD

    print("🚀 Activating custom monitoring interface on Ziggurat satellite...")
    print("📋 This will override the default Juno template")

    try:
        async with ICPClient(satellite_id="bvxuo-uaaaa-aaaal-asgua-cai") as client:

            print("🔍 Testing satellite connectivity...")
            health = await client.query_satellite_health()
            print(f"✅ Satellite status: {health.status}")

            # Store interface activation configuration
            print("⚙️ Storing interface activation configuration...")

=======
    
    print("🚀 Activating custom monitoring interface on Ziggurat satellite...")
    print("📋 This will override the default Juno template")
    
    try:
        async with ICPClient(satellite_id="bvxuo-uaaaa-aaaal-asgua-cai") as client:
            
            print("🔍 Testing satellite connectivity...")
            health = await client.query_satellite_health()
            print(f"✅ Satellite status: {health.status}")
            
            # Store interface activation configuration
            print("⚙️ Storing interface activation configuration...")
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            activation_config = {
                "interface_mode": "custom_monitoring_dashboard",
                "override_default": True,
                "routes": {
                    "/": "lamassu_landing_page",
                    "/dashboard": "monitoring_dashboard",
<<<<<<< HEAD
                    "/api/monitoring": "monitoring_api",
=======
                    "/api/monitoring": "monitoring_api"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                },
                "branding": {
                    "company": "Lamassu Labs",
                    "product": "Contract Monitoring Dashboard",
<<<<<<< HEAD
                    "theme": "dark_professional",
=======
                    "theme": "dark_professional"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                },
                "features": {
                    "auto_refresh": True,
                    "real_time_alerts": True,
                    "api_access": True,
<<<<<<< HEAD
                    "cors_enabled": True,
                },
            }

            config_result = await client.store_data(
                {
                    "type": "interface_activation",
                    "config": activation_config,
                    "priority": "high",
                    "override_default": True,
                    "timestamp": int(asyncio.get_event_loop().time()),
                }
            )

            if config_result["success"]:
                print(f"✅ Activation config stored: {config_result['storage_id']}")
            else:
                print(
                    f"❌ Failed to store activation config: {config_result.get('error')}"
                )
                return False

            # Create the index override
            print("🎨 Creating index page override...")

            index_override = await create_index_override()

            index_result = await client.store_data(
                {
                    "type": "index_override",
                    "content": index_override,
                    "route": "/",
                    "priority": "critical",
                    "content_type": "text/html",
                }
            )

=======
                    "cors_enabled": True
                }
            }
            
            config_result = await client.store_data({
                "type": "interface_activation",
                "config": activation_config,
                "priority": "high",
                "override_default": True,
                "timestamp": int(asyncio.get_event_loop().time())
            })
            
            if config_result["success"]:
                print(f"✅ Activation config stored: {config_result['storage_id']}")
            else:
                print(f"❌ Failed to store activation config: {config_result.get('error')}")
                return False
            
            # Create the index override
            print("🎨 Creating index page override...")
            
            index_override = await create_index_override()
            
            index_result = await client.store_data({
                "type": "index_override",
                "content": index_override,
                "route": "/",
                "priority": "critical",
                "content_type": "text/html"
            })
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            if index_result["success"]:
                print(f"✅ Index override stored: {index_result['storage_id']}")
            else:
                print(f"❌ Failed to store index override: {index_result.get('error')}")
                return False
<<<<<<< HEAD

            # Store template override instructions
            print("📝 Storing template override instructions...")

=======
            
            # Store template override instructions
            print("📝 Storing template override instructions...")
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            override_instructions = {
                "action": "replace_default_template",
                "target": "index.html",
                "source": index_result["storage_id"],
                "backup_original": True,
<<<<<<< HEAD
                "activation_immediate": True,
            }

            instruction_result = await client.store_data(
                {
                    "type": "template_override_instructions",
                    "instructions": override_instructions,
                    "execution_priority": "immediate",
                }
            )

            if instruction_result["success"]:
                print(
                    f"✅ Override instructions stored: {instruction_result['storage_id']}"
                )
            else:
                print(
                    f"❌ Failed to store override instructions: {instruction_result.get('error')}"
                )

            # Create activation manifest
            print("📋 Creating activation manifest...")

=======
                "activation_immediate": True
            }
            
            instruction_result = await client.store_data({
                "type": "template_override_instructions",
                "instructions": override_instructions,
                "execution_priority": "immediate"
            })
            
            if instruction_result["success"]:
                print(f"✅ Override instructions stored: {instruction_result['storage_id']}")
            else:
                print(f"❌ Failed to store override instructions: {instruction_result.get('error')}")
            
            # Create activation manifest
            print("📋 Creating activation manifest...")
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            manifest = {
                "activation_id": f"lamassu_monitoring_{int(asyncio.get_event_loop().time())}",
                "components": {
                    "activation_config": config_result["storage_id"],
                    "index_override": index_result["storage_id"],
<<<<<<< HEAD
                    "override_instructions": instruction_result["storage_id"],
=======
                    "override_instructions": instruction_result["storage_id"]
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                },
                "status": "ready_for_activation",
                "url_endpoints": [
                    "https://bvxuo-uaaaa-aaaal-asgua-cai.icp0.io/",
                    "https://bvxuo-uaaaa-aaaal-asgua-cai.icp0.io/dashboard",
<<<<<<< HEAD
                    "https://bvxuo-uaaaa-aaaal-asgua-cai.icp0.io/api/monitoring",
                ],
            }

            manifest_result = await client.store_data(
                {
                    "type": "activation_manifest",
                    "manifest": manifest,
                    "activation_ready": True,
                }
            )

            if manifest_result["success"]:
                print(f"✅ Activation manifest stored: {manifest_result['storage_id']}")
            else:
                print(
                    f"❌ Failed to store activation manifest: {manifest_result.get('error')}"
                )

=======
                    "https://bvxuo-uaaaa-aaaal-asgua-cai.icp0.io/api/monitoring"
                ]
            }
            
            manifest_result = await client.store_data({
                "type": "activation_manifest",
                "manifest": manifest,
                "activation_ready": True
            })
            
            if manifest_result["success"]:
                print(f"✅ Activation manifest stored: {manifest_result['storage_id']}")
            else:
                print(f"❌ Failed to store activation manifest: {manifest_result.get('error')}")
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            print("\n🎉 Custom interface activation complete!")
            print("\n📋 Activation Summary:")
            print(f"   🔧 Config: {config_result['storage_id']}")
            print(f"   🎨 Index Override: {index_result['storage_id']}")
            print(f"   📝 Instructions: {instruction_result['storage_id']}")
            print(f"   📋 Manifest: {manifest_result['storage_id']}")
<<<<<<< HEAD

            print("\n🌐 Your custom monitoring dashboard should now be visible at:")
            print("   📍 https://bvxuo-uaaaa-aaaal-asgua-cai.icp0.io/")

            print("\n💡 If you still see the default Juno page:")
            print("   1. Wait 1-2 minutes for canister update propagation")
            print("   2. Clear browser cache (Cmd+Shift+R)")
            print(
                "   3. Try the raw endpoint: https://bvxuo-uaaaa-aaaal-asgua-cai.raw.icp0.io/"
            )

            return True

=======
            
            print("\n🌐 Your custom monitoring dashboard should now be visible at:")
            print("   📍 https://bvxuo-uaaaa-aaaal-asgua-cai.icp0.io/")
            
            print("\n💡 If you still see the default Juno page:")
            print("   1. Wait 1-2 minutes for canister update propagation")
            print("   2. Clear browser cache (Cmd+Shift+R)")
            print("   3. Try the raw endpoint: https://bvxuo-uaaaa-aaaal-asgua-cai.raw.icp0.io/")
            
            return True
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    except Exception as e:
        print(f"❌ Activation failed: {e}")
        return False


async def create_index_override():
    """Create the index page that will override the default Juno template."""
<<<<<<< HEAD

    return """<!DOCTYPE html>
=======
    
    return '''<!DOCTYPE html>
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lamassu Labs - Contract Monitoring Dashboard</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛰️</text></svg>">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .container {
            max-width: 900px;
            text-align: center;
            padding: 50px;
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
            border-radius: 25px;
<<<<<<< HEAD
            box-shadow:
=======
            box-shadow: 
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                0 25px 80px rgba(0, 0, 0, 0.6),
                0 0 100px rgba(0, 255, 136, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(42, 42, 62, 0.8);
            backdrop-filter: blur(20px);
            position: relative;
            z-index: 1;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .logo {
            font-size: 5em;
            margin-bottom: 25px;
            animation: float 6s ease-in-out infinite;
            filter: drop-shadow(0 0 20px rgba(0, 255, 136, 0.3));
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(5deg); }
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .title {
            font-size: 3em;
            margin-bottom: 15px;
            background: linear-gradient(45deg, #00ff88, #00d4ff, #ffffff);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            animation: gradient 4s ease infinite;
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.3);
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .subtitle {
            font-size: 1.4em;
            color: #b0b0b0;
            margin-bottom: 15px;
            line-height: 1.6;
            font-weight: 300;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .tagline {
            font-size: 1.1em;
            color: #888;
            margin-bottom: 40px;
            font-style: italic;
        }
<<<<<<< HEAD

        .btn-container {
            margin: 40px 0;
        }

=======
        
        .btn-container {
            margin: 40px 0;
        }
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .btn {
            display: inline-block;
            background: linear-gradient(45deg, #00ff88, #00d4ff);
            color: #000;
            text-decoration: none;
            padding: 18px 35px;
            border-radius: 15px;
            font-weight: 700;
            font-size: 1.2em;
            margin: 15px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
<<<<<<< HEAD
            box-shadow:
=======
            box-shadow: 
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                0 8px 25px rgba(0, 255, 136, 0.3),
                0 0 0 0 rgba(0, 255, 136, 0.4);
            position: relative;
            overflow: hidden;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
<<<<<<< HEAD

        .btn:hover::before {
            left: 100%;
        }

        .btn:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow:
                0 15px 40px rgba(0, 255, 136, 0.5),
                0 0 30px rgba(0, 212, 255, 0.3);
        }

        .btn:active {
            transform: translateY(-2px) scale(1.02);
        }

=======
        
        .btn:hover::before {
            left: 100%;
        }
        
        .btn:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 
                0 15px 40px rgba(0, 255, 136, 0.5),
                0 0 30px rgba(0, 212, 255, 0.3);
        }
        
        .btn:active {
            transform: translateY(-2px) scale(1.02);
        }
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 25px;
            margin-top: 50px;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .status-card {
            background: linear-gradient(135deg, rgba(22, 33, 62, 0.8) 0%, rgba(16, 21, 46, 0.8) 100%);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(42, 42, 62, 0.6);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .status-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00ff88, #00d4ff);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
<<<<<<< HEAD

        .status-card:hover {
            transform: translateY(-8px);
            box-shadow:
=======
        
        .status-card:hover {
            transform: translateY(-8px);
            box-shadow: 
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                0 15px 35px rgba(0, 0, 0, 0.3),
                0 0 25px rgba(0, 255, 136, 0.1);
            border-color: rgba(0, 255, 136, 0.3);
        }
<<<<<<< HEAD

        .status-card:hover::before {
            opacity: 1;
        }

=======
        
        .status-card:hover::before {
            opacity: 1;
        }
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .status-title {
            color: #00ff88;
            font-weight: 700;
            margin-bottom: 10px;
            font-size: 1.1em;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .status-text {
            color: #ccc;
            font-size: 0.95em;
            line-height: 1.5;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .status-indicator {
            display: inline-block;
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: #00ff88;
            margin-right: 10px;
            animation: pulse 2s infinite;
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.1); }
            100% { opacity: 1; transform: scale(1); }
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .powered-by {
            margin-top: 50px;
            padding-top: 30px;
            border-top: 1px solid rgba(42, 42, 62, 0.6);
            color: #666;
            font-size: 0.95em;
            line-height: 1.6;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        .tech-badge {
            display: inline-block;
            background: rgba(0, 255, 136, 0.1);
            color: #00ff88;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            margin: 5px;
            border: 1px solid rgba(0, 255, 136, 0.3);
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        /* Background animation */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
<<<<<<< HEAD
            background:
=======
            background: 
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                radial-gradient(circle at 20% 50%, rgba(0, 255, 136, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(0, 212, 255, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(0, 255, 136, 0.02) 0%, transparent 50%);
            animation: backgroundShift 20s ease infinite;
            z-index: -1;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        @keyframes backgroundShift {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        /* Auto-redirect notification */
        .redirect-notice {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: rgba(0, 255, 136, 0.1);
            color: #00ff88;
            padding: 15px 20px;
            border-radius: 10px;
            border: 1px solid rgba(0, 255, 136, 0.3);
            font-size: 0.9em;
            opacity: 0;
            transform: translateY(100px);
            animation: slideUp 0.5s ease 6s forwards;
        }
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        @keyframes slideUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🛰️</div>
        <h1 class="title">Lamassu Labs</h1>
        <h2 class="subtitle">Contract Monitoring Dashboard</h2>
        <p class="tagline">Guardian of AI Trust • Powered by Blockchain Intelligence</p>
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        <div class="btn-container">
            <a href="/dashboard" class="btn">📊 View Dashboard</a>
            <a href="/api/monitoring" class="btn">🔧 API Access</a>
        </div>
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        <div class="status-grid">
            <div class="status-card">
                <div class="status-title">🌍 Network Status</div>
                <div class="status-text">
                    <span class="status-indicator"></span>
                    Internet Computer Protocol (ICP) Mainnet
                </div>
            </div>
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            <div class="status-card">
                <div class="status-title">🛰️ Satellite Health</div>
                <div class="status-text">
                    Ziggurat Intelligence<br>
                    <code>bvxuo-uaaaa-aaaal-asgua-cai</code>
                </div>
            </div>
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            <div class="status-card">
                <div class="status-title">⚡ Real-time Monitoring</div>
                <div class="status-text">
                    Aleo smart contracts<br>
                    Live health & performance tracking
                </div>
            </div>
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            <div class="status-card">
                <div class="status-title">🔐 Security</div>
                <div class="status-text">
                    Blockchain-verified data integrity<br>
                    Cryptographic proof validation
                </div>
            </div>
        </div>
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        <div class="powered-by">
            <strong>Powered by:</strong><br>
            <span class="tech-badge">Lamassu Labs TrustWrapper</span>
            <span class="tech-badge">Ziggurat Intelligence</span>
            <span class="tech-badge">Internet Computer Protocol</span>
            <span class="tech-badge">Aleo Blockchain</span>
        </div>
    </div>
<<<<<<< HEAD

    <div class="redirect-notice">
        🚀 Auto-redirecting to dashboard in <span id="countdown">8</span>s
    </div>

=======
    
    <div class="redirect-notice">
        🚀 Auto-redirecting to dashboard in <span id="countdown">8</span>s
    </div>
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    <script>
        // Countdown timer
        let countdown = 8;
        const countdownElement = document.getElementById('countdown');
<<<<<<< HEAD

        const timer = setInterval(() => {
            countdown--;
            countdownElement.textContent = countdown;

=======
        
        const timer = setInterval(() => {
            countdown--;
            countdownElement.textContent = countdown;
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            if (countdown <= 0) {
                clearInterval(timer);
                window.location.href = '/dashboard';
            }
        }, 1000);
<<<<<<< HEAD

        // Prevent redirect if user interacts with the page
        let userInteracted = false;

=======
        
        // Prevent redirect if user interacts with the page
        let userInteracted = false;
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        document.addEventListener('click', () => {
            userInteracted = true;
            clearInterval(timer);
            document.querySelector('.redirect-notice').style.display = 'none';
        });
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        document.addEventListener('scroll', () => {
            userInteracted = true;
            clearInterval(timer);
            document.querySelector('.redirect-notice').style.display = 'none';
        });
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        // Add hover effects
        document.querySelectorAll('.status-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                if (!userInteracted) {
                    clearInterval(timer);
                    document.querySelector('.redirect-notice').style.opacity = '0.5';
                }
            });
        });
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        // Performance monitoring
        window.addEventListener('load', () => {
            console.log('🛰️ Lamassu Labs Monitoring Dashboard Loaded');
            console.log('📊 Satellite: bvxuo-uaaaa-aaaal-asgua-cai');
            console.log('🌐 Network: ICP Mainnet');
            console.log('⚡ Status: Operational');
        });
    </script>
</body>
<<<<<<< HEAD
</html>"""


if __name__ == "__main__":
    asyncio.run(activate_monitoring_interface())
=======
</html>'''


if __name__ == "__main__":
    asyncio.run(activate_monitoring_interface())
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
