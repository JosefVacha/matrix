# Running the CI watcher as a background service (optional)

This document shows an example `systemd` unit you can use to run the opt-in CI watcher in the background on a maintainer machine.

Important: This is opt-in and for maintainers only. The watcher can optionally auto-notify; ensure secrets and tokens are set appropriately before enabling auto-notify.

Example unit (copy to `/etc/systemd/system/matrix-watch-pr.service`):

```
[Unit]
Description=Matrix PR CI Watcher
After=network.target

[Service]
Type=simple
User=matrix
WorkingDirectory=/home/matrix/MATRIX
ExecStart=/bin/bash -lc '/home/matrix/MATRIX/scripts/qa/watch_pr_ci_polling.sh main --interval 60'
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Enable and start:

```
sudo systemctl daemon-reload
sudo systemctl enable --now matrix-watch-pr.service
```

Notes:
- Set `ExecStart` to the appropriate path and branch/PR you want to watch.
- If using `--auto-notify`, make sure the environment has the required secrets (e.g., `SLACK_WEBHOOK`, `AUTOMATION_GH_TOKEN`) and that you trust automatic notifications.
- The watcher writes artifacts into `outputs/ci-artifacts` under the repo working directory; rotate or clean these periodically.
