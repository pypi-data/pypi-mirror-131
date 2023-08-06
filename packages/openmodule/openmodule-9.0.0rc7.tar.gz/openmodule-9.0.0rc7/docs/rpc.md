# RPC Server

TODO

# RPC Client

## Blocking RPC Requests

The rpc client can be used to call functions which other services provide via an [RPC Server](#RPC Server). The RPC
client is accessible through the `OpenModuleCore` instance.

```python
result = core().rpc_client.rpc(b"channel", "test", SomeRequest())
result.status  # ok
```

A blocking RPC call is equivalent to calling `.result()` on a non-blocking call:

```python
rpc_client.rpc(b"channel", "test", SomeRequest())
# -> equivalent
rpc_client.rpc(b"channel", "test", SomeRequest(), blocking=False).result()
```

### Using a dedicated RPC client

Currently we do not see a reason why this is necessary, but you can instantiate the RPC client manually. In this case
you need to provide a `MessageDispatcher` which the RPC client uses to listen for RPC responses. It however still uses
the `OpenModuleCore.publish` function, to send out rpc requests.

```python
sub_socket = get_sub_socket(core().context, settings)
my_dispatcher = ZMQMessageDispatcher(sub_socket)
rpc_client = RPCClient(my_dispatcher)

while True:
    topic, message = receive_message_from_socket(some_sub_socket)
    my_dispatcher.dispatch(topic, message)
```

## Non Blocking RPC Requests

By passing `rpc(..., blocking=False)` the rpc call returns a `RPCEntry` object, which can be used for waiting for an RPC
response asynchronously.

```python
future = client.rpc(b"channel", "test", SomeRPCRequest(), blocking=False)

# The future object can be used to wait for the RPC result asynchronously
future.result(timeout=1)

# You can also check if a response is available 
future.done()  # True
```

### About Timeouts

Please note that you **cannot extend the timeout, after sending the rpc request**. For example if you send an PRC
request with a timeout of 5 seconds:

```python
future = client.rpc(b"channel", "test", SomeRPCRequest(), blocking=False, timeout=5)
```

You cannot wait for longer than 5 seconds.

```python
future.result(timeout=10)

# UserWarning: You cannot extend the timeout of an RPC after sending the request. The timeout will be limited to at most the initial timeout.
#  result.result(timeout=2)
```

This is because the RPC Client's worker discards timed out rpc requests in order to conserve memory. If however a
response was already received within the timeout, calling `result()` will not trigger a timeout error.
