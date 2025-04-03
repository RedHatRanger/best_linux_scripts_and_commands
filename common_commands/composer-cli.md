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

printf '\n[[packages]]\nname = "nginx"\nversion = "*"' >> node-app-server.toml

# You can also review the nginx being added
composer-cli blueprints show node-app-server
```
