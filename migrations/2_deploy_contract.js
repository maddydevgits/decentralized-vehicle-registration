const Migrations = artifacts.require("vehicle");

module.exports = function (deployer) {
  deployer.deploy(Migrations);
};
