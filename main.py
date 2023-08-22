import sdk
import os
import sys
import json
import boto3


###############################################################################
#   Ambiente                                                    #
###############################################################################
stage = os.getenv("STAGE")
if stage is None:
    stage = "dev"
else:
    stage = os.getenv("STAGE")
#### End Ambiente #############


def handler(event, context):

    client = boto3.client('dms')

    client.start_replication_task(
        ReplicationTaskArn='arn:aws:dms:us-east-1:864673161229:task:KWIWEEZGACM2UDL54LZONQWHNRIWI47CK5DL5UQ',
        StartReplicationTaskType='reload-target'
    )
    
    client.start_replication_task(
        ReplicationTaskArn='arn:aws:dms:us-east-1:864673161229:task:DTOUVWC3KYTRTC4YMF7M47NPWTGWRLKVHL3N7LA',
        StartReplicationTaskType='reload-target'
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": {}
        
    }
