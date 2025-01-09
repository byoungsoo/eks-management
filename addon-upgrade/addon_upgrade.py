import boto3
import os
import json
import datetime

# boto3.setup_default_session(profile_name='shared-admin')

ec2Client = boto3.client('ec2')
asgClient = boto3.client('autoscaling')
ssmClient = boto3.client('ssm')
eks_client = boto3.client('eks')

def get_latest_addon(kubernetesVersion, addonName):
    addons = eks_client.describe_addon_versions(
        kubernetesVersion=kubernetesVersion,
        addonName=addonName,
    )
    # print(json.dumps(addons['addons'][0]['addonVersions'][0], indent=4))
    return addons['addons'][0]['addonVersions'][0]


def upgrade_addon_version():
    eks_clusters_res = eks_client.list_clusters()
    eks_clusters = eks_clusters_res['clusters']

    # exclude_eks_cluster = os.environ['ExcludeEKSClusters']
    # target_eks_clusters = [cluster for cluster in eks_clusters if cluster not in exclude_eks_cluster]
    target_eks_clusters = ["bys-shared-eks-main"]
    for cluster in target_eks_clusters:

        addons_res = eks_client.list_addons(
            clusterName=cluster
        )

        eks_details = eks_client.describe_cluster(
            name=cluster
        )
        eks_version = eks_details['cluster']['version']

        addons = addons_res['addons']
        for addon in addons:
            # print("AddonName: ", addon)
            latest_addon = get_latest_addon(eks_version, addon)

            ## To Do
            # Describe addon and get status. If Not Active then continue.
            addon_detail = eks_client.describe_addon(
                clusterName=cluster,
                addonName=addon
            )

            addon_status = addon_detail['addon']['status']
            current_addon_version = addon_detail['addon']['addonVersion']

            try:
                addon_configuration = addon_detail['addon']['configurationValues']
            except KeyError as e:
                addon_configuration = ""
                pass
            latest_addon_version = latest_addon['addonVersion']

            if current_addon_version != latest_addon_version:
                if addon_status == 'ACTIVE':
                    eks_client.update_addon(
                        clusterName=cluster,
                        addonName=addon,
                        addonVersion=latest_addon_version,
                        configurationValues=addon_configuration
                    )
                    print("UpdateCall - ", addon, " - ", latest_addon_version)
                else:
                    print(addon, "- status:", addon_status,  "- Skip(Status) -", latest_addon['addonVersion'])
                    continue
            else:
                print(addon, "- status: ", addon_status,  " - Skip(LatestVersion) - ", latest_addon['addonVersion'])


if __name__ == '__main__':
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Date:", formatted_date)
    upgrade_addon_version()