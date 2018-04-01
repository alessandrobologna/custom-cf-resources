# custom-cf-resources
custom cloudformation resources implemented as lambdas

## What is this
A collection of CloudFormation custom resources, deployed using the serverless framework, to handle those edge cases where CloudFormation is not flexible enough.

###Resources available:

1. Lambda EventSourceMapping sample: handle registering a lot of lambda functions to the same stream, and avoid bailing out if any of the CreateEventSourceMapping calls fail because of service limits.


### How to deploy:
Just `cd` to the corresponding directorty and type `sls deploy`



