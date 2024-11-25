# Digital Product Passport (DPP) Proof of Concept

## **Overview**

This repository contains a **Proof of Concept (PoC)** for managing **Digital Product Passports (DPP)** using **smart contracts** on the Ethereum blockchain. DPPs are digital representations that contain crucial information about a product, enabling its traceability and verification of authenticity throughout its lifecycle.

The core functionality includes:
- **Storing static information** about products (e.g., name, type).
- **Managing events** such as modifications or merging with other products.
- Leveraging blockchain technology to ensure **immutability**, **transparency**, and **security** of data.

## **Features**

- **Smart Contracts**: Written in Solidity to manage DPPs and associated events.
- **Blockchain Simulation**: Includes a local blockchain environment using Ganache for development and testing.
- **API Integration**: A Flask-based REST API that interacts with smart contracts for creating, updating, and querying DPPs.
- **Testing Suite**: Comprehensive tests using Truffle to validate the functionality of smart contracts.
- **Docker Support**: Includes Docker Compose for setting up the development environment seamlessly.

## **Technologies Used**

- **Ethereum Blockchain**: Secure and decentralized storage of DPP data.
- **Truffle**: Framework for developing, testing, and deploying smart contracts.
- **Ganache**: Local blockchain environment for development.
- **Flask**: Backend framework for building the REST API.
- **Docker Compose**: Simplified setup and deployment of the development environment.

### **Set Up the Environment with Docker Compose**

This project leverages `docker-compose` to simplify the setup process. Using `docker-compose`, all required services (e.g., Ganache and the Flask API) are automatically configured and started with a single command.

#### **Steps to Set Up the Environment**

1. **Clone the Repository**
   Begin by cloning the repository to your local machine:
   ```bash
   git clone https://github.com/ajripa-uoc/TFG-DPP-PoC.git
   cd TFG-DPP-PoC
   ```
2. **Start the Services**
   Run the following command to start all services defined in `docker-compose.yml`:
   ```bash
   docker-compose up
   ```
   This command will:
   - Start **Ganache** to simulate a local Ethereum blockchain.
   - Deploy the **Flask API**, making it accessible on `http://localhost`.
   - Automatically handle networking between the services.

3. **Verify the Setup**
   Once the containers are running, you can verify:
   - **Ganache** is available at `http://localhost:8545`.
   - **Flask API** is accessible at `http://localhost`.

   Check the logs for any errors or to confirm that the services are running correctly:
   ```bash
   docker-compose logs
   ```
4. **Stop the Services**
   To stop the running services, use:
   ```bash
   docker-compose down
   ```
   This will gracefully stop and remove all containers.

#### **Key Advantages of Docker Compose**
- **One Command Setup**: No need to manually install or configure dependencies.
- **Consistency**: Guarantees the same environment across all development machines.
- **Reproducibility**: Easily replicate the setup for testing or production environments.