# regulatory_compliance

1. clone the repository
2. make sure you have done the `az login`
3. run the scirpt

```
$ pip install -r requirements.txt
$ virutalenv venv
$ source venv/bin/activate

$ python index.py

Control ID: 3.7
State: Failed
Description: Ensure that 'Public access level' is disabled for storage accounts with blob containers
------
Control ID: 3.8
State: Failed
Description: Ensure Default Network Access Rule for Storage Accounts is Set to Deny
------
