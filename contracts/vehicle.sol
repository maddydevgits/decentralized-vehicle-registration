// SPDX-License-Identifier: MIT
pragma experimental ABIEncoderV2;
pragma solidity >=0.4.22 <0.9.0;

contract vehicle {

  address[] vOwners;
  string[] vTypes;
  string[] vNumbers;
  string[] vEmails;
  string[] vAddresses;
  string[] vChassisnos;
  string[] vOwnernames;

  mapping(string=>bool) regList;

  address admin;
  constructor() public{
    admin=msg.sender;
  }

  modifier onlyAdmin() {
    require(msg.sender==admin);
    _;
  }

  function addVehicle(address _vowner, string memory _vtype, string memory _vnumber, string memory _vemail, string memory _vaddress, string memory _vchassis, string memory _vownername) public onlyAdmin {

    require(!regList[_vnumber]);

    vOwners.push(_vowner);
    vTypes.push(_vtype);
    vNumbers.push(_vnumber);
    vEmails.push(_vemail);
    vAddresses.push(_vaddress);
    vChassisnos.push(_vchassis);
    vOwnernames.push(_vownername);
  }

  function viewVehicles() public view onlyAdmin returns (address[] memory, string[] memory, string[] memory, string[] memory, string[] memory, string[] memory, string[] memory) {

    return(vOwners,vTypes,vNumbers,vEmails,vAddresses,vChassisnos,vOwnernames);
  }
}
