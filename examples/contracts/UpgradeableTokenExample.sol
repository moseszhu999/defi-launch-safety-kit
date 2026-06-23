// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract UpgradeableTokenExample {
    address public owner;
    address public implementation;
    bool public initialized;
    mapping(address => uint256) public balanceOf;

    modifier onlyOwner() {
        require(msg.sender == owner, "only owner");
        _;
    }

    function initialize(address initialOwner) external {
        require(!initialized, "already initialized");
        owner = initialOwner;
        initialized = true;
    }

    function upgradeTo(address newImplementation) external onlyOwner {
        implementation = newImplementation;
    }

    function _authorizeUpgrade(address newImplementation) internal view onlyOwner {
        newImplementation;
    }

    function delegate(bytes calldata data) external onlyOwner returns (bytes memory) {
        (bool ok, bytes memory result) = implementation.delegatecall(data);
        require(ok, "delegatecall failed");
        return result;
    }
}
