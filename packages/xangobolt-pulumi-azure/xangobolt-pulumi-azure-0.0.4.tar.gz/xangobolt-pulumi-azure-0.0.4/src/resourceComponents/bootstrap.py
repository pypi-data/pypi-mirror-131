from pulumi import ComponentResource, ResourceOptions, StackReference
from pulumi_azure_native import storage
from resources import resource_group, storage_account, key_vault
import pulumi
from pulumi import Output

class Bootstrap(ComponentResource):
    def __init__(self, name: str, props: None, opts:  ResourceOptions = None):
        super().__init__('Bootstrap', name, {}, opts)

        # Create bootstrap resource group
        bootstrap_rg = resource_group.resource_group('pulumi-bootstrap', props, parent = self)

        # Create Storage account for state management
        bootstrap_sa = storage_account.storage_account('pulumistate', props, bootstrap_rg.name, parent=bootstrap_rg)

        # Create Storage container 
        bootstrap_bc = storage_account.container('pulumi-state', props, bootstrap_sa.name, bootstrap_rg.name, parent=bootstrap_sa)


        # Create Key Vault
        bootstrap_kv = key_vault.vault('pulumi-bootstrap', props, bootstrap_rg.name, object_id=props.objectId, parent=bootstrap_rg)

        # Create Key
        bootstrap_key = key_vault.key('pulumi-bootstrap', props, bootstrap_kv.name, bootstrap_rg.name, parent=bootstrap_kv, )