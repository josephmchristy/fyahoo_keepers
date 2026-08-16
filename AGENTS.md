# AGENTS.md

## Purpose

This repository generates keeper information for a long-running Yahoo fantasy football league.

Prioritize preserving existing keeper calculations and historical behavior over architectural cleanup.

## Working rules

* Make small, focused changes.
* Do not rewrite working code solely for style or modernization.
* Use the repo-local .venv for Python commands; never install dependencies globally.
* Preserve existing inputs and generated outputs unless a task explicitly requires changing them.
* Treat historical keeper outputs as regression evidence when available.
* Separate Yahoo/API concerns from keeper-rule calculations where practical.
* Prefer extracting testable logic over introducing new abstractions.
* Do not add dependencies unless they provide clear value.
* Do not change league rules based on assumptions. Ask or flag ambiguity instead.

## Keeper invariants

* Each team may keep at most 2 players.
* A player may be held for at most 3 seasons total: draft year plus 2 keeper years.
* Keeper cost normally starts one round earlier than the player's draft round and increases by one round for each subsequent keeper year.
* Players drafted in rounds 1 or 2 cannot be kept.
* An undrafted free-agent pickup has a 6th-round keeper cost.
* A drafted player who was dropped uses the better/higher-cost result of the applicable original draft value or the league's 6th-round rule.
* If the required pick is unavailable, an earlier-round pick may be substituted and becomes the player's new keeper cost.

When implementation behavior and these summarized rules appear to disagree, do not silently change the implementation. Identify the discrepancy first.