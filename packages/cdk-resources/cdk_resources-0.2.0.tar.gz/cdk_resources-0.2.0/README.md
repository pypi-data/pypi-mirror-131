# CDK Resources #

## Motivation
Regular **aws-cdk** has a *stack-based* architecture where resources are defined in each stack and then resources are
shared between stacks. This project is proposing a *resource-based* architecture as this would enable a more natural
organization of resources based on AWS services, and easier parameterization of resources across environments.
