# HyperFlex Custom Report

This script provides a very basic HTML formatted report of an HX Cluster including cluster info, current CRM master, and rebalance status.  Some of the commands needed to generate this script are not yet exposed via the HXDP or Intersight API so ansible is used to SSH into the controller manager and issue the needed shell commands.

This script supports SSH using passwords (as well as ssh keys) to access the HX CRM master.  Automating this via Ansible requires the `sshpass` library which can be troublesome to install depending on your operating system.  Because of this, docker was used to package all of the necesary requirements into a portable container for execution.

Please follow the guide below to prepare your host for running this script.

## Prerequisites

- docker
- git

## Setup

### Cloning the repo

1. Clone this repo using the following command
   
   ```
   git clone https://github.com/techBeck03/hx-custom-c1.git
   cd hx-custom-c1
   ```

### Preparing files

1. Create vault password file to be used for encypting sensitive data
   
   `echo -n "supersecretpassword" > vault_pass`

2. Copy the example inventory file to `inventory.yml`
   
   `cp inventory.example.yml inventory.yml`

3. Modify the inventory file with your cluster info (**passwords will be covered in the next step**)
   
   ```yaml
   all:
   vars:
     ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o userknownhostsfile=/dev/null'
     connection_type: ssh_key # valid choices are 'ssh_key' | 'password'
   children:
     hxclusters:
       hosts:
         cm-1:
           ansible_use: admin
         cm-2:
           ansible_use: admin
   ```
   `cm-1` and `cm-2` in the code above are the fqdn or IP address of the CRM master for a given hyperflex cluster.  Only one entry is needed per cluster.  The `connection_type` value will be covered in more detail in a later step.

4. Copy the example `group_vars` file

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

### Preparing for remote access
   
   Ansible requires ssh access to the CRM master in order to run the shell commands necessary for creating the report.  You can choose to use `SSH keys` OR `user/pass` to establish these ssh connections from ansible.  Choose a guide below based on your preference and then return to the next section to complete the setup.

   - [SSH Keys](docs/ssh_keys.md)
   - [user/pass](docs/local_passwords.md)

### Building and running the container

1. Build the docker image to run the script

   `docker build -t hx-report .`

2. Run the docker image to generate and email the report

   `docker run --rm -it hx-report`


## Example Report
![Example Report](/docs/img/example_report.png?raw=true)

### Please report any issues to this git repository and not to the author directly.