# Creating SSH Keys (if not already configured)

By default the storage controller VMs do not have a trusted public key defined for the `admin` account.  You will need to SSH to each controller VM using username and password initially to run the steps below.

## Prerequisites
- ssh public/private key (creating a key is not covered in this guide)

## Setting up the Keys

The following steps need to be applied to **every controller vm** in your HX cluster

1. SSH to the controller VM using the admin account
   
   `ssh admin@cm-1`

2. Create the `.ssh` directory if it doesn't already exist
   
   `mkdir ~/.ssh`

3. Add your public key to the `authorized_keys` file
   
   `echo "pasteYourPublicKeyHere" >> ~/.ssh/authorized_keys`

## Encrypting the SSH key (Optional but recommended)

The following steps explain how to create an encrypted copy of your private key for ansible to use.  These commands should be issued locally within your cloned git repository and **not** on the controller VMs.

1. Copy your ssh key to the git repo root directory and name it `ssh.key`
   
   `cp ~/.ssh/id_rsa ./ssh.key`

2. Build the salt image (only do this once)

   ```
   docker build -t salt ./salt
   ```

3. Run a container from this image to generate the encrypted password.

   ```
   docker run --rm -it -v $PWD/vault_pass:/app/vault_pass -v $PWD/ssh.key:/app/encryptme:rw -e ENCRYPTION_TYPE=file salt
   ```
   
4. The `ssh.key` file should now be converted to an encrypted string

## Add the ssh key to inventory

1. Ensure the `connection_type` is set to `ssh_key` in your `inventory.yml` file
   
   ```yaml
   all:
     vars:
       ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o userknownhostsfile=/dev/null'
       connection_type: ssh_key # valid choices are 'ssh_key' | 'password'
     children:
       hxclusters:
         hosts:
           cm-1:
             ansible_user: admin
           cm-2:
             ansible_user: admin
    ```

2. Add your ssh key file to the inventory file.  The below example assumes the key is the same for all clusters.  If that's not the case for your environment then repeat the steps in the **Encrypting the SSH key** section for each key and define the `ansible_ssh_private_key_file` within each `host`
   
   ```yaml
   all:
     vars:
       ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o userknownhostsfile=/dev/null'
       connection_type: ssh_key # valid choices are 'ssh_key' | 'password'
       ansible_ssh_private_key_file: /app/ssh.key
     children:
       hxclusters:
         hosts:
           cm-1:
             ansible_user: admin
           cm-2:
             ansible_user: admin
    ```
   
Return to the [Building and Running the Container](../README.md/#building-and-running-the-container) section of the **README** to complete the setup