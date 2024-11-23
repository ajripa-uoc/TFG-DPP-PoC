var Dpp = artifacts.require("DigitalProductPassport");

module.exports = function(deployer) {
  deployer.deploy(Dpp)
  .then(() => {
    // Write contract number to .env file
    const fs = require('fs');
    const contractAddress = Dpp.address;
    fs.writeFileSync(
      '.env',
      `CONTRACT_ADDRESS=${contractAddress}\n`,
      // Remove the flag option to overwrite
    );
    console.log(`Contract address ${contractAddress} saved to .env`);
  });
};