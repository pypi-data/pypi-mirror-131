# Module overview
This module integrates with DUO MFA to get temporary access for aws
##Installation and execution
To install this package, please run the below command on your console.

```
pip install aws-access
```
This will install the package along with all its dependencies.
Once installed, execute the package using the below command

```
python -m aws_access_util.get_aws_access --awsurl <url> --u <user> --dur <duration> --p <password> --prf <profile> --r <role_arn>

url: This is the url of the AWS account
user: The userid to connect to the URL
password: The password to connect to the URL
dur: The duration in seconds for which access is required. Deafult is 1 hour
prf:AWS profile. Default is saml
r:Role ARN to assume the role if account is mapped with multiple roles.If it is not provided, then program will print the list of roles to choose if it is mapped with multiple roles
```
If none of the parameters are given, the utility will prompt for the value 
of the parameters except for duration(--dur),profile(--prf) and role_arn(--r). It will take default duration of 1 hour for dur and saml for profile

##Help information

To find out how to use the utility, you can execute the below command

``` 
python -m aws_access_util.get_aws_access --help

usage: get_aws_access.py [-h] [--awsurl URL] [--u USER] [--p PASSWORD]
                         [--dur DURATION_SECONDS] [--prf PROFILE] [--r ROLE_ARN]

Retrieves and stores a temporary token which is used to access AWS resource

optional arguments:
  -h, --help            show this help message and exit
  --awsurl URL          Specify a valid aws url
  --u USER              Specify your userid
  --p PASSWORD          Specify your password
  --dur DURATION_SECONDS
                        Specify duration in seconds for which you need
                        access.Must be > 900 and less than 43200. Default is 1
                        hour or 3600 secs.
  --prf profile			Specify profile name for aws credentials config, default will be saml
  --r role_arn			Specify Role ARN to select the specific role if it is mapped with multiple roles
```

##Authors

* **Rajib Deb** - *Initial Work* - [Cisco](rajdeb@cisco.com)
* **Mounika Gorintla** - [Cisco](mgorintl@cisco.com)
