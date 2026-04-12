.PHONY: help run remote app

.DEFAULT_GOAL := help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

run: ## Open TouchOSC MTC Movie Slate layout
	open mtc-movie-slate.tosc

remote: ## Start MTC Remote Control (production metadata GUI)
	cd mtc-remote-control && ./start.sh

app: ## Build PyInstaller app (macOS .app bundle)
	cd mtc-remote-control && pyinstaller --name 'MTC Remote Control' \
		--windowed src/mtc_remote_control/main.py
