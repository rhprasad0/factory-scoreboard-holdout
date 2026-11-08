# factory-scoreboard-holdout

Hidden oracles for the factory-scoreboard software factory. Workers never check this
repository out; only the oracle CI job reads it, with a read-only deploy key.

Layout: `tasks/<issue-number>/task.json` binds an oracle to a spec hash and base commit;
`tasks/<issue-number>/test_*.py` are black-box pytest + httpx scenarios run against the
API under `cargo lambda watch` on port 9000 with `DYNAMODB_ENDPOINT` pointing at
DynamoDB Local. See `PLAN.md` in factory-scoreboard for the contract.
