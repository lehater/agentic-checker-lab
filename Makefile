.PHONY: semantic-test harness-pack-preflight harness-consumer-preflight check harness-smoke cmind-preflight cmind-codex-smoke cmind-codex-live cmind-rpg-init cmind-rpg-phase1 cmind-rpg-skeleton cmind-rpg-status cmind-rpg-export cmind-rpg-audit architecture-test telemetry-test

check:
	python3 tools/check_repository.py
	python3 -m unittest discover -s tests -p 'test_architecture_policy.py' -v
	python3 -m unittest discover -s tests -p 'test_run_observability.py' -v
	python3 -m unittest discover -s tests -p 'test_semantic_review.py' -v

architecture-test:
	python3 -m unittest discover -s tests -p 'test_architecture_policy.py' -v

telemetry-test:
	python3 -m unittest discover -s tests -p 'test_run_observability.py' -v

# Historical Harness smoke: not part of the current engineering method.
harness-smoke:
	bash tools/harness_smoke.sh

cmind-preflight:
	bash tools/cmind_preflight.sh

cmind-codex-smoke:
	bash tools/cmind_codex_pr96_smoke.sh

cmind-codex-live:
	bash tools/cmind_codex_live_probe.sh

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

RPG_AUDIT_DIR ?= experiments/runs/rpg-synthetic-v1
cmind-rpg-audit:
	@python3 tools/audit_synthetic_rpg.py "$(RPG_AUDIT_DIR)"

harness-consumer-preflight:
	@bash tools/harness_consumer_preflight.sh

harness-pack-preflight:
	@bash tools/harness_pack_preflight.sh

semantic-test:
	python3 -m unittest discover -s tests -p 'test_semantic_review.py' -v
