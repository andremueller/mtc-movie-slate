.PHONY: help run remote app

.DEFAULT_GOAL := help

help: ## Diese Hilfe anzeigen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

run: ## TouchOSC MTC Movie Slate Layout öffnen
	open mtc-movie-slate.tosc

remote: ## MTC Remote Control starten (Produktions-Metadaten GUI)
	cd mtc-remote-control && ./start.sh

app: ## PyInstaller App bauen (macOS .app Bundle)
	cd mtc-remote-control && pyinstaller --name 'MTC Remote Control' \
		--windowed src/mtc_remote_control/main.py
