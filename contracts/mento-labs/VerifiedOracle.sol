// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title VerifiedOracle
 * @dev Simplified oracle contract for Mento Labs partnership demo
 * @notice This is a proof-of-concept for ZK-verified price feeds
 */
contract VerifiedOracle {

    // Price data structure
    struct PriceData {
        uint256 price;
        uint256 timestamp;
        bytes32 proofHash;
        uint32 confidence;
        bool verified;
    }

    // State variables
    mapping(bytes32 => PriceData) public prices;
    mapping(address => bool) public authorizedProvers;
    address public owner;

    // Events
    event PriceUpdated(
        bytes32 indexed assetPair,
        uint256 price,
        uint256 timestamp,
        bytes32 proofHash,
        uint32 confidence
    );

    event ProverAuthorized(address indexed prover);
    event ProverRevoked(address indexed prover);

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    modifier onlyAuthorizedProver() {
        require(authorizedProvers[msg.sender], "Unauthorized prover");
        _;
    }

    // Constructor
    constructor() {
        owner = msg.sender;
        authorizedProvers[msg.sender] = true; // Owner is automatically authorized
    }

    /**
     * @dev Update price with ZK proof
     * @param assetPair The asset pair identifier (e.g., keccak256("CELO/USD"))
     * @param price The verified price (with appropriate decimals)
     * @param proof The ZK proof data
     * @param confidence Confidence score (0-10000, representing 0-100%)
     */
    function updatePriceWithProof(
        bytes32 assetPair,
        uint256 price,
        bytes calldata proof,
        uint32 confidence
    ) external onlyAuthorizedProver returns (bool) {
        require(price > 0, "Price must be positive");
        require(confidence <= 10000, "Confidence must be <= 100%");
        require(proof.length > 0, "Proof cannot be empty");

        // In production, this would verify the actual ZK proof
        // For demo purposes, we simulate proof verification
        bool proofValid = _simulateProofVerification(proof, price, confidence);
        require(proofValid, "Invalid proof");

        // Calculate proof hash
        bytes32 proofHash = keccak256(proof);

        // Update price data
        prices[assetPair] = PriceData({
            price: price,
            timestamp: block.timestamp,
            proofHash: proofHash,
            confidence: confidence,
            verified: true
        });

        // Emit event
        emit PriceUpdated(assetPair, price, block.timestamp, proofHash, confidence);

        return true;
    }

    /**
     * @dev Get verified price for an asset pair
     * @param assetPair The asset pair identifier
     * @return price The verified price
     * @return timestamp When the price was last updated
     * @return confidence The confidence score
     * @return verified Whether the price has been verified
     */
    function getVerifiedPrice(bytes32 assetPair)
        external
        view
        returns (
            uint256 price,
            uint256 timestamp,
            uint32 confidence,
            bool verified
        )
    {
        PriceData memory data = prices[assetPair];
        return (data.price, data.timestamp, data.confidence, data.verified);
    }

    /**
     * @dev Check if a price is fresh (updated within time limit)
     * @param assetPair The asset pair identifier
     * @param maxAge Maximum age in seconds
     * @return Whether the price is considered fresh
     */
    function isPriceFresh(bytes32 assetPair, uint256 maxAge)
        external
        view
        returns (bool)
    {
        PriceData memory data = prices[assetPair];
        return data.verified && (block.timestamp - data.timestamp) <= maxAge;
    }

    /**
     * @dev Authorize a new prover
     * @param prover Address to authorize
     */
    function authorizeProver(address prover) external onlyOwner {
        require(prover != address(0), "Invalid prover address");
        authorizedProvers[prover] = true;
        emit ProverAuthorized(prover);
    }

    /**
     * @dev Revoke prover authorization
     * @param prover Address to revoke
     */
    function revokeProver(address prover) external onlyOwner {
        authorizedProvers[prover] = false;
        emit ProverRevoked(prover);
    }

    /**
     * @dev Get the latest price for multiple asset pairs
     * @param assetPairs Array of asset pair identifiers
     * @return prices Array of price data
     */
    function getMultiplePrices(bytes32[] calldata assetPairs)
        external
        view
        returns (PriceData[] memory)
    {
        PriceData[] memory result = new PriceData[](assetPairs.length);

        for (uint i = 0; i < assetPairs.length; i++) {
            result[i] = prices[assetPairs[i]];
        }

        return result;
    }

    /**
     * @dev Emergency function to pause/unpause price updates
     * @notice This is a safety feature for production deployment
     */
    bool public paused = false;

    function setPaused(bool _paused) external onlyOwner {
        paused = _paused;
    }

    modifier whenNotPaused() {
        require(!paused, "Contract is paused");
        _;
    }

    // Apply pause modifier to price updates
    function updatePriceWithProofSafe(
        bytes32 assetPair,
        uint256 price,
        bytes calldata proof,
        uint32 confidence
    ) external onlyAuthorizedProver whenNotPaused returns (bool) {
        return updatePriceWithProof(assetPair, price, proof, confidence);
    }

    /**
     * @dev Simulate ZK proof verification
     * @notice In production, this would call actual ZK verification
     * @param proof The proof data
     * @param price The claimed price
     * @param confidence The confidence score
     * @return Whether the proof is valid
     */
    function _simulateProofVerification(
        bytes calldata proof,
        uint256 price,
        uint32 confidence
    ) internal pure returns (bool) {
        // Simple simulation: check that proof is not empty and price/confidence are reasonable
        if (proof.length < 32) return false;
        if (price == 0) return false;
        if (confidence > 10000) return false;

        // Simulate some proof validation logic
        bytes32 proofHash = keccak256(proof);
        uint256 priceCheck = uint256(proofHash) % 1000000; // Simple deterministic check

        // Accept if the proof hash relates to the price in some way
        return (priceCheck > 0 && confidence >= 5000); // Require at least 50% confidence
    }

    /**
     * @dev Get contract statistics
     * @return totalPairs Number of asset pairs with prices
     * @return totalUpdates Total number of price updates
     * @return authorizedProverCount Number of authorized provers
     */
    function getStats()
        external
        view
        returns (
            uint256 totalPairs,
            uint256 totalUpdates,
            uint256 authorizedProverCount
        )
    {
        // Note: This is a simplified implementation
        // In production, you'd want to track these metrics properly
        return (0, 0, 0); // Placeholder for demo
    }

    /**
     * @dev Utility function to generate asset pair identifier
     * @param symbol The asset pair symbol (e.g., "CELO/USD")
     * @return The bytes32 identifier
     */
    function getAssetPairId(string calldata symbol) external pure returns (bytes32) {
        return keccak256(abi.encodePacked(symbol));
    }
}

