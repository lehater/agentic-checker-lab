.PHONY: check harness-smoke

check:
	python3 tools/check_repository.py

# Optional explicit network/tooling operation; never run as part of documentation CI.
harness-smoke:
	bash tools/harness_smoke.sh
