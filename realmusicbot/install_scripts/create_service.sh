#!/bin/sh
SYSTEMD_SCRIPT_DIR=$( cd  $(dirname "${BASH_SOURCE:=$0}") && pwd)
cp -f "$SYSTEMD_SCRIPT_DIR/realmusicbot.service" ~/.config/systemd/user

systemctl --user daemon-reload
