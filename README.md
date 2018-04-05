# custom-cf-resources
custom cloudformation resources implemented as lambdas using the [serverless framework](https://serverless.com/).

## What is this:
A collection of CloudFormation custom resources, deployed using the serverless framework, to handle those edge cases where CloudFormation is not flexible enough. It's a work in progress, more custom resources will be added as needed.

### Resources available:
1. Lambda [EventSourceMapping](event-source-mapping) sample: handle registering a lot of lambda functions to the same stream, and avoid bailing out if any of the CreateEventSourceMapping calls fail because of service limits. The subproject also demo 16 subscriptions to the stream.

### How to deploy:
Just `cd` to the corresponding directorty and type `sls deploy`



