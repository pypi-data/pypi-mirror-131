# Calibration Protocol #

Calibration session protocol: 

```gRPC
// The qserve service definition.
service QCalibrate {
  // submits a task and return a result
  rpc CreateExperiment (CreateExperimentRequest) returns (CreateExperimentResponse);
  rpc Run (stream Request) returns (stream Response);
}
```

```mermaid
sequenceDiagram
    participant Client as Client
    participant Server as Server
    Client->>+Server: Initialize
    Server->>Client: Initialized
    Client->>Server: Start
    loop while end criteria not reached
        Server->>+Client: Parameters 
        Client->>-Server: Fom
    end
    Server->>-Client: End
```
