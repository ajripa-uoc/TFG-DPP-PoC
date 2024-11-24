module.exports = {
  networks: {
    development: {
      url: process.env.NETWORK_URL || "http://127.0.0.1:8545", // Docker compose service name
      network_id: "*" // Match any network id
    },
    live: {
      url: process.env.NETWORK_URL,
      network_id: "*"
    },
    develop: {
      port: 7545
    }
  },
};