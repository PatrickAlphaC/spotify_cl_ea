pragma solidity >= 0.4.20;

import "https://github.com/smartcontractkit/chainlink/evm-contracts/src/v0.4/ChainlinkClient.sol";
import "https://github.com/smartcontractkit/chainlink/evm-contracts/src/v0.4/vendor/Ownable.sol";

contract Test is ChainlinkClient, Ownable {
  // This is the LINK payment, currently set to 1 LINK
  // Get free testnet LINK here: https://ropsten.chain.link/
  // Get free testnet ETH here: https://faucet.ropsten.be/
  uint256 constant private ORACLE_PAYMENT = 1 * LINK;
  uint256 public popularity;
  
  // The addresses of the Alpha Vantage Ropsten node
  address ALPHA_VANTAGE_ADDRESS_ROPSTEN = 0xB36d3709e22F7c708348E225b20b13eA546E6D9c;

  // The address of the jobs for ropsten(testnet).
  // These return an unsigned int
  string constant private UINT_TICKER_JOB_ROPSTEN = "903c5a53e95141218e2784a6142f53a5";
 // Once the data comes back, we allow the user to access the data with this function
  // The main funciton that happens when you request data
  // onlyOwner means only the owner of the ETH wallet can call this function
    function requestPopularity(string _artist) public onlyOwner
  {
    // We initialize the request, and begin building it
    Chainlink.Request memory req = buildChainlinkRequest(stringToBytes32(UINT_TICKER_JOB_ROPSTEN), this, this.fulfillPopularity.selector);
    // We add the parameters from the API
    req.add("artist", _artist);
    // This is the location in the JSON return to get
    string[] memory copyPath = new string[](1);
    copyPath[0] = "popularity";
    req.addStringArray("copyPath", copyPath);
    // Then we make the request
    sendChainlinkRequestTo(ALPHA_VANTAGE_ADDRESS_ROPSTEN, req, ORACLE_PAYMENT);
  }

      function fulfillPopularity(bytes32 _requestId, uint256 _popularity)
    public
    recordChainlinkFulfillment(_requestId)
  {
    emit RequestPopularityFullfilled(_requestId, _popularity);
    popularity = _popularity;
  }
  // Understands when the API call is completed
  event RequestPopularityFullfilled(
    bytes32 indexed requestId,
    uint256 indexed popularity
  );



// Needed functions to make the above work
  function getChainlinkToken() public view returns (address) {
    return chainlinkTokenAddress();
  }

  function withdrawLink() public onlyOwner {
    LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
    require(link.transfer(msg.sender, link.balanceOf(address(this))), "Unable to transfer");
  }

  constructor() public Ownable() {
    setPublicChainlinkToken();
  }
  
  function stringToBytes32(string memory source) private pure returns (bytes32 result) {
    bytes memory tempEmptyStringTest = bytes(source);
    if (tempEmptyStringTest.length == 0) {
      return 0x0;
    }
    assembly { // solhint-disable-line no-inline-assembly
      result := mload(add(source, 32))
    }
  }
}
