import addon_upgrade
import json

def lambda_handler(event, context):

    try:
        addon_upgrade.upgrade_addon_version()
    except Exception as e:
        print(e)
        return {
            'body': json.dumps('Failed to update!')
        }
    else:
        return {
            'body': json.dumps('Success to update!')
        }

