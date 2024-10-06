// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

contract DataStorageWithNames {
    address public owner;
    mapping(string => string) public ipfsHashToFileName;
    mapping(address => bool) public authorizedAddresses;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    modifier onlyAuthorized() {
        require(msg.sender == owner || authorizedAddresses[msg.sender], "Not authorized");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function addIPFSHash(string memory _ipfsHash, string memory _fileName) public onlyOwner {
        ipfsHashToFileName[_ipfsHash] = _fileName;
    }

    function getFileName(string memory _ipfsHash) public view onlyAuthorized returns (string memory) {
        require(bytes(ipfsHashToFileName[_ipfsHash]).length > 0, "Hash not found");
        return ipfsHashToFileName[_ipfsHash];
    }

    function authorizeAddress(address _address) public onlyOwner {
        authorizedAddresses[_address] = true;
    }

    function revokeAuthorization(address _address) public onlyOwner {
        require(_address != owner, "Owner cannot revoke their own authorization");
        authorizedAddresses[_address] = false;
    }

    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Invalid address");
        owner = newOwner;
    }

    function getAuthorizedAddresses(address _address) public view returns (bool) {
        return authorizedAddresses[_address];
    }
}