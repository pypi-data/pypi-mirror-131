# Configuring

The configuration file will be stored in the data directory, `~/.boltlight`
by default. The `--boltlightdir` option can be used to override it.

All configuration options are set in the `config` file and paths are
relative to the data directory.

See [config.sample](/examples/config.sample) for a commented example.
If run without a config file, the example file will be copied in place for the
user to edit.


#### Bare-minimum

For boltlight to work, you will need to set the following options:
* `implementation`
* `server_key` and `server_crt` (unless `insecure_connection` is `1`)
and then configure the section for the chosen implementation.

You can request TLS certificates from CAs (e.g. letsencrypt) or you can
generate your own. The certificate must include the host names or IP addresses
you will contact boltlight on, lest certificate validation failing in at
least some cases.

Example one-liner to generate a self-signed TLS certificate <sup>1</sup>:
```
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt -subj "/CN=node.example.com" -extensions SAN -config <(cat /etc/ssl/openssl.cnf <(printf "\n[SAN]\nsubjectAltName=DNS:node.example.com,DNS:boltlight,DNS:localhost,IP:127.0.0.1,IP:::1"))
```

### boltlight section

| Variable                      | Description                                                                |
| ----------------------------- | -------------------------------------------------------------------------- |
| `implementation` <sup>2</sup> | Implementation to use (possible values: `clightning`, `eclair`, `electrum`, `lnd`; no default) |
| `insecure_connection`         | Set to `1` to make boltlight listen in cleartext (default `0`). Implies disabling macaroons. |
| `port`                        | Boltlight's listening port (default `1708`)                                  |
| `server_key`                  | Private key path (default `./certs/server.key`)                            |
| `server_crt`                  | Certificate (chain) path (default `./certs/server.crt`)                    |
| `logs_dir`                    | Location <sup>4</sup> to hold log files (default `./logs`)                 |
| `logs_level`                  | Desired console log level (possible values: `critical`, `error`, `warning`, `info`, `debug`; default `info`) |
| `db_dir`                      | Location to hold the database (default `./db`)                             |
| `macaroons_dir`               | Location to hold macaroons (default `./macaroons`)                         |
| `disable_macaroons` <sup>3</sup> | Set to `1` to disable macaroons authentication (default `0`)            |

### blink section

| Variable                      | Description                                                                |
| ----------------------------- | -------------------------------------------------------------------------- |
| `rpcserver`                   | Boltlight host[:port] (default `localhost:1708`)                             |
| `tlscert`                     | Boltlight certificate (chain) path (default `./certs/server.crt`)          |
| `macaroon`                    | Boltlight macaroon path (default `./macaroons/admin.macaroon`)             |
| `insecure`                    | Set to `1` to connect to boltlight in cleartext  (default `0`)               |
| `no_macaroon`                 | Set to `1` to connect to boltlight with no macaroon (default `0`)            |


### clightning section

| Variable                      | Description                                                                |
| ----------------------------- | -------------------------------------------------------------------------- |
| `cl_rpc_dir` <sup>5</sup>     | Location <sup>4</sup> containing `cl_rpc`                                  |
| `cl_rpc` <sup>6</sup>         | JSON-RPC socket name (default `lightning-rpc`)                             |

### eclair section

| Variable                      | Description                                                                |
| ----------------------------- | -------------------------------------------------------------------------- |
| `ecl_host`                    | Host <sup>7</sup> (default `localhost`)                                    |
| `ecl_port` <sup>8</sup>       | Port (default `8080`)                                                      |

### electrum section

| Variable                      | Description                                                                |
| ----------------------------- | -------------------------------------------------------------------------- |
| `ele_host`                    | Host <sup>7</sup> (default `localhost`)                                    |
| `ele_port`                    | Port (default `7777`)                                                      |
| `ele_user`                    | User (default `user`)                                                      |

### lnd section

| Variable                      | Description                                                                |
| ----------------------------- | -------------------------------------------------------------------------- |
| `lnd_host`                    | Host <sup>7</sup> (default `localhost`)                                    |
| `lnd_port`                    | Port (default `10009`)                                                     |
| `lnd_cert_dir`                | Location <sup>4</sup> containing `lnd_cert`                                |
| `lnd_cert`                    | TLS certificate name (default `tls.cert`)                                  |

#### Notes

1. _requires the package_ `openssl` _to be installed, which provides_
   `/etc/ssl/openssl.cnf`
2. _implementation value is case-insensitive_
3. _running boltlight on mainnet with macaroons disabled has severe security
   implications and is highly discouraged, don't do this unless you know
   what you're doing_
4. _location must be a directory;
   path can be absolute or relative (to boltlight's data directory)_
5. _usually ~/.lightning/\<network\>_
6. _option:_ `rpc-file` _the JSON-RPC socket needs to be owned by the same user
   boltlight is running as_
7. _host can be an IP or a FQDN_
8. _option:_ `eclair.api.port` _(usually 8080)_
