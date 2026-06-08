# Nao — optional agentic BI appendix

Hands-on **natural language → SQL → chart** on Open Food Facts. The lecture
covers agentic BI failure modes; this guide is for students who want to try
the pipeline themselves.

**In class:** we may demo this live. **Self-paced:** follow the steps below.

Goal: run the pipeline, open the SQL every time, and hit at least one prompt
where the answer looks plausible but is wrong — then apply the verification
checklist (same spirit as the ethics drill on Streamlit charts).

## Prerequisites

- `data/openfoodfacts.parquet` (same as Sessions 3–6)
- An LLM API key. Warning: the default Nao setup might write it in `nao_config.yaml`, use `api_key: ${{ env('ANTHROPIC_API_KEY') }}` to avoid leakage.

## 1. Build the DuckDB

Nao profiles the database to feed the LLM column stats and hints. We keep ~15
demo-relevant columns over the full ~3M-row Parquet:

```bash
uv run python session6/build_off_db.py
# writes session6/data/off.duckdb
```

Smoke test (smaller sample):

```bash
uv run python session6/build_off_db.py --sample 50000
```

## 2. Configure the workspace

Follow instructions in https://github.com/getnao/nao.

Already in this repo as examples but can be overriden (or removed) in case of conflict

```
session6/nao-workspace/
├── nao_config.yaml   # points at ../data/off.duckdb
└── RULES.md          # OFF-specific SQL guardrails
```

Edit `RULES.md` if you want stricter agent behaviour. Re-run `nao sync` after
rebuilding the DuckDB (schema fingerprint changes).

## 3. Sync and chat

```bash
cd session6/nao-workspace
export ANTHROPIC_API_KEY=sk-ant-...
uv run nao sync       # profiles columns (uses Anthropic credits)
uv run nao chat
```

After each answer, open **View SQL** before trusting the chart — *the SQL is
the lesson*.

## Suggested prompts

### Prompt 1 — baseline
> *"How many products do we have per country? Show the top 10."*

Expected SQL ≈ `SELECT countries_en, COUNT(*) … GROUP BY 1 ORDER BY 2 DESC LIMIT 10`.

### Prompt 2 — filter + distribution
> *"What is the NutriScore distribution for products from France?"*

Check grade ordering on the X-axis — alphabetical A→E vs sorted by count matters.

### Prompt 3 — trap (ordinal as interval)
> *"What's the average NutriScore for ultra-processed foods?"*

Watch for `AVG(nutriscore_grade)` or silent A=1..E=5 mapping. Either is a
verification failure — read the SQL aloud.

### Prompt 4 — silent truncation
> *"What category has the most grade-A products?"*

Check `WHERE nutriscore_grade IS NOT NULL` and `pnns_groups_1 <> 'unknown'`.
If `unknown` tops the chart, the answer is meaningless.

## Verification checklist

Before trusting any AI-generated chart:

1. Read the SQL.
2. Check row counts against an independent query.
3. Eyeball the first 5 rows of the result.
4. If the answer is a single number, ask “compared to what?”

## Without Nao

Open `off_dashboard_queries.py`, read `query_category_nutri_score()` aloud, and
ask what changes if you forget `<> 'unknown'` or A–E filtering — same
verification point, no API key.

## Gotchas

- Rebuild DuckDB → must `nao sync` again before `nao chat`
- `nao sync` triggers per-column profiling calls — costs Anthropic credits
- Do not point Streamlit and Nao at the same `off.duckdb` file simultaneously
  (DuckDB file lock)

## Links

- [nao docs](https://docs.getnao.io/)
- [nao_config.yaml reference](https://docs.getnao.io/nao-agent/context-builder/configuration#nao_config-yaml)
