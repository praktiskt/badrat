generate:
	uv run baml-cli generate --from=src

dev-fastapi:
	cd src && uv run fastapi dev

dev-baml:
	uv run baml-cli dev --from=src --preview
