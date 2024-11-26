#!/bin/bash

# Base URL
BASE_URL="https://dpp-poc.ajripa.click/api"

# Test health check
echo "Testing health check..."
curl -s -X GET "${BASE_URL}/dpp/healthz"
echo -e "\n"

# Create a new DPP
echo "Creating new DPP..."
DPP_RESPONSE=$(curl -s -X POST "${BASE_URL}/dpp" \
  -H "Content-Type: application/json" \
  -d '{
    "companyName": "Apple",
    "productType": "iPhone",
    "productDetail": "iPhone 12 Pro",
    "manufactureDate": "2021-01-01"
  }')
echo $DPP_RESPONSE
echo -e "\n"

# Extract DPP ID from response (assuming it's in JSON format)
DPP_ID=$(echo $DPP_RESPONSE | jq -r '.dppId')

# Update the DPP
echo "Updating DPP..."
curl -s -X PUT "${BASE_URL}/dpp/${DPP_ID}" \
  -H "Content-Type: application/json" \
  -d '{
    "companyName": "Apple",
    "productType": "iPhone",
    "productDetail": "Battery change",
    "manufactureDate": "2024-01-01"
  }'
echo -e "\n"

# Get first event
echo "Getting first event..."
curl -s -X GET "${BASE_URL}/dpp/${DPP_ID}/first"
echo -e "\n"

# Get history
echo "Getting history..."
curl -s -X GET "${BASE_URL}/dpp/${DPP_ID}/history"
echo -e "\n"

# Get last event
echo "Getting last event..."
curl -s -X GET "${BASE_URL}/dpp/${DPP_ID}/last"
echo -e "\n"