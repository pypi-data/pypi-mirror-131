# Coding guidelines

Consistency is key, so here are some guidelines to ease the integration of new
code into the project.


## Style

The main rules to consider:

- follow [PEP8](https://www.python.org/dev/peps/pep-0008/) rules
- use English for all text
- use meaningful comments and object names
- use a context manager when opening a resource
  (files, gRPC channels, etc.)
- use the f-strings when possible, `.format()` method otherwise
- all runtime configuration should be defined in the `settings`
  module
- to add logs use the `LOGGER` object
- add comments where code is not explicit enough
- private and dummy variable names should start with `_`


## Adding an implementation

In order to add support for a new implementation,
you will need to add two files: one for the translation module
and one for the related tests.
As an example, for an hypothetic implementation called
`FasterThanBoltlight`:

- `boltlight/light_fasterthanboltlight.py`
- `tests/test_light_fasterthanboltlight.py`

Implementing all of the rpc methods included in `boltlight.proto` is not
mandatory.
For the unimplemented ones, a default error will be returned, signaling that
the method is not supported.

Variable names for LN node requests and responses are built from a
shortened implementation name (2/3 chars) and the suffix `_req` or `_res`.
Example names from currently supported implementations are:
-  `cl_req` / `cl_res`
-  `ecl_req` / `ecl_res`
-  `ele_req` / `ele_res`
-  `lnd_req` / `lnd_res`

Use instead the full names `request` and `response` when
communicating with the client interface.


## Error handling

Errors returned by LN implementations may differ, just like
operations, but boltlight needs to keep the client error interface
agnostic with respect to the underlying implementation.

To do so, LN errors are mapped between a specific and a common error dictionary
<sup>1</sup>, then a dispatcher method in the `errors` module builds the
`grpc.RpcError` object (from the common dictionary) and returns it to the
client via gRPC context, setting an appropriate `StatusCode` and message.

To add handling for an unmapped error you need to:
- identify a unique substring to match the implementation's error
- add an item to the `ERROR` dictionary using:
  - the identifed substring as key
  - the function to be called when handling the error <sup>2</sup>
  - the string representing the optional error function parameter
    <sup>3</sup>

An example error dictionary entry:
```python
ERRORS = {
    'string to be captured': {
        'fun': 'fun_to_call',
        'params': 'additional params to be passed'
    },
}
```

#### Notes

1. _see_ `Err.report_error()` _in `errors.py` and the specific implementation of
   the_ `_handle_error()` _method_
2. _see_ `errors.ERRORS`_'s keys for the list of available functions_
3. _supported if the erorr function's_ `msg` _contains_
   `%PARAM%`_, use_ `None` _otherwise_
