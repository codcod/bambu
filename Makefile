.PHONY = venv lint test run

export PYTHONPATH=src/.

OUT_DIR := build

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

venv:
	rm -rf ".venv"
	rye sync
	@printf "\nDone. You can now activate the virtual environment:"
	@printf "\n  source .venv/bin/activate\n  virtualenv --upgrade-embed-wheels\n"

lint:
	rye run lint

test:
	rye run pytest

run:
	rye run app1

sbom:
	mkdir -p $(OUT_DIR)
	rye run python -m cyclonedx_py environment > build/cyclonedx.json
	curl -X POST http://localhost:8081/api/v1/bom \
		-H "Content-Type: multipart/form-data" \
		-H "X-API-Key: ${DT_API_KEY}" \
		-F "project=${DT_PROJECT}" \
		-F "bom=@$(OUT_DIR)/cyclonedx.json"