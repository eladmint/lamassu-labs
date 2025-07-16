import Text "mo:base/Text";
import Result "mo:base/Result";
import HashMap "mo:base/HashMap";
import Time "mo:base/Time";
import Int "mo:base/Int";
import Principal "mo:base/Principal";
import Blob "mo:base/Blob";
import Array "mo:base/Array";
import Nat8 "mo:base/Nat8";
import Iter "mo:base/Iter";
import Random "mo:base/Random";
import Http "mo:base/Http";

actor OAuthHandler {
    // Types
    public type User = {
        id: Text;
        email: Text;
        name: Text;
        picture: Text;
        verified_email: Bool;
    };

    public type AuthResult = {
        success: Bool;
        user: ?User;
        sessionToken: ?Text;
        error: ?Text;
    };

    public type TokenResponse = {
        access_token: Text;
        token_type: Text;
        expires_in: Nat;
        refresh_token: ?Text;
        scope: Text;
    };

    // Private state
    private stable var CLIENT_ID = "867263134607-vkkd9avs6a75gmjpzja17a9a0bbdle1.apps.googleusercontent.com";
    private stable var CLIENT_SECRET = ""; // Set this via secure method
    private stable var allowedOrigins = [
        "https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io",
        "http://localhost:3000"
    ];

    // Session storage
    private var sessions = HashMap.HashMap<Text, (User, Time.Time)>(10, Text.equal, Text.hash);

    // Admin principal for setting secrets
    private stable var admin : ?Principal = null;

    // Initialize admin
    public shared(msg) func initAdmin() : async Result.Result<Text, Text> {
        switch (admin) {
            case (?existingAdmin) {
                #err("Admin already initialized")
            };
            case null {
                admin := ?msg.caller;
                #ok("Admin initialized: " # Principal.toText(msg.caller))
            };
        };
    };

    // Set client secret (admin only)
    public shared(msg) func setClientSecret(secret: Text) : async Result.Result<Text, Text> {
        switch (admin) {
            case (?adminPrincipal) {
                if (msg.caller == adminPrincipal) {
                    CLIENT_SECRET := secret;
                    #ok("Client secret updated")
                } else {
                    #err("Unauthorized: Only admin can set client secret")
                };
            };
            case null {
                #err("Admin not initialized")
            };
        };
    };

    // Exchange Google auth code for user data
    public func exchangeGoogleAuthCode(authCode: Text, redirectUri: Text) : async AuthResult {
        try {
            // Validate redirect URI
            if (not isValidRedirectUri(redirectUri)) {
                return {
                    success = false;
                    user = null;
                    sessionToken = null;
                    error = ?"Invalid redirect URI";
                };
            };

            // Exchange code for tokens
            let tokenResult = await exchangeCodeForTokens(authCode, redirectUri);

            switch (tokenResult) {
                case (#ok(tokens)) {
                    // Get user info
                    let userResult = await getUserInfo(tokens.access_token);

                    switch (userResult) {
                        case (#ok(user)) {
                            // Generate session token
                            let sessionToken = await generateSessionToken(user.id);

                            // Store session
                            sessions.put(sessionToken, (user, Time.now()));

                            return {
                                success = true;
                                user = ?user;
                                sessionToken = ?sessionToken;
                                error = null;
                            };
                        };
                        case (#err(error)) {
                            return {
                                success = false;
                                user = null;
                                sessionToken = null;
                                error = ?error;
                            };
                        };
                    };
                };
                case (#err(error)) {
                    return {
                        success = false;
                        user = null;
                        sessionToken = null;
                        error = ?error;
                    };
                };
            };
        } catch (e) {
            return {
                success = false;
                user = null;
                sessionToken = null;
                error = ?"Internal error during authentication";
            };
        };
    };

    // Validate session token
    public query func validateSession(sessionToken: Text) : async ?User {
        switch (sessions.get(sessionToken)) {
            case (?(user, timestamp)) {
                // Check if session is still valid (24 hours)
                let now = Time.now();
                let dayInNanos = 24 * 60 * 60 * 1_000_000_000;

                if (now - timestamp < dayInNanos) {
                    ?user
                } else {
                    // Session expired
                    null
                };
            };
            case null {
                null
            };
        };
    };

    // Private helper functions
    private func isValidRedirectUri(uri: Text) : Bool {
        for (origin in allowedOrigins.vals()) {
            if (Text.startsWith(uri, #text origin)) {
                return true;
            };
        };
        false
    };

    private func exchangeCodeForTokens(code: Text, redirectUri: Text) : async Result.Result<TokenResponse, Text> {
        // In Motoko, making HTTP requests requires using the IC's HTTP outcalls feature
        // This is a simplified version - in production, use proper HTTP outcalls

        // For now, return an error indicating this needs to be implemented
        // with IC's HTTP outcalls feature
        #err("HTTP outcalls not implemented - deploy as a separate service")
    };

    private func getUserInfo(accessToken: Text) : async Result.Result<User, Text> {
        // Similar to above - requires HTTP outcalls
        #err("HTTP outcalls not implemented - deploy as a separate service")
    };

    private func generateSessionToken(userId: Text) : async Text {
        let entropy = await Random.blob();
        let timestamp = Int.toText(Time.now());
        let combined = userId # "-" # timestamp # "-" # Blob.toText(entropy);
        combined
    };

    // Clean up expired sessions periodically
    public func cleanupSessions() : async Nat {
        let now = Time.now();
        let dayInNanos = 24 * 60 * 60 * 1_000_000_000;
        var removed = 0;

        for ((token, (user, timestamp)) in sessions.entries()) {
            if (now - timestamp >= dayInNanos) {
                sessions.delete(token);
                removed += 1;
            };
        };

        removed
    };
};
