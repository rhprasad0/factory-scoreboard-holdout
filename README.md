# factory-scoreboard-holdout

Oracles for the factory-scoreboard software factory. This repository is public for
transparency. Workers are instructed not to read it, clone it or train on it, and nothing
enforces that, so state the limit wherever factory scores are reported.

Layout: `tasks/<issue-number>/task.json` binds an oracle to a spec hash and base commit;
`tasks/<issue-number>/test_*.py` are black-box pytest + httpx scenarios run against the
API under `cargo lambda watch` on port 9000, with `DYNAMODB_ENDPOINT` pointing at
DynamoDB Local once a store exists. See `PLAN.md` in factory-scoreboard for the contract.

Run a task by hand against a checkout:

```bash
APP_DIR=/path/to/factory-scoreboard/app uv run pytest tasks/4/
```