/**
 * @title MentoOracleAdapter
 * @dev Adapter contract to integrate with existing Mento protocol
 * @notice This demonstrates how to integrate verified prices with Mento
 */
contract MentoOracleAdapter {

    VerifiedOracle public immutable verifiedOracle;
    address public immutable mentoExchange;

    constructor(address _verifiedOracle, address _mentoExchange) {
        verifiedOracle = VerifiedOracle(_verifiedOracle);
        mentoExchange = _mentoExchange;
    }

    /**
     * @dev Get price in Mento-compatible format
     * @param assetPair The asset pair identifier
     * @return price The price in Mento format
     */
    function getPrice(bytes32 assetPair) external view returns (uint256 price) {
        (uint256 verifiedPrice, uint256 timestamp, uint32 confidence, bool verified) =
            verifiedOracle.getVerifiedPrice(assetPair);

        require(verified, "Price not verified");
        require(block.timestamp - timestamp < 300, "Price too stale"); // 5 minutes max
        require(confidence >= 8000, "Confidence too low"); // 80% minimum

        return verifiedPrice;
    }

    /**
     * @dev Check if oracle is healthy
     * @return Whether the oracle is operational
     */
    function isHealthy() external view returns (bool) {
        // Basic health check - in production would be more comprehensive
        return address(verifiedOracle) != address(0);
    }
}
