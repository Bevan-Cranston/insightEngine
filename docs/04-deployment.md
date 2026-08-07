# Deployment

This document outlines the current deployment architecture of Insight Engine together with planned deployment 
experiments as the project evolves from local development towards cloud-hosted production environments.

## Current State
At present, the mobile web UI connects via localhost to the FastAPI server running on PC through WIFI. The server 
connects to MongoDB running locally on the same machine via pymongo.

## Experimentation
For future cloud deployment we have packaged the server into a Docker container and have test run this successfully. 
This experiment deliberately focused on validating application containerisation in isolation - without connecting to the
DB. Database containerisation will be explored separately to simplify debugging and validate each deployment stage 
independently.

## Future State and Experiments
When a dual container deployment has been tested locally, the plan is to upload these containers to ECR on AWS. 
Initially we will test a simple cloud deployment on EC2 with an S3 volume attached for persistent storage.

To achieve baseline scalability, we will consider Amazon Fargate for elastic EC2 deployments, 
in combination with Mongo Atlas. To experiment with the AWS ecosystem, we have also considered creating a VPC using 
DocumentDB on a private subnet.