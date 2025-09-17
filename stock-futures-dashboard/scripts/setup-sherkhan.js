const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log('🔐 Sherkhan API Setup');
console.log('====================');
console.log('');

// Function to update .env.local file
function updateEnvFile(apiKey, secretKey) {
  const envPath = path.join(process.cwd(), '.env.local');
  let envContent = '';

  // Read existing .env.local if it exists
  if (fs.existsSync(envPath)) {
    envContent = fs.readFileSync(envPath, 'utf8');
  }

  // Update or add Sherkhan API credentials
  const updates = {
    'SHERKHAN_API_KEY': apiKey,
    'SHERKHAN_SECRET_KEY': secretKey,
    'SHERKHAN_API_BASE': 'https://api.sherkhan.com',
    'SHERKHAN_WEBSOCKET_URL': 'wss://api.sherkhan.com/ws'
  };

  Object.entries(updates).forEach(([key, value]) => {
    const regex = new RegExp(`^${key}=.*$`, 'm');
    if (envContent.match(regex)) {
      envContent = envContent.replace(regex, `${key}=${value}`);
    } else {
      envContent += `${key}=${value}\n`;
    }
  });

  fs.writeFileSync(envPath, envContent);
  console.log('✅ Credentials saved to .env.local');
}

// Function to test API connection
async function testConnection() {
  try {
    console.log('\n🧪 Testing API connection...');
    
    const response = await fetch('http://localhost:3000/api/market/live', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ action: 'test-connection' })
    });

    const result = await response.json();
    
    if (response.ok) {
      console.log('✅ API connection successful!');
      console.log('Account info:', result.account);
    } else {
      console.log('❌ API connection failed:', result.error);
    }
  } catch (error) {
    console.log('❌ Connection test failed. Make sure your Next.js dev server is running.');
    console.log('Run: npm run dev');
  }
}

// Main setup flow
async function setup() {
  console.log('Please enter your Sherkhan API credentials:');
  console.log('(You can find these in your Sherkhan developer dashboard)');
  console.log('');

  rl.question('API Key: ', (apiKey) => {
    rl.question('Secret Key: ', (secretKey) => {
      if (!apiKey || !secretKey) {
        console.log('❌ Both API Key and Secret Key are required!');
        rl.close();
        return;
      }

      updateEnvFile(apiKey, secretKey);
      
      console.log('');
      console.log('🎉 Setup complete!');
      console.log('');
      console.log('Next steps:');
      console.log('1. Start your development server: npm run dev');
      console.log('2. Visit http://localhost:3000/api/market/live to test the API');
      console.log('3. Update your dashboard to use the /api/market/live endpoint');
      console.log('');
      console.log('Your dashboard will now show real Indian stock market data!');
      
      rl.close();
    });
  });
}

// Add to .gitignore if not already there
function updateGitignore() {
  const gitignorePath = path.join(process.cwd(), '.gitignore');
  let gitignoreContent = '';

  if (fs.existsSync(gitignorePath)) {
    gitignoreContent = fs.readFileSync(gitignorePath, 'utf8');
  }

  if (!gitignoreContent.includes('.env.local')) {
    gitignoreContent += '\n# Environment variables\n.env.local\n.env\n';
    fs.writeFileSync(gitignorePath, gitignoreContent);
    console.log('✅ Added .env.local to .gitignore');
  }
}

// Run setup
updateGitignore();
setup();
