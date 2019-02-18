AWS Cloudwatch log Stream
=========

Manages a cloudwatch log stream

Role Variables
--------------

log_group_name
log_stream_name
state

Example Playbook
----------------

```
  # ensure present
  tasks:
    - name: log stream
      aws_cloudwatch_log_stream:
        log_group_name: example-log-group
        log_stream_name: example-stream
        state: present

  # ensure absent
  tasks:
    - name: log stream
      aws_cloudwatch_log_stream:
        log_group_name: example-log-group
        log_stream_name: example-stream
        state: absent
```


License
-------

BSD

Author Information
------------------
BGC Partners
