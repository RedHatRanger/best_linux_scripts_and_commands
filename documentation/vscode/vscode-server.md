To manually install the VS Code Server on a Red Hat Enterprise Linux (RHEL) machine in an isolated network without internet access, follow these steps:
 
1. **Identify the required VS Code Server version**:  
   On your local machine, open VS Code and attempt to connect to the remote RHEL host using the Remote - SSH extension. Since the network is isolated, the connection will fail, but VS Code will log the commit ID of the VS Code Server it is trying to install. You can find this information in the Output tab under "Remote - SSH"
 
2. **Download the VS Code Server offline package**:    *****ATTACHED TO THIS MESSAGE*****
   Use an external machine with internet access to download the VS Code Server tarball using the commit ID obtained in the previous step. The download URL follows this format:  
   `https://update.code.visualstudio.com/commit:{COMMIT_ID}/server-linux-x64/stable`  
   For example: Commit ID  ddc367ed5c8936efe395cffeec279b04ffd7db78
  `https://update.code.visualstudio.com/commit:ddc367ed5c8936efe395cffeec279b04ffd7db78/server-linux-x64/stable`  
 
3. **Transfer the tarball to the RHEL machine**:  
   Copy the downloaded `vscode-server-linux-x64.tar.gz` file to the target RHEL machine using a USB drive, SCP, or another secure transfer method
 
4. **Prepare the remote server directory**:  
   On the RHEL machine, create the appropriate directory under `~/.vscode-server/bin/` using the commit ID:  
   ```bash
   mkdir -p ~/.vscode-server/bin/ddc367ed5c8936efe395cffeec279b04ffd7db78
   ```
 
5. **Extract the tarball**:  
   Navigate to the created directory and extract the tarball:
   ```bash
   cd ~/.vscode-server/bin/c9a2f78283b6e5ef708fb8869e2a5adaa476e42f
   tar -xvzf ~/vscode-server-linux-x64.tar.gz --strip-components 1
   ```
   This extracts the server binaries and required files such as `server.sh`, `package.json`, and the `out/` directory
 
6. **Ensure compatibility**:  
   The prebuilt VS Code Server requires `glibc >= 2.28` and `libstdc++ >= 3.4.25` RHEL 8 and later meet these requirements If using an older RHEL version, you may need to provide a compatible sysroot and use `patchelf` (version 0.18 or higher) to patch the binaries, though this is not officially supported
 
7. **Set up authentication (optional)**:  
   If you plan to use Settings Sync, configure a keyring on the server to persist secrets. Otherwise, secrets will be stored in memory and lost when the server stops
 
8. **Connect from VS Code**:  
   Return to your local VS Code instance and reconnect to the RHEL host via Remote - SSH. The connection should now succeed, as the required server is already in place
 
Note: The VS Code Server is designed for single-user access and is not licensed for hosting as a multi-user service