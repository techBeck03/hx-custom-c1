# HyperFlex Custom Report

This script provides a very basic HTML formatted report of an HX Cluster including cluster info, current CRM master, and rebalance status.  Some of the commands needed to generate this script are not yet exposed via the HXDP or Intersight API so ansible is used to SSH into the controller manager and issue the needed shell commands.

This script requires SSH using passwords to access the HX cm.  Automating this via Ansible requires the `sshpass` library which can be troublesome to install depending on your operating system.  Because of this, docker was used to package all of the necesary requirements into a portable container for execution.

Please follow the guide below to prepare your host for running this script.

## Prerequisites

- docker
- git

## Setup

1. Clone this repo using the following command
   `git clone https://github.com/techBeck03/hx-custom-c1.git`

2. Create vault password file to be used for encypting sensitive data
   `echo -n "supersecretpassword" > vault_pass`

3. Copy the example inventory file to `inventory.yml`
   `cp inventory.example.yml inventory.yml`

4. Modify the inventory file with your cluster info (passwords will be covered in a coming step)
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


Issue the command below to store an encrypted copy of the HX password using Ansible's built-in vault:

```bash
ansible-vault create --vault-id hxinfo@prompt access.yml
```

```bash
cluster:
  host: hxcm.example.com
  username: admin
  password: password
```