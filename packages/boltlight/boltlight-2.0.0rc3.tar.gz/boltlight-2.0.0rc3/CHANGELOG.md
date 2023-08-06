# Changelog
All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0]

### Added
- support for c-lightning `v0.10.1`
- support for eclair `v0.6.1`
- support for electrum `v4.1.5`
- support for lnd `v0.13.3-beta`
- functional tests
- test handling with `tox`
- pytest and coverage reports upload from Gitlab CI
- code coverage html report on gitlab pages
- eclair: added `ListTransactions`, `NewAddress`, `PayOnChain`, `BalanceOnChain`
- proto: added a `GetInfo` API under the `Boltlight` service
- proto: added `node_unlocked` to `UnlockResponse`
- secure: added `unsafe_secrets` env variable to receive randomness from a
non-blocking source

### Changed
- renamed project from `lighter` to `boltlight`
- renamed CLI from `cliter` to `blink`
- renamed pairing script from `lighter-pairing` to `boltlight-pairing`
- renamed secure script from `lighter-secure` to `boltlight-secure`
- renamed `LICENSE.md` in `COPYING` (txt)
- renamed `unix_helper.sh` to `unix_helper`
- improved error handling for runtime operations
- use `UNAVAILABLE` error code when service is locked
- implemented `UnlockNode` also on implementations without a locking mechanism
- updated base python version from 3.5 (deptecated) to 3.7
- throw `node_locked` error instead of the generic `node_error` when node is
locked
- run tests with multiple python versions, in parallel
- proto: changed `ChannelState` and `InvoiceState` field order
- proto: changed the `GetNodeInfoResponse` `network` string field to a new
`Network.Name` enum field
- proto: changed the `AddressType` enum to `Address.Type`
- proto: changed the field order of `Address.Type`, `BalanceOnChainResponse`,
`Channel`, `DecodeInvoiceResponse`, `GetNodeInfoResponse`, `Invoice`,
`Payment`, `Peer` and `Transaction` messages/enums
- proto: changed some fields type
- proto: changed the `Order` enum to `Order.Direction`
- proto: moved `InvoiceState` inside the `Invoice` message and renamed it to
`State`
- proto: moved `ChannelState` inside the `Channel` message and renamed it to
`State`
- proto: renamed `Address.Type` fields
- proto: renamed all `blockheight` fields to `block_height`
- proto: renamed `UNKNOWN_INVOICE_STATE` to `UNKNOWN`
- proto: renamed `GetInfo` to `GetNodeInfo`
- proto: renamed the `Locker` service to `Boltlight`
- proto: renamed `ChannelBalance` to `BalanceOffChain`
- proto: renamed `WalletBalance` to `BalanceOnChain`
- proto: renamed `LockBoltlight` to `Lock`
- proto: renamed `UnlockBoltlight` to `Unlock`
- proto: renamed the `BalanceOffChain` `balance` field to `out_tot_msat`
- proto: renamed the `BalanceOnChainResponse` `balance` field to `total_sat`
and the `balance_confirmed` field to `confirmed_sat`
- proto: renamed the `Transaction` `num_confirmations` field to `confirmations`
- proto: renamed the `NewAddressRequest` `type` field to `addr_type`
- proto: renamed the `Invoice` `amount_msat` field to `amount_encoded_msat`
- proto: renamed the `Payment` `fee_base_msat` field to `fee_msat`
- proto: renamed all `expiry_time` occurrences to `expiry`
- proto: represent all amounts with integers and append unit name to field
names
- lnd: accept amounts with msat precision in `CreateInvoiceRequest`

### Removed
- removed `add_secret_type_column` migration
- common error mapping: `payinvoice_pending`
- proto: removed the `CheckInvoiceResponse` `settled` field
- proto: removed the `Transaction` `dest_addresses` field
- proto: removed the `Lock` `password` field
- proto: removed the `GetNodeInfoResponse` `version` field
- proto: removed the `out_max_now_msat` and `in_max_now_msat` fields from the
`BalanceOffChainResponse` message

### Fixed
- lnd: fixed `UnlockNode` when node is already unlocked
- proto: `DecodeInvoice` throws `unimplemented_parameter` error when
description in request (unsupported by eclair, electrum and lnd)
- secure: fixed deactivation of lnd macaroon


