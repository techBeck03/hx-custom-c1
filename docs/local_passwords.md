# Creating Encrypted Passwords (SSH Key Alternative)

This guide walks through how to create encrypted passwords to use in your ansible playbook if you prefer to use a `password` for ssh access to the CRM master instead of creating SSH keys on each controller VM.


   
1. Build the salt image (only do this once)

   ```
   docker build -t salt ./salt
   ```

   Run a container from this image to generate the encrypted password.

   ```
   docker run --rm -it -v $PWD/vault_pass:/app/vault_pass salt
   ```
   
2. Choose a hyperflex cluster from your inventory file and enter the **password** at the command prompt shown below
   
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

3. Copy everything to the right of `secret:` in your output and paste in your `inventory.yml` file for the cluster whose password you entered

   ```
   all:
   vars:
     ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o userknownhostsfile=/dev/null'
     connection_type: password # valid choices are 'ssh_key' | 'password'
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

**Repeat the above for each remaining hyperflex cluster in your inventory**

4. Change the `connection_type` in `inventory.yml` to `password`
   
   ```
   all:
   vars:
     ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o userknownhostsfile=/dev/null'
     connection_type: password # valid choices are 'ssh_key' | 'password'
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
           ansible_ssh_pass: !vault |
             $ANSIBLE_VAULT;1.1;AES256
             65333737356439336430643239366361666336396539616632346630386663306161396164376162
             6434643766383061323034336666333633663931373238390a613431336466656332386631353565
             31646236633665613835383730653836373738313537386163646133306435376264633066316331
             3861346264303433330a333133363066353034643661383534626236653632336230663330336363
             6438
   ```

Return to the [Building and Running the Container](../README.md/#building-and-running-the-container) section of the **README** to complete the setup