.PHONY: check harness-smoke cmind-preflight

check:
	python3 tools/check_repository.py

harness-smoke:
	bash tools/harness_smoke.sh

cmind-preflight:
	bash tools/cmind_preflight.sh
