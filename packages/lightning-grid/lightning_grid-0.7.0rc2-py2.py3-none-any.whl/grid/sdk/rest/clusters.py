from grid.openapi import V1ClusterState, V1ClusterType, V1ListClustersResponse
from grid.sdk.rest import GridRestClient
from grid.sdk.rest.exceptions import throw_with_message


@throw_with_message
def list_clusters(c: GridRestClient, is_global: bool = False) -> V1ListClustersResponse:
    if is_global:
        resp = c.cluster_service_list_clusters(
            phase_in=[V1ClusterState.RUNNING], cluster_type_in=[V1ClusterType.GLOBAL]
        )
    else:
        resp = c.cluster_service_list_clusters(phase_in=[V1ClusterState.RUNNING])
    return resp
