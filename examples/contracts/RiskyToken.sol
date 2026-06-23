// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract RiskyToken {
    string public name = "Risky Token";
    string public symbol = "RISK";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    address public owner;
    uint256 public tax;
    bool public paused;
    mapping(address => bool) public blacklist;
    mapping(address => uint256) public balanceOf;

    modifier onlyOwner() {
        require(msg.sender == owner, "only owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function mint(address to, uint256 amount) external onlyOwner {
        totalSupply += amount;
        balanceOf[to] += amount;
    }

    function burn(address from, uint256 amount) external onlyOwner {
        balanceOf[from] -= amount;
        totalSupply -= amount;
    }

    function pause() external onlyOwner {
        paused = true;
    }

    function unpause() external onlyOwner {
        paused = false;
    }

    function setBlacklist(address user, bool value) external onlyOwner {
        blacklist[user] = value;
    }

    function setTax(uint256 newTax) external onlyOwner {
        tax = newTax;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        require(!paused, "paused");
        require(!blacklist[msg.sender] && !blacklist[to], "blacklisted");
        uint256 fee = amount * tax / 10000;
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount - fee;
        balanceOf[owner] += fee;
        return true;
    }

    function rescueTokens(address token, address to, uint256 amount) external onlyOwner {
        (bool ok,) = token.call(abi.encodeWithSignature("transfer(address,uint256)", to, amount));
        require(ok, "rescue failed");
    }

    function emergencyWithdraw() external onlyOwner {
        payable(owner).transfer(address(this).balance);
    }

    function destroy() external onlyOwner {
        selfdestruct(payable(owner));
    }
}
