#!/usr/bin/env python3
"""
Flask Web Application for Near Future Data - TradeTiger Style
"""

from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
from token_manager import WebsiteNearFuture
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize the Near Future system
near_future_system = WebsiteNearFuture()

# HTML Template for the website
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Near Future - TradeTiger Style</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .status-bar {
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .status-item {
            margin: 5px 0;
        }
        .status-valid { color: #28a745; }
        .status-expired { color: #dc3545; }
        .status-no_token { color: #6c757d; }
        
        .controls {
            padding: 15px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            text-align: center;
        }
        .btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 5px;
            font-size: 14px;
        }
        .btn:hover { background: #0056b3; }
        .btn-success { background: #28a745; }
        .btn-success:hover { background: #1e7e34; }
        
        .data-container {
            padding: 20px;
            overflow-x: auto;
        }
        .contracts-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        .contracts-table th {
            background: #343a40;
            color: white;
            padding: 12px 8px;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
        }
        .contracts-table td {
            padding: 8px;
            border-bottom: 1px solid #e9ecef;
        }
        .contracts-table tr:hover {
            background: #f8f9fa;
        }
        .symbol { font-weight: bold; color: #2c3e50; }
        .expiry { color: #dc3545; font-weight: 500; }
        .days-near { color: #dc3545; font-weight: bold; }
        .days-far { color: #6c757d; }
        
        .loading {
            text-align: center;
            padding: 40px;
            font-size: 18px;
            color: #6c757d;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin: 20px;
        }
        .success {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin: 20px;
        }
        
        @media (max-width: 768px) {
            body { padding: 10px; }
            .status-bar { flex-direction: column; text-align: center; }
            .contracts-table { font-size: 11px; }
            .contracts-table th, .contracts-table td { padding: 6px 4px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 Near Future - Stock Futures</h1>
            <p>Real-time near expiry futures contracts • TradeTiger Style</p>
        </div>
        
        <div class="status-bar">
            <div>
                <span class="status-item"><strong>Status:</strong> 
                    <span id="token-status" class="status-no_token">Loading...</span>
                </span>
                <span class="status-item"><strong>Last Updated:</strong> 
                    <span id="last-updated">Never</span>
                </span>
            </div>
            <div>
                <span class="status-item"><strong>Contracts:</strong> 
                    <span id="contract-count">0</span>
                </span>
                <span class="status-item"><strong>Token Expires:</strong> 
                    <span id="token-expiry">Unknown</span>
                </span>
            </div>
        </div>
        
        <div class="controls">
            <button class="btn btn-success" onclick="loadData()">🔄 Refresh Data</button>
            <button class="btn" onclick="checkTokenStatus()">🔑 Check Token</button>
            <button class="btn" onclick="toggleAutoRefresh()">⏱️ Auto Refresh</button>
        </div>
        
        <div class="data-container">
            <div id="loading" class="loading">Click "Refresh Data" to load near future contracts...</div>
            <div id="error-message" class="error" style="display:none;"></div>
            <div id="success-message" class="success" style="display:none;"></div>
            
            <table class="contracts-table" id="contracts-table" style="display:none;">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Symbol</th>
                        <th>Expiry Date</th>
                        <th>Days to Expiry</th>
                        <th>Lot Size</th>
                        <th>Scrip Code</th>
                    </tr>
                </thead>
                <tbody id="contracts-body">
                </tbody>
            </table>
        </div>
    </div>

    <script>
        let autoRefreshInterval = null;
        
        async function loadData() {
            const loading = document.getElementById('loading');
            const errorMessage = document.getElementById('error-message');
            const successMessage = document.getElementById('success-message');
            const table = document.getElementById('contracts-table');
            
            loading.style.display = 'block';
            loading.textContent = 'Loading near future data...';
            errorMessage.style.display = 'none';
            successMessage.style.display = 'none';
            table.style.display = 'none';
            
            try {
                const response = await fetch('/api/near-future');
                const result = await response.json();
                
                loading.style.display = 'none';
                
                if (result.success) {
                    displayData(result.data);
                    updateStatus(result.token_info, result.count);
                    successMessage.textContent = `✅ Loaded ${result.count} near future contracts`;
                    successMessage.style.display = 'block';
                    setTimeout(() => successMessage.style.display = 'none', 3000);
                } else {
                    showError(result.error);
                }
            } catch (error) {
                loading.style.display = 'none';
                showError('Failed to fetch data: ' + error.message);
            }
        }
        
        async function checkTokenStatus() {
            try {
                const response = await fetch('/api/token-status');
                const result = await response.json();
                updateStatus(result);
                
                const message = `Token Status: ${result.status}\\nExpires: ${result.expires_at || 'Unknown'}\\nTime Remaining: ${result.time_remaining || 0} minutes`;
                alert(message);
            } catch (error) {
                alert('Failed to check token status: ' + error.message);
            }
        }
        
        function displayData(contracts) {
            const tbody = document.getElementById('contracts-body');
            const table = document.getElementById('contracts-table');
            
            tbody.innerHTML = '';
            
            contracts.forEach((contract, index) => {
                const row = tbody.insertRow();
                const daysClass = contract.days_to_expiry <= 15 ? 'days-near' : 'days-far';
                
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td class="symbol">${contract.symbol}</td>
                    <td class="expiry">${contract.expiry}</td>
                    <td class="${daysClass}">${contract.days_to_expiry} days</td>
                    <td>${contract.lot_size.toLocaleString()}</td>
                    <td>${contract.scrip_code}</td>
                `;
            });
            
            table.style.display = 'table';
        }
        
        function updateStatus(tokenInfo, contractCount = null) {
            document.getElementById('token-status').textContent = tokenInfo.status;
            document.getElementById('token-status').className = 'status-' + tokenInfo.status;
            document.getElementById('token-expiry').textContent = tokenInfo.expires_at || 'Unknown';
            document.getElementById('last-updated').textContent = new Date().toLocaleString();
            
            if (contractCount !== null) {
                document.getElementById('contract-count').textContent = contractCount;
            }
        }
        
        function showError(message) {
            const errorMessage = document.getElementById('error-message');
            errorMessage.textContent = '❌ ' + message;
            errorMessage.style.display = 'block';
        }
        
        function toggleAutoRefresh() {
            if (autoRefreshInterval) {
                clearInterval(autoRefreshInterval);
                autoRefreshInterval = null;
                alert('Auto-refresh disabled');
            } else {
                autoRefreshInterval = setInterval(loadData, 60000); // Every minute
                alert('Auto-refresh enabled (every 60 seconds)');
                loadData(); // Load immediately
            }
        }
        
        // Load token status on page load
        window.onload = function() {
            checkTokenStatus();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/near-future')
def api_near_future():
    """API endpoint to get near future data"""
    try:
        result = near_future_system.get_near_future_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/token-status')
def api_token_status():
    """API endpoint to get token status"""
    try:
        token_info = near_future_system.get_token_status()
        return jsonify(token_info)
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        })

@app.route('/api/refresh-token', methods=['POST'])
def api_refresh_token():
    """API endpoint to manually refresh token"""
    try:
        success = near_future_system.token_manager.refresh_token_automatically()
        if success:
            # Re-initialize the connection with new token
            near_future_system.near_future_fetcher = None
            return jsonify({
                "success": True,
                "message": "Token refreshed successfully"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to refresh token"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    print("🚀 Starting Near Future Website...")
    print("🔗 Open your browser and go to: http://localhost:5000")
    print("📊 The website will automatically manage tokens for you!")
    print("⏰ Tokens will be refreshed automatically when they expire")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
