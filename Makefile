

.PHONY: remote
remote:
	cd mtc-remote-control && poetry run python src/mtc_remote_control/main.py

.PHONY: run
run:
	open mtc-movie-slate.tosc
