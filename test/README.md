# Tests for evaluating system

## How to use?
```
pytest
```


## Tests
### Latency test
Measures latencies of requests between client and server. Outputs average, min and max latencies to latencies.txt. Tests run many games in parallel. Fail if average latency is too high.

## End game test
End game properly when both players try to join at the same time.