## [Forking point]

The original changelog doesn't include changes since the latest tag
(`1.2.0` - `a4f64869`).
Here's a brief recap of the major changes up to the forking point (`f2bab33b`).

### Added
- initial electrum support
- support for latest implementation versions
(c-lightning v0.8.2.1, eclair v0.4, lnd v0.10.1-beta)
- PyPi packaging

### Changed
- converted c-lightning and eclair calls from CLI to RPC
- default path for data (from `lighter-data` to `~/.lighter`)
- cliter: improved exit code (see the module's docstring for more info)
- secure: changed behaviour when configuring lnd secrets
- improved separation of implementation-specific code
- renamed `unix_make.sh` in `unix_helper.sh` and improved script
- improved nodes connection check
- refactored project `utils` structure

### Removed
- docker run support and related documentation

### Fixed
- docker build on arm32v7
- conversion method
- uncaught exceptions
- entrypoint exit codes
- secure: fixed DB check and unattended mode with new DB
- c-lightning: handle empty node address
- other minor bugs


## [1.2.0] - 2019-11-22

### Added
- default value for `expiry_time` in `CreateInvoice`
- paring procedure (`make pairing`)
- systemd example service
- `sqlalchemy` ORM for better DB handling and `alembic` as DB migration tool
- support for latest implementation versions
(c-lightning v0.7.3, eclair v0.3.2, lnd v0.8.0-beta)
- proto: added `state` field to `CheckInvoice` message
- proto: added `UnlockNode` API
- proto: added `unlock_node` field to `UnlockLighter` message
- secure: added non-interactive mode

### Changed
- default value of config var `DOCKER`
- improved security documentation
- updated pips and docker base image
- errors: changed double quotes into single around `%PARAM%`
- secure: ask for implemenetation password 2 times

### Deprecated
- docker assisted usage

### Fixed
- cliter: fixed bad escaping of double quotation mark
- Makefile: fixed pips install calling secure target
- secure: fixed password mismatch on new db case


## [1.1.1] - 2019-10-02

### Added
- cliter: add check for incompatible options
- cliter: add `--insecure`, `--macaroon`, `--no-macaroon`, `--rpcserver`,
`--tlscert`, `--version` options
- cliter: add installation in docker image
- support for c-lightning v0.7.2 (v0.7.2.1)

### Changed
- c-lightning: changed `listpayments` (deprecated) to `listsendpays`
- cliter: changed output format to JSON
- cliter: cli errors are now redirected to stderr (except for lighter errors)
and exit code is 1
- cliter: lighter errors are now printed in JSON format (`code` and `details`)
- removed default description from invoices

### Fixed
- c-lightning: fixed parsing of fallback address in `DecodeInvoice`
- c-lightning: fixed `PayOnChain`
- cliter: fixed packaging (add generation of proto files in `setup.py`)
- lnd: fixed closing txid decoding


## [1.1.0] - 2019-08-21

### Added
- support for latest implementation versions
(c-lightning v0.7.1, eclair v0.3.1, lnd v0.7.1-beta)
- error log when a request is aborted
- new common error mappings: `closechannel_failed`, `payinvoice_failed` and
`payinvoice_pending`
- dynamic implementation timeout based on client one
- log message when Lighter is locked
- config: added option to change console logging level
- eclair: added `OpenChannel`
- proto: added `amount_received_bits` field to `Invoice` message
- proto: added `balance_confirmed` field to `WalletBalanceResponse` message
- proto: added `CloseChannel` API (full support)
- proto: added `color` field to `Peer` message
- proto: added `(local|remote)_reserve_sat` fields to `Channel` message
- proto: added `LockLighter` API
- proto: added more granular balances to `ChannelBalanceResponse`
- proto: added `node_uri` field to `GetInfoResponse` message
- proto: added `payment_request` field to `Invoice` message
- proto: added `private` field to `Channel` message
- proto: added `state` and `active` fields to `Channel` message

### Changed
- added internal bech32 amount decode to avoid calling the node
(currently lnd's decode doesn't handle amounts below 1 sat)
- added operations to invoices macaroon
- code of conduct
- description of `unimplemented_method` and `unimplemented_parameter` errors
- improved implementation errors mapping
- made `make secure` mandatory
- refactored `Crypter` and `DbHandler`
- cli: increased timeout + log fix
- cli: renamed from `lit-cli` to `cliter`

### Fixed
- minor bugs in `PayInvoice`, `ListChannels`, `OpenChannel`, `ListPeers` and
`GetInfo`
- secure: added keyboard interrupt catching and decryption error handling

### Security
- generation of macaroon rootkey at runtime
- password documentation and auto generation
- using different derived key for each secret
- using `/dev/random` by default to generate password and salts


## [1.0.0] - 2019-04-23

### Added
- added security support
- added a CLI (`lit-cli`) with bash completion
- Makefile: added `secure` and `cli` targets
- proto: added `UnlockerServicer`
- errors: added mappings
- config: added variables `DB_DIR`, `DB_NAME`, `DISABLE_MACAROONS`,
`INSECURE_CONNECTION` and `MACAROON_DIR`
- add operation logging

### Changed
- Makefile: improved `clean` target (now removes also autogenerated files)
- proto/HopHint: renamed `fee_base_bits` to `fee_base_msat`

### Removed
- config: removed variables `ALLOW_INSECURE_CONNECTION`,
`ALLOW_SECURE_CONNECTION`, `ECL_PASS` `LND_MACAROON` and `LND_MACAROON_DIR`

### Fixed
- unix_make: improved bash portability and arch detect for macOS
- utils: fixed `check_connection` (now async and persistent until successful)

### Security
- added macaroon support
- added a database to store implementation secrets and macaroon root key
- added `secure` process for handling secrets


## [0.2.2] - 2019-03-06

### Fixed
- proto: fixed OpenChannel rpc definition
- lnd: fixed missing `max_precision` in `funding_bits` conversion of OpenChannel
- `KeyboardInterrupt` was not triggering `_slow_exit`


## [0.2.1] - 2019-03-04

### Changed
- Updated supported implementation versions

### Fixed
- Utils module tests (oops)
- c-lightning: wrong parameter for timestamp


## [0.2.0] - 2019-02-12

### Added
- New APIs (see support table):
  * ListInvoices
  * ListPayments
  * ListTransactions
  * OpenChannel
  * PayOnChain
- Supported APIs table
- gRPC version update (1.18.0)
- Node.js proto compilation example
- New error mappings
- lnd connection handling decorator
- Checks for required parameters

### Fixed
- Makefile: targets lint and test work on first run
- Dockerfile generation on arm
- c-lightning invoice creation (`check_value` usage)
- lighter.proto reordering (alphabetical sort)


## [0.1.0] - 2018-12-04

### Added
- Protobuf definitions
- Lighter dispatcher
- Support for c-lightning node
- Support for eclair node
- Support for lnd node
- Unified error handling
- Runtime settings management
- Utils common module
- Configuration support
- Graceful exit and signal handling
- Logging
- Test suite
- Building, running, testing and linting orchestration via Makefile
- Docker support with autogeneration of Dockerfile and compose file
- arm32v7 support
- Documentation


[Unreleased]: https://gitlab.com/hashbeam/boltlight/compare/2.0.0...develop
[2.0.0]: https://gitlab.com/hashbeam/boltlight/compare/f2bab33b...2.0.0
[Forking point]: https://gitlab.com/hashbeam/boltlight/compare/a4f64869...f2bab33b
[1.2.0]: https://gitlab.com/inbitcoin/lighter/compare/1.1.1...1.2.0
[1.1.1]: https://gitlab.com/inbitcoin/lighter/compare/1.1.0...1.1.1
[1.1.0]: https://gitlab.com/inbitcoin/lighter/compare/1.0.0...1.1.0
[1.0.0]: https://gitlab.com/inbitcoin/lighter/compare/0.2.2...1.0.0
[0.2.2]: https://gitlab.com/inbitcoin/lighter/compare/0.2.1...0.2.2
[0.2.1]: https://gitlab.com/inbitcoin/lighter/compare/0.2.0...0.2.1
[0.2.0]: https://gitlab.com/inbitcoin/lighter/compare/0.1.0...0.2.0
[0.1.0]: https://gitlab.com/inbitcoin/lighter/-/tags/0.1.0
