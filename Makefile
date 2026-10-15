.PHONY: check harness-smoke cmind-preflight cmind-codex-smoke cmind-codex-live cmind-rpg-init cmind-rpg-phase1 cmind-rpg-skeleton cmind-rpg-status cmind-rpg-export cmind-rpg-audit

check:
	python3 tools/check_repository.py

harness-smoke:
	bash tools/harness_smoke.sh

cmind-preflight:
	bash tools/cmind_preflight.sh

# Explicit isolated Codex PR #96 compatibility probe (no model calls).
cmind-codex-smoke:
	bash tools/cmind_codex_pr96_smoke.sh

# Explicit: one live model invocation; never part of CI.
cmind-codex-live:
	bash tools/cmind_codex_live_probe.sh

# Staged, explicit synthetic forward-RPG pipeline. phase1 and skeleton invoke the model.
cmind-rpg-init:
	bash tools/cmind_synthetic_rpg.sh init

cmind-rpg-phase1:
	bash tools/cmind_synthetic_rpg.sh phase1

cmind-rpg-skeleton:
	bash tools/cmind_synthetic_rpg.sh skeleton

cmind-rpg-status:
	bash tools/cmind_synthetic_rpg.sh status

cmind-rpg-export:
	bash tools/cmind_synthetic_rpg.sh export

# Read-only independent graph structure audit, after explicit artifact export.
RPG_AUDIT_DIR ?= experiments/runs/rpg-synthetic-v1
cmind-rpg-audit:
	@python3 tools/audit_synthetic_rpg.py "$(RPG_AUDIT_DIR)"
