#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")/.."

ZIP="BoziDockCat.zip"
APP_NAME="BoziDockCat.app"
TARGET="${1:-$HOME/Applications}"

if [[ ! -f "$ZIP" ]]; then
  ./scripts/package_bozi_release.sh
fi

STAGE="$(mktemp -d "${TMPDIR:-/tmp}/bozidockcat-install.XXXXXX")"
trap 'rm -rf "$STAGE"' EXIT
unzip -q "$ZIP" -d "$STAGE"

mkdir -p "$TARGET"
rm -rf "$TARGET/$APP_NAME"
ditto "$STAGE/DockCat.app" "$TARGET/$APP_NAME"

# Seed first-run settings (JSON blob stored by DockCat).
python3 - <<'PY'
import json
import plistlib
from pathlib import Path

settings = {
    "language": "chinese",
    "catName": "波子",
    "catIdentifier": "Bozi",
    "userSalutation": "妈妈",
    "selectedAssetPackID": "default-lizz",
    "remindersEnabled": True,
    "waterReminderInterval": 1800,
    "waterReminderMessageSuffix": "该喝水啦",
    "movementReminderInterval": 3600,
    "movementReminderMessageSuffix": "该起来走走啦",
    "customReminderEnabled": False,
    "customReminderInterval": 1800,
    "customReminderMessageSuffix": "休息一下吧",
    "outingDepartureMessageSuffix": "工作要加油呀！",
    "defaultOutingDuration": 1500,
    "restDurationMinimum": 120,
    "restDurationMaximum": 300,
    "walkDurationMinimum": 120,
    "walkDurationMaximum": 300,
    "walkBaseSpeed": 36,
    "catScalePercent": 15,
    "startPositionPercent": 75,
    "catActivityScope": "dockEdge",
}
plist_path = Path.home() / "Library/Preferences/com.tianmaizhang.DockCat.plist"
plist = {}
if plist_path.exists():
    with plist_path.open("rb") as handle:
        plist = plistlib.load(handle)
plist["DockCat.AppSettings.v1"] = json.dumps(settings).encode("utf-8")
with plist_path.open("wb") as handle:
    plistlib.dump(plist, handle)
PY

xattr -dr com.apple.quarantine "$TARGET/$APP_NAME" 2>/dev/null || true
open "$TARGET/$APP_NAME"
echo "Installed to $TARGET/$APP_NAME"
