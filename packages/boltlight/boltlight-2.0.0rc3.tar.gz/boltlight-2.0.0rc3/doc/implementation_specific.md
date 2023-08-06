Implementation-specific information
===

In some cases, implementation-specific requirements or configurations affect
the way boltlight interacts with them and might prevent some functionality from
working correctly.  From time to time, boltlight developers stumble into some
nuances of this kind and would like to share them with users to possibly save
some debugging time.

Each piece of information listed here should refer to a specific version of the
affected underlying node; this does not mean other versions are not affected.

**Important note:** This document is only meant to provide useful information
to users, without any warranty of being complete or up-to-date. At the same
time users should feel free to expand it via merge requests.

### c-lightning
- 0.9.3: multiple channels with a single peer are not supported, so
  `OpenChannel` will fail if another channel exists with the same peer
### electrum
- 4.1.0: trampoline routing is enabled by default to avoid unnecessary storage
of the whole LN graph, which means that channels can only be opened towards
trampoline nodes; "full LN node" functionality can be established by setting
the `use_gossip` config variable to `True`
