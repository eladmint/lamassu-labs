/**
 * Secure OAuth API Handler - CommonJS Version
 * Deploy this as an Express.js endpoint on Hivelocity VPS
 */

const fetch = require('node-fetch');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');

// Environment variables (set these in your deployment environment)
const CLIENT_ID = process.env.GOOGLE_CLIENT_ID || process.env.GOOGLE_OAUTH_CLIENT_ID || '867263134607-vkkd9avs6a75gmjpzja17a9a0bbdle1.apps.googleusercontent.com';
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET || process.env.GOOGLE_OAUTH_CLIENT_SECRET;
const JWT_SECRET = process.env.JWT_SECRET || crypto.randomBytes(32).toString('hex');
const ALLOWED_ORIGINS = (process.env.ALLOWED_ORIGINS || 'https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io').split(',');

// CORS headers
const corsHeaders = {
    'Access-Control-Allow-Origin': '*', // Will be set dynamically based on origin
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
};

/**
 * Main handler function
 */
async function handler(req, res) {
    // Set CORS headers based on request origin
    const origin = req.headers.origin;
    if (ALLOWED_ORIGINS.includes(origin)) {
        res.setHeader('Access-Control-Allow-Origin', origin);
    }

    // Handle preflight
    if (req.method === 'OPTIONS') {
        Object.entries(corsHeaders).forEach(([key, value]) => {
            res.setHeader(key, value);
        });
        return res.status(200).end();
    }

    // Only accept POST
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { code, redirectUri } = req.body;

        // Validate inputs
        if (!code || !redirectUri) {
            return res.status(400).json({ error: 'Missing required parameters' });
        }

        // Validate redirect URI
        const url = new URL(redirectUri);
        if (!ALLOWED_ORIGINS.includes(url.origin)) {
            return res.status(400).json({ error: 'Invalid redirect URI' });
        }

        // Exchange code for tokens
        const tokenResponse = await fetch('https://oauth2.googleapis.com/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                client_id: CLIENT_ID,
                client_secret: CLIENT_SECRET,
                code: code,
                grant_type: 'authorization_code',
                redirect_uri: redirectUri
            })
        });

        if (!tokenResponse.ok) {
            const error = await tokenResponse.json();
            console.error('Token exchange failed:', error);
            return res.status(400).json({
                error: 'Authentication failed',
                details: error.error_description
            });
        }

        const tokens = await tokenResponse.json();

        // Get user info
        const userResponse = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
            headers: {
                'Authorization': `Bearer ${tokens.access_token}`
            }
        });

        if (!userResponse.ok) {
            return res.status(400).json({ error: 'Failed to get user info' });
        }

        const userInfo = await userResponse.json();

        // Create secure session token (JWT)
        const sessionToken = jwt.sign(
            {
                id: userInfo.id,
                email: userInfo.email,
                provider: 'google'
            },
            JWT_SECRET,
            {
                expiresIn: '7d',
                issuer: 'mento-monitor'
            }
        );

        // Return user data and session token
        return res.status(200).json({
            success: true,
            user: {
                id: userInfo.id,
                email: userInfo.email,
                name: userInfo.name,
                picture: userInfo.picture,
                verified_email: userInfo.verified_email
            },
            sessionToken
        });

    } catch (error) {
        console.error('OAuth handler error:', error);
        return res.status(500).json({
            error: 'Internal server error',
            message: error.message
        });
    }
}

/**
 * Express.js implementation
 */
function createExpressHandler() {
    const express = require('express');
    const router = express.Router();

    // Middleware to handle CORS
    router.use((req, res, next) => {
        const origin = req.headers.origin;
        if (ALLOWED_ORIGINS.includes(origin)) {
            res.setHeader('Access-Control-Allow-Origin', origin);
        }
        Object.entries(corsHeaders).forEach(([key, value]) => {
            res.setHeader(key, value);
        });
        next();
    });

    // Token exchange endpoint
    router.post('/oauth/google/exchange', async (req, res) => {
        return handler(req, res);
    });

    // Session validation endpoint
    router.post('/oauth/validate', async (req, res) => {
        try {
            const { sessionToken } = req.body;

            if (!sessionToken) {
                return res.status(400).json({ error: 'No session token provided' });
            }

            const decoded = jwt.verify(sessionToken, JWT_SECRET, {
                issuer: 'mento-monitor'
            });

            return res.status(200).json({
                valid: true,
                user: {
                    id: decoded.id,
                    email: decoded.email,
                    provider: decoded.provider
                }
            });

        } catch (error) {
            if (error.name === 'TokenExpiredError') {
                return res.status(401).json({ error: 'Session expired' });
            }
            return res.status(401).json({ error: 'Invalid session' });
        }
    });

    return router;
}

module.exports = {
    handler,
    createExpressHandler
};
