#!/usr/bin/python
#
# Copyright (c) 2017 Ansible Project
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---

"""

try:
    import botocore
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

from ansible.module_utils._text import to_native
from ansible.module_utils.aws.core import AnsibleAWSModule
from ansible.module_utils.ec2 import boto3_conn, ec2_argument_spec, get_aws_connection_info


def is_stream_present(module, client):
    """Function to determine whether or not the log stream is present

    Arguments:
        module {[type]} -- [description]
        client {[type]} -- [description]
    """
    log_group_name = module.params.get('log_group_name')
    log_stream_name = module.params.get('log_stream_name')
    stream_present = False
    try:
        streams = client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name
        )
        if 'logStreams' in streams:
            for stream in streams['logStreams']:
                if stream['logStreamName'] == log_stream_name:
                    stream_present = True
    except botocore.exceptions.ClientError as e:
        module.fail_json_aws(e, msg='Unexpected error {0}'.format(to_native(e)))
    return stream_present


def ensure_deleted(module, client):
    """Deletes an elasticsearch domain by DomainName

    Arguments:
        module {[type]} -- [description]
        client {[type]} -- [description]
    """
    changed = False
    try:
        client.delete_log_stream(
            logGroupName=module.params.get('log_group_name'),
            logStreamName=module.params.get('log_stream_name')
        )
        changed = True
    except botocore.exceptions.ClientError as e:
        module.fail_json_aws(e, msg='Unexpected error {0}'.format(to_native(e)))
    return changed


def ensure_created(module, client):
    """Ensures elasticsearch domain is created

    Arguments:
        module {[type]} -- [description]
        client {[type]} -- [description]
    """
    changed = False
    try:
        client.create_log_stream(
            logGroupName=module.params.get('log_group_name'),
            logStreamName=module.params.get('log_stream_name')
        )
        changed = True
    except botocore.exceptions.ClientError as e:
        module.fail_json_aws(e, msg='Unexpected error {0}'.format(to_native(e)))
    return changed


def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(
        state=dict(type='str', choices=['present', 'absent'], default='present'),
        log_group_name=dict(type='str', required=True),
        log_stream_name=dict(type='str', required=True)
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
    )

    region, ec2_url, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
    client = boto3_conn(
        module,
        conn_type='client',
        resource='logs',
        region=region,
        endpoint=ec2_url,
        **aws_connect_kwargs)

    state = module.params.get('state')
    changed = False
    if state == 'present':
        if not is_stream_present(module, client):
            changed = ensure_created(module, client)
    elif state == 'absent':
        if is_stream_present(module, client):
            changed = ensure_deleted(module, client)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
