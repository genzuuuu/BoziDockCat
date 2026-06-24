#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")/.."
export COPYFILE_DISABLE=1

PROJECT="DockCatApp/DockCat.xcodeproj"
SCHEME="DockCat"
CONFIGURATION="Release"
DERIVED_DATA="DockCatApp/DerivedDataRelease"
APP_PATH="$DERIVED_DATA/Build/Products/$CONFIGURATION/DockCat.app"
SOURCE_ZIP="DockCat.zip"
ZIP_PATH="BoziDockCat.zip"
BOZI_ASSETS="DockCatApp/DockCat/Resources/DefaultCat"
BOZI_ICONS="DockCatApp/DockCat/Resources/AppIcon"

build_from_source() {
  echo "Building BoziDockCat from source..." >&2
  xcodebuild \
    -project "$PROJECT" \
    -scheme "$SCHEME" \
    -configuration "$CONFIGURATION" \
    -derivedDataPath "$DERIVED_DATA" \
    ONLY_ACTIVE_ARCH=NO \
    ARCHS="arm64 x86_64" \
    clean build >&2
  [[ -d "$APP_PATH" ]] || { echo "Missing $APP_PATH" >&2; exit 1; }
  echo "$APP_PATH"
}

patch_official_app() {
  local stage="$1"
  local app="$stage/DockCat.app"
  echo "Patching official DockCat.app with Bozi assets..." >&2
  rm -rf "$app/Contents/Resources/DefaultCat"
  ditto "$BOZI_ASSETS" "$app/Contents/Resources/DefaultCat"
  ditto "$BOZI_ICONS/icon_sleep.png" "$app/Contents/Resources/AppIcon/icon_sleep.png"
  ditto "$BOZI_ICONS/icon_empty.png" "$app/Contents/Resources/AppIcon/icon_empty.png"
  python3 scripts/make_app_icon_icns.py "$BOZI_ICONS/icon_sleep.png" "$app/Contents/Resources/AppIcon.icns"
}

resolve_app_path() {
  if xcodebuild -version >/dev/null 2>&1; then
    build_from_source
    return
  fi
  echo "Xcode not available; packaging patched official DockCat release." >&2
  [[ -f "$SOURCE_ZIP" ]] || {
    echo "Missing $SOURCE_ZIP. Download DockCat release or install Xcode." >&2
    exit 1
  }
  local stage
  stage="$(mktemp -d "${TMPDIR:-/tmp}/bozidockcat.XXXXXX")"
  unzip -q "$SOURCE_ZIP" -d "$stage"
  patch_official_app "$stage"
  echo "$stage/DockCat.app"
}

package_release() {
  local app_path="$1"
  local stage
  stage="$(mktemp -d "${TMPDIR:-/tmp}/bozidockcat-package.XXXXXX")"

  ditto --norsrc "$app_path" "$stage/DockCat.app"
  cp README.md "$stage/README.md"
  cp README.en.md "$stage/README.en.md"
  cp LICENSE.txt "$stage/LICENSE.txt"
  mkdir -p "$stage/CustomizationGuide"
  cp -R CustomizationGuide/. "$stage/CustomizationGuide/"

  rm -f "$ZIP_PATH"
  ditto -c -k --norsrc "$stage" "$ZIP_PATH"
  rm -rf "$stage"
  echo "Created $(pwd)/$ZIP_PATH"
}

APP_PATH="$(resolve_app_path)"
package_release "$APP_PATH"
