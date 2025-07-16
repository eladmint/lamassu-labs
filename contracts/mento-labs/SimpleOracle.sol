// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title SimpleOracle
 * @dev A simple oracle contract for Mento Labs partnership demo
 */
contract SimpleOracle {

    address public owner;

    struct PriceData {
        uint256 price;
        uint256 timestamp;
    }

    mapping(bytes32 => PriceData) public prices;

    event PriceUpdated(
        bytes32 indexed assetPair,
        uint256 price,
        uint256 timestamp
    );

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }

    function updatePrice(
        bytes32 assetPair,
        uint256 price,
        uint256 timestamp
    ) external onlyOwner {
        require(price > 0, "Price must be positive");
        require(timestamp > 0, "Invalid timestamp");

        prices[assetPair] = PriceData({
            price: price,
            timestamp: timestamp
        });

        emit PriceUpdated(assetPair, price, timestamp);
    }

    function getPrice(bytes32 assetPair) external view returns (uint256 price, uint256 timestamp) {
        PriceData memory data = prices[assetPair];
        return (data.price, data.timestamp);
    }

    function getPairId(string calldata symbol) external pure returns (bytes32) {
        return keccak256(abi.encodePacked(symbol));
    }
}
