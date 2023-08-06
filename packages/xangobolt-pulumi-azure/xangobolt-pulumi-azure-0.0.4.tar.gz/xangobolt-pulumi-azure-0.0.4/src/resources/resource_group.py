from arpeggio.cleanpeg import NOT, prefix
from pulumi.resource import ResourceOptions
import pulumi_azure_native.resources as resources

def resource_group(stem, props, provider=None, parent=None, depends_on=None):
    rg = resources.ResourceGroup(
        f'rg-{stem}',
        resource_group_name=f'rg-{stem}',
        tags=props.tags,
        location=props.location,
        opts=ResourceOptions(provider=provider, parent=parent, depends_on=depends_on)
    )
    return rg