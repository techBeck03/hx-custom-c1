# HyperFlex Custom Report

This script provides a very basic HTML formatted report of an HX Cluster including cluster info, current CRM master, and rebalance status.  Some of the commands needed to generate this script are not yet exposed via the HXDP or Intersight API so ansible is used to SSH into the controller manager and issue the needed shell commands.

This script requires SSH using passwords to access the HX cm.  Automating this via Ansible requires the `sshpass` library which can be troublesome to install depending on your operating system.  Because of this, docker was used to package all of the necesary requirements into a portable container for execution.

Please follow the guide below to prepare your host for running this script.

## Prerequisites

- docker
- git

## Setup

1. Clone this repo using the following command
   
   ```
   git clone https://github.com/techBeck03/hx-custom-c1.git
   cd hx-custom-c1
   ```

2. Create vault password file to be used for encypting sensitive data
   
   `echo -n "supersecretpassword" > vault_pass`

3. Copy the example inventory file to `inventory.yml`
   
   `cp inventory.example.yml inventory.yml`

4. Modify the inventory file with your cluster info (**passwords will be covered in the next step**)
   
   ```yaml
   all:
   vars:
     ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o userknownhostsfile=/dev/null'
   children:
     hxclusters:
       hosts:
         cm-1:
           ansible_use: admin
           ansible_ssh_pass: PASTE ENCRYPTED PASSWORD HERE
         cm-2:
           ansible_use: admin
           ansible_ssh_pass: PASTE ENCRYPTED PASSWORD HERE
   ```

5. Create an encrypted password for each cluster defined in your inventory above
   
   Build the salt image (only do this once)

   ```
   docker build -t salt ./salt
   ```

   Run a container from this image to generate the encrypted password.

   ```
   docker run --rm -it -v $PWD/vault_pass:/app/vault_pass salt
   ```
   
   Choose a hyperflex cluster from your inventory file and enter the **password** at the command prompt shown below
   
   ```
   Please enter the password to encrypt
   Password: 
   secret: !vault |
             $ANSIBLE_VAULT;1.1;AES256
             65333737356439336430643239366361666336396539616632346630386663306161396164376162
             6434643766383061323034336666333633663931373238390a613431336466656332386631353565
             31646236633665613835383730653836373738313537386163646133306435376264633066316331
             3861346264303433330a333133363066353034643661383534626236653632336230663330336363
             6438
   ```

   Copy everything to the right of `secret:` in your output and paste in your `inventory.yml` file for the cluster whose password you entered

   ```
   all:
   vars:
     ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o userknownhostsfile=/dev/null'
   children:
     hxclusters:
       hosts:
         cm-1:
           ansible_use: admin
           ansible_ssh_pass: !vault |
             $ANSIBLE_VAULT;1.1;AES256
             65333737356439336430643239366361666336396539616632346630386663306161396164376162
             6434643766383061323034336666333633663931373238390a613431336466656332386631353565
             31646236633665613835383730653836373738313537386163646133306435376264633066316331
             3861346264303433330a333133363066353034643661383534626236653632336230663330336363
             6438
         cm-2:
           ansible_use: admin
           ansible_ssh_pass: PASTE ENCRYPTED PASSWORD HERE
   ```

   > **Repeat the above for each remaining hyperflex cluster in your inventory**

6. Copy the example `group_vars` file

   `cp group_vars/all.yml.example group_vars/all.yml`

   Edit the mail related variables specific to your environment
   ```yaml
   mail_server: mail.example.com
   mail_port: 25
   mail_from_address: sender@example.com (Lab Reporting)
   mail_report_recipients:
     - you@example.com
     - someoneelse@example.com
   ```

7. Build the docker image to run the script

   `docker build -t hx-report .`

8. Run the docker image to generate and email the report

   `docker run --rm -it hx-report`


## Example Report
![Example Report](/docs/img/example_report.png?raw=true)

### Please report any issues to this git repository and not to the author directly.