.PHONY: app
app:
	cd mtc-remote-control && pyinstaller --name 'MTC Remote Control' \
		--windowed src/mtc_remote_control/main.py

.PHONY: remote
remote:
	cd mtc-remote-control && ./start.sh

.PHONY: run
run:
	open mtc-movie-slate.tosc
