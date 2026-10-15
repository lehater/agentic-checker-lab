.PHONY: check harness-smoke cmind-preflight cmind-codex-smoke cmind-codex-live

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
