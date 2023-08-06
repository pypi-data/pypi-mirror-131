from pulumi import ComponentResource, ResourceOptions, StackReference
from resources import operational_insights, security_insights, resource_group


class AzureSentinel(ComponentResource):
    def __init__(self, name: str, props: None, opts: ResourceOptions = None):
        super().__init__('Sentinel', name, {}, opts)

        Resources = [security_insights, operational_insights]

        for resource in Resources:
            resource.location = props.location
            # resource.resource_group_name = props.resource_group_name
            resource.self = self
            resource.tags = props.tags

        sentinel_rg = resource_group.resource_group(
            name, 
            props=props,
            provider=opts.providers.get('xangobolt'),
            parent=self,
        )

        sentinel_workspace = operational_insights.Workspace(
            name,
            props,
            resource_group=sentinel_rg.name,
            provider=opts.providers.get('xangobolt'),
            parent=sentinel_rg
        )

        xb_sentinel = security_insights.Sentinel(
            name, 
            props=props,
            resource_group=sentinel_rg.name,
            workspace=sentinel_workspace.name,
            provider=opts.providers.get('xangobolt'),
            parent=sentinel_rg
        )

        ea = security_insights.EntityAnalytics(
            name,
            props=props,
            resource_group=sentinel_rg.name,
            workspace=sentinel_workspace.name,
            provider=opts.providers.get('xangobolt'),
            parent=sentinel_rg,
            depends_on=xb_sentinel
        )

        ueba = security_insights.Ueba(
            name,
            props=props,
            resource_group=sentinel_rg.name,
            workspace=sentinel_workspace.name,
            provider=opts.providers.get('xangobolt'),
            parent=sentinel_rg,
            depends_on=ea
        )

        # ascc = security_insights.ASCConnector(
        #     name,
        #     props=props,
        #     resource_group=sentinel_rg.name,
        #     workspace=sentinel_workspace.name,
        #     subscription="44798e5a-c098-4be2-9077-99b93cb24fd3",
        #     provider=opts.providers.get('xangobolt'),
        #     parent=sentinel_rg,
        #     depends_on=xb_sentinel
        # )

        # aaddc = security_insights.AADDataConnector(
        #     name,
        #     props=props,
        #     resource_group=sentinel_rg.name,
        #     workspace=sentinel_workspace.name,
        #     tenant_id="90b0fe7d-3ae6-4cae-b850-625b1fbb8b8c",
        #     provider=opts.providers.get('xangobolt'),
        #     parent=sentinel_rg,
        #     depends_on=xb_sentinel
        # )

        o365dc = security_insights.O365DataConnector(
            name,
            props=props,
            resource_group=sentinel_rg.name,
            workspace=sentinel_workspace.name,
            tenant_id="90b0fe7d-3ae6-4cae-b850-625b1fbb8b8c",
            provider=opts.providers.get('xangobolt'),
            parent=sentinel_rg,
            depends_on=xb_sentinel
        )


        mdcadc = security_insights.MDCADataConnector(
            name,
            props=props,
            resource_group=sentinel_rg.name,
            workspace=sentinel_workspace.name,
            tenant_id="90b0fe7d-3ae6-4cae-b850-625b1fbb8b8c",
            provider=opts.providers.get('xangobolt'),
            parent=sentinel_rg,
            depends_on=xb_sentinel
        )
