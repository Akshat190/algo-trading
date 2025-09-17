import { NextRequest, NextResponse } from 'next/server'
import { getOAuthConfig, getCookie, setCookie, clearCookie } from '../../../../lib/sharekhan-oauth'
import axios from 'axios'

// Handles the OAuth callback from Sharekhan
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const code = searchParams.get('code')
  const state = searchParams.get('state')
  const error = searchParams.get('error')

  // Check for OAuth error
  if (error) {
    console.error('OAuth error:', error)
    return NextResponse.json({ error: `OAuth error: ${error}` }, { status: 400 })
  }

  // Verify state to prevent CSRF
  const savedState = getCookie('sk_oauth_state')
  clearCookie('sk_oauth_state')
  
  if (!state || state !== savedState) {
    return NextResponse.json({ error: 'Invalid state parameter' }, { status: 400 })
  }

  if (!code) {
    return NextResponse.json({ error: 'No authorization code received' }, { status: 400 })
  }

  const { clientId, clientSecret, redirectUri, tokenUrl } = getOAuthConfig()

  try {
    // Exchange authorization code for access token
    const tokenResponse = await axios.post(tokenUrl, {
      grant_type: 'authorization_code',
      client_id: clientId,
      client_secret: clientSecret,
      redirect_uri: redirectUri,
      code
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      timeout: 10000
    })

    const { access_token, refresh_token, expires_in } = tokenResponse.data

    if (!access_token) {
      return NextResponse.json({ error: 'No access token received' }, { status: 400 })
    }

    // Store tokens in secure cookies
    const expiresInSeconds = expires_in || 3600
    setCookie('sk_access_token', access_token, expiresInSeconds)
    
    if (refresh_token) {
      setCookie('sk_refresh_token', refresh_token, expiresInSeconds * 2)
    }

    // Redirect to your dashboard
    return NextResponse.redirect('http://127.0.0.1:3000/?login=success')

  } catch (error: any) {
    console.error('Token exchange failed:', error.response?.data || error.message)
    return NextResponse.json({ 
      error: 'Token exchange failed',
      details: error.response?.data || error.message
    }, { status: 500 })
  }
}
