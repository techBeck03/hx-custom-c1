# Creating SSH Keys (if not already configured)

By default the storage controller VMs do not have a trusted public key defined for the `admin` account.  You will need to SSH to each controller VM to using username and password initially to run the steps below.

## Prerequisites
- ssh public key (creating a key is not described in this guide)

## Setting up the Keys

The following steps need to be applied to **every controller vm** in your HX cluster

1. SSH to the controller VM using the admin account
   
   `ssh admin@hxctlvm1`

2. Create the `.ssh` directory if it doesn't already exist
   
   `mkdir ~/.ssh`

3. Add your public key to the `authorized_keys` file
   
   `cat "pasteYourPublicKeyHere" >> ~/.ssh/authorized_keys`

Return to the [Building and Running the Container](../README.md/#building-and-running-the-container) section of the `README` to complete the setup