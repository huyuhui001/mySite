# SUSE Enterprise Storage Foundation and Basic Operation

## [SUSE Enterprise Storage Foundation](./linux_ses_memo.md)

## [SUSE Enterprise Storage Basic Operation](./linux_ses_demo.md)

### 1. Installation
#### 1.1. Environment Setup
#### 1.2. Install Packages
#### 1.3. Stage 0 — the preparation
#### 1.4. Stage 2 — the configuration
#### 1.5. Stage 3 — the deployment
#### 1.6. Stage 4 — the services
#### 1.7. Stage 5 — the removal stage
#### 1.8. Installation Guide
#### 1.9. Issues during installation
#### 1.10. Shutting Down the Whole Ceph Cluster
#### 1.11. Starting, Stopping, and Restarting Services Using Targets
#### 1.12. Restarting All Services
#### 1.13. Restarting Specific Services

### 2. Basic Operation
#### 2.1. Pools and Data Placement
##### 2.1.1. Enable the PG Autoscaler and Balancer Modules
##### 2.1.2. Manipulate Erasure Code Profiles
##### 2.1.3. Manipulate CRUSH Map Rulesets
##### 2.1.4. Investigate BlueStore

#### 2.2. Common Day 1 Tasks Using the CLI
##### 2.2.1. Ceph Users and Configuration
##### 2.2.2. Run the Ceph Health Commands
##### 2.2.3. Manipulate Pools
##### 2.2.4. Maintain consistency of data with Scrub and Repair
##### 2.2.5. Manipulate Manager Modules
##### 2.2.6. Introduction to the Tell command

#### 2.3. Ceph Dashboard
##### 2.3.1. Access Dashboard
##### 2.3.2. Explore the Dashboard Health, Performance, Status

#### 2.4. Storage Data Access
##### 2.4.1. Ensure the SES Cluster is Healthy
##### 2.4.2. Use the S3 API to Interact with the RADOS Gateway
##### 2.4.3. Use the swift API to Interact with the RADOS Gateway
##### 2.4.4. Create Snapshots on SES using RBD
##### 2.4.5. Create and manage COW Clones with rbd
##### 2.4.6. Configure iSCSI on SES
##### 2.4.7. Mount CephFS Provided by SUSE Enterprise Storage
##### 2.4.8. Export an NFS Share from SES with NFS Ganesha
##### 2.4.9. Configure and Mount CIFS

