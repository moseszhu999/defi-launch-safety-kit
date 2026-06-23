// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SafeToken {
    string public name = "Safe Token";
    string public symbol = "SAFE";
    uint8 public decimals = 18;
    uint256 public immutable totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 supply) {
        totalSupply = supply;
        balanceOf[msg.sender] = supply;
        emit Transfer(address(0), msg.sender, supply);
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        require(to != address(0), "zero address");
        require(balanceOf[msg.sender] >= amount, "insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }
}
