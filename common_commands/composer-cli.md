# LAB: Composer-CLI to build VMs

```
dnf install -y composer-cli osbuild-composer
systemctl enable --now osbuild-composer.socket

composer-cli blueprints list
# There will be no existing blueprints yet

# To save some time look at the node-app-server.toml file that has already been pre-created using a tool like cat or less
cat node-app-server.toml


# The name of the blueprint is called node-app-server. It is recommended that you also include a description so that others using this blueprint know what system image they are building.
# At this point, the blueprint file does not have any packages but we will add the nodejs and nginx packages to it.
# nodejs is distributed as an application stream for Red Hat Enterprise Linux, so you will need to add a [[packages]] section to the node-app-server.toml file adding nodejs to the build.

printf '\n[[packages]]\nname = "nodejs"\nversion = "*"' >> node-app-server.toml
# The printf command appends the following formatted stanza to the node-app-server.toml file.

# In order to create the blueprint from the local TOML file, we will use the blueprints push cli option.
composer-cli blueprints push node-app-server.toml

# To verify that your update has been made, review the log of changes made to the node-app-server blueprint.
composer-cli blueprints changes node-app-server

cat << EOF >> node-app-server.toml
[[packages]]
name = "nginx"
version = "*"
EOF

# You can also review the nginx being added
composer-cli blueprints show node-app-server

# Use the composer-cli command to start a compose based on the node-app-server blueprint. For this lab, you will use the output format of qcow2. However, you could build many different types of images including:
# Output type	          Details:
# ami	                  Amazon EC2
# openstack	            OpenStack image
# qcow2	                qcow2 image
# rhel-edge-commit	    RHEL edge image
# tar	                  tar archive
# vhd	                  virtual hard disk
# vmdk	                Virtual Machine disk

composer-cli compose start node-app-server qcow2
composer-cli compose status

# In the next steps, you will access the machine image, however it will not work if the machine image is not yet completed. The compose can take upwards of 5 minutes.
# The below command is a small until shell script that will run until the completed machine image is created.

until $(composer-cli compose status | tail -1 | grep FINISHED &>/dev/null); do echo "Compose not finished ... waiting 10 seconds"; sleep 10; done; echo "COMPOSE FINISHED"
composer-cli compose image $(composer-cli compose status | tail -1 | cut -f1 -d" ")
```
