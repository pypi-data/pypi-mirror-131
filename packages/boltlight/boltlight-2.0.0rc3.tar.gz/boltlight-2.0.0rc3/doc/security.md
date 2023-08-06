# Security

Boltlight needs to secure communications on the client side and on the LN node
side. Doing this requires handling a number of secrets that need to be kept
confidential.

On the client side, boltlight uses TLS for connection privacy and
[macaroons](/doc/security.md#boltlights-macaroons) for authorization.
On the node side, security depends on the choice of implementation and
boltlight can make use of the node's security mechanisms.
A password is used to encrypt secrets, which are then stored in a SQLite
database. This password is never stored by boltlight and needs to be separately
saved and kept safe, as it's the only secret the user needs to access boltlight
and all its features.

Please note that deleting the database or recreating the macaroon files
invalidates all previously generated macaroons, preventing further access to
boltlight until macaroons are re-generated and configured on the client.

Secrets are encrypted using the _secretbox_ symmetric key algorithm and a
unique 32-byte key derived from boltlight's password using _scrypt_.

When boltlight is executed it starts in a locked state and will require its
password in order to transition to a fully operational state.

Upon unlocking, decryption correctness is verified with a token stored in the
database, secrets are then made available and normal operation begins.

More precisely, after fisrt being run or after being locked by the user, the
`Unlocker` service (see [boltlight.proto](/boltlight/boltlight.proto)) starts,
meaning API access is denied except for `Unlock`. The unlock API takes
boltlight's password, checks it's correct, decrypts the secrets stored in the
database, then exits, starting the runtime services (`Lightning` and
`Boltlight`). When unlocked, a `Lock` API is available to request locking
(boltlight password required).

Boltlight can optionally also unlock the underlying node, if the required
secrets have been configured.

## Setup

All security configuration is handled via the `boltlight-secure` command.

It sets boltlight's password and all the secrets required to operate.

You can choose an **interactive** mode by running:
```bash
boltlight-secure
```
This will prompt you for all the secrets required by the
[configured implementation](/doc/configuring.md#boltlight-section).
On a first run (or when overriding the database) it will ask you to set
boltlight's password, create boltlight's database and macaroon files
and ask for [implementation secrets](#implementation-secrets) (if any).
On successive runs, the provided password will be used to verify its
correctness, then implementation secrets and macaroons can be managed.

You can implicitly enable a **non-interactive** version by passing
secrets via environment variables.
A full-configuration example:
```bash
boltlight_password=somethingSecure create_macaroons=1 \
    eclair_password=eclairPassword \
    electrum_password=electrumPassword \
    lnd_macaroon=/path/to/lndMacaroon lnd_password=lndPassword \
    boltlight-secure
```
This will create or update the database without asking for user prompt.

`boltlight_password` is necessary to run in non-interactive mode.
`create_macaroons=1` (re)creates macaroon files (defaults to `0`).

It's not possible to automatically secure this operation for every possible
environment and it's ultimately the user's responsibility to assess the risks
and appropriate countermeasures for each specific situation.
As an example, pay attention to the risk of exposed secrets in cleartext files
(e.g.  `~/.bash_history`) or environment variables when using the
non-interactive mode.

Developers can set `unsafe_secrets=1` to receive randomness from a
non-blocking source (not suggested when using boltlight in production).
For more info read the [entropy source paragraph](#entropy-source).

## Password Strength

We strongly suggest the use of a
[password manager](https://en.wikipedia.org/wiki/List_of_password_managers)
to create and store a randomly crafted strong password on the users' behalf.
`boltlight-secure` supports the generation of its password when running for the
first time or after deleting the database.
The generation uses strong entropy and a 64-char alphabet to produce a
password that is 12 characters long.
When genereating a password manually it's highly recommended to follow
[guidelines](https://en.wikipedia.org/wiki/Password_strength#Guidelines_for_strong_passwords)
and best practices.

### Scrypt guarantees

The use of _scrypt_ to stretch the password with a random salt helps to make
stronger against brute-force and rainbow-table attacks. The
[_scrypt_ whitepaper](http://www.tarsnap.com/scrypt/scrypt.pdf)
gives an estimation on the cost of the hardware needed to crack a password in
one year on average with the default `cost_factor` at 2<sup>14</sup>, as
compared to other key derivation functions:

|KDF   |6 letters|8 letters|8 chars|10 chars|
|:-----|--------:|--------:|------:|-------:|
|PBKDF2|<$1      |<$1      |$18k   |$160M   |
|bcrypt|<$1      |$4       |$130k  |$1.2B   |
|scrypt|<$1      |$150     |$4.8M  |$43B    |

Although these values might become off by a factor of 10 due to hardware cost
instability or performance improvement, they offer a good idea on the
confidence one can put into a password.
__Important note:__ these values only apply in the case of _randomly_ chosen
passwords; the ones created to be remembered by humans tend to be weak against
pure dictionary attacks.

### Entropy source

The confidence that can be put on the solutions described above depends
significantly on the available entropy source. For this reason we use a
blocking (`/dev/random`) source of randomness which only returns when the
Operating System has enough entropy to fulfill the request.
On most devices this should not affect execution time, but if it is the case
you can help this process by doing one or more of the following in advance:
* install entropy collecting tools like
[haveged](https://linux.die.net/man/8/haveged)
* install a hardware TRNG
or one of the following while running `boltlight-secure`:
* randomly utilize an input device (keyboard, mouse) connected to the host
running boltlight
* type `unsafe` and press enter to use a non-blocking entropy source; this
choice will NOT be remembered for later runs

## Implementation secrets

### c-lightning

Boltlight connects directly to c-lightning's RPC-JSON socket so there are no
secrets to store, at the moment.
To prevent data leaks, a secure network connection is recommended. As an
example, boltlight and the node can be run as containers connected by a
private Docker network.

### eclair

We crypt eclair's password (`eclair.api.password` to be set on the eclair node,
along with `eclair.api=True`). <sup>1</sup>

If configured to run with eclair, `boltlight-secure` will ask to insert or
update its password.

### electrum

We crypt electrum's password (config `rpcpassword` on the electrum node).

If configured to run with electrum, `boltlight-secure` will ask to insert or
update its password.


### lnd

We crypt lnd's macaroon <sup>2</sup> and password, if given.

If configured to run with lnd, `boltlight-secure` will insert or update the
macaroon (if a path to the file has been provided) and ask if it should be used
when connecting to lnd, then ask to insert, update or skip lnd's password.
Connection with no macaroon will be attempted if none is available (requires
`--no-macaroons` to be set on the lnd node).

Attention, the choice of lnd macaroon could impact some boltlight
functionalities, as some operations could be forbidden.

The `UnlockNode` API and the `Unlock`'s boolean option `unlock_node` require
lnd's password, so it must have been provided running `boltlight-secure`.

#### Notes

1. _from version 1.0.0 variable_ `ECL_PASS` _is no longer necessary_
2. _from version 1.0.0 variables_ `LND_MACAROON` _and_ `LND_MACAROON_DIR` _are no longer
   necessary_


## Boltlight's macaroons

We use the `pymacaroons` and `macaroonbakery` packages to create and handle
[macaroons](https://ai.google/research/pubs/pub41892).
A randomly generated 32-byte key is used as root key to sign macaroons.
This key is encrypted and stored in the database.

At the moment, we provide 3 different types of macaroons, enabling the
following APIs:

| API                | **admin** | **readonly** | **invoices** |
| ------------------ | --------- | ------------ | ------------ |
| `BalanceOffChain`  |     ☇     |       ☇      |              |
| `BalanceOnChain`   |     ☇     |       ☇      |              |
| `CheckInvoice`     |     ☇     |       ☇      |       ☇      |
| `CloseChannel`     |     ☇     |              |              |
| `CreateInvoice`    |     ☇     |              |       ☇      |
| `DecodeInvoice`    |     ☇     |       ☇      |       ☇      |
| `GetInfo`          |     ☇     |       ☇      |       ☇      |
| `GetNodeInfo`      |     ☇     |       ☇      |       ☇      |
| `ListChannels`     |     ☇     |       ☇      |       ☇      |
| `ListInvoices`     |     ☇     |       ☇      |       ☇      |
| `ListPayments`     |     ☇     |       ☇      |              |
| `ListPeers`        |     ☇     |       ☇      |       ☇      |
| `ListTransactions` |     ☇     |       ☇      |              |
| `Lock`             |     ☇     |              |              |
| `NewAddress`       |     ☇     |              |              |
| `OpenChannel`      |     ☇     |              |              |
| `PayInvoice`       |     ☇     |              |              |
| `PayOnChain`       |     ☇     |              |              |
| `UnlockNode`       |     ☇     |              |              |
