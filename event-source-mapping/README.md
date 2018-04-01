### Event Source Mapping Custom resource

Meant to be a 1:1 replacement for [AWS::Lambda::EventSourceMapping](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lambda-eventsourcemapping.html).
This custom resource will not bail out at the first exception whn attempting to register a Lambda to a Kinesis Stream.
This example deploys 16 Lambda consumers for one Kinesis stream.

Just deploy this stack with `sls deploy`, then run `sls invoke local -f loader` to load some data in your stream, and then modify the `BatchSize` parameter in each `EventSourceMapping` object in `serverless.yaml`:

```yaml
   EventSourceMapping00:
      Type: Custom::EventSourceMapping
      Properties:
        ServiceToken: 
          Fn::GetAtt: [MapperLambdaFunction, Arn]
        EventSourceArn:
          Fn::GetAtt: [EventStream,Arn]
        FunctionName: 
          Fn::GetAtt: [Sink00LambdaFunction,Arn]
        StartingPosition: LATEST
        BatchSize: 5
        Enabled: True
```
The Custom resource will retry registering any time it gets a `ProvisionedThroughputExceededException` or a `LimitExceededException`, without bailing out.

