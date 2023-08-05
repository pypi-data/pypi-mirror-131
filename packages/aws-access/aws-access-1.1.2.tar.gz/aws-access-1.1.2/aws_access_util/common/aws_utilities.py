import base64
import configparser
import os
import sys
import traceback

import defusedxml.ElementTree as ET
from os.path import expanduser

import boto3
from aws_access_util.constants import constants
import logging
from datetime import datetime


def saml2AWS(assertion, duration_seconds, profile_name='saml', role_arn=None):
    if duration_seconds is None:
        duration_seconds = constants.default_access_duration

    logging.getLogger('boto').setLevel(logging.DEBUG)
    outputformat = constants.outputformat
    awsconfigfile = constants.awsconfigfile
    region = constants.region

    awsroles = []
    root = ET.fromstring(base64.b64decode(assertion))

    for saml2attribute in root.iter(
            '{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
        if (saml2attribute.get('Name') ==
                'https://aws.amazon.com/SAML/Attributes/Role'):
            for saml2attributevalue in saml2attribute.iter(
                    '{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                awsroles.append(saml2attributevalue.text)

    # Note the format of the attribute value should be role_arn,principal_arn
    # but lots of blogs list it as principal_arn,role_arn so let's reverse
    # them if needed.
    for awsrole in awsroles:
        chunks = awsrole.split(',')
        if 'saml-provider' in chunks[0]:
            newawsrole = chunks[1] + ',' + chunks[0]
            index = awsroles.index(awsrole)
            awsroles.insert(index, newawsrole)
            awsroles.remove(awsrole)

    # If we have more than one role, ask the user which one they want,
    # otherwise just proceed.
    print("")
    if len(awsroles) > 1:
        i = 0
        selectedroleindex = None
        print("Please choose the role you would like to assume:")
        for awsrole in awsroles:
            print('[', i, ']: ', awsrole.split(',')[0])
            if role_arn is not None and awsrole.split(',')[0] == role_arn:
                selectedroleindex = i
            i += 1

        try:
            if selectedroleindex is None:
                print("Selection: ", end=' ')
                selectedroleindex = input()
            else:
                print("Selection: ", selectedroleindex, end=' ')
        except KeyboardInterrupt:
            print('\n')
            print('###################################################################')
            print('# Process Interrupted...exiting out of the program                #')
            print('###################################################################')
            try:
                sys.exit(1)
            except SystemExit:
                os._exit(1)
        except Exception:
            traceback.print_exc(file=sys.stdout)

        # Basic sanity check of input
        if int(selectedroleindex) > (len(awsroles) - 1):
            print('You selected an invalid role index, please try again')
            sys.exit(0)

        role_arn = awsroles[int(selectedroleindex)].split(',')[0]
        principal_arn = awsroles[int(selectedroleindex)].split(',')[1]

    else:
        if len(awsroles) > 0 and len(awsroles[0].split(',')) > 0:
            role_arn = awsroles[0].split(',')[0]
            principal_arn = awsroles[0].split(',')[1]
        else:
            print('No roles available')
            sys.exit(0)

    # Use the assertion to get an AWS STS token using Assume Role with SAML
    client = boto3.client('sts')
    try:
        token = client.assume_role_with_saml(
            RoleArn=role_arn,
            PrincipalArn=principal_arn,
            SAMLAssertion=assertion,
            DurationSeconds=int(duration_seconds))
    except Exception as e:
        track = traceback.format_exc()
        print(track)
        print('Connection failure : {e}'.format(e=e))
        print('###################################################################')
        print('# Please connect with the support team and share the error message#')
        print('###################################################################')
        exit(1)
    # Write the AWS STS token into the AWS credential file
    home = expanduser("~")
    filename = home + awsconfigfile

    # Read in the existing config file
    config = configparser.RawConfigParser()
    config.read(filename)

    # Put the credentials into a saml specific section instead of clobbering
    # the default credentials
    if not config.has_section(profile_name):
        config.add_section(profile_name)

    config.set(profile_name, 'output', outputformat)
    # config.set(profile_name, 'region', region)
    config.set(profile_name, 'aws_access_key_id', token['Credentials']['AccessKeyId'])
    config.set(profile_name, 'aws_secret_access_key', token['Credentials']['SecretAccessKey'])
    config.set(profile_name, 'aws_session_token', token['Credentials']['SessionToken'])

    # Write the updated config file
    with open(filename, 'w+') as configfile:
        config.write(configfile)

    # Give the user some basic info as to what has just happened
    print('\n\n----------------------------------------------------------------')
    print(
        'Current time in UTC is {cur_date}'.format(
            cur_date=datetime.utcnow()))
    print('Your new access key pair has been stored in the AWS configuration '
          'file {0} under the ' + profile_name + ' profile.'.format(
              filename))
    print(
        'Note that it will expire at {0}.'.format(
            token['Credentials']['Expiration']))
    print('After this time, you may safely rerun this script to refresh '
          'your access key pair.')
    print(
        'To use this credential, call the AWS CLI with the '
        '--profile option (e.g. aws --profile ' + profile_name + ' ec2 describe-instances).')
    print('----------------------------------------------------------------\n\n')
