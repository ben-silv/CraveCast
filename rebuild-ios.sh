#!/usr/bin/env bash
# Rebuild the CraveCast iOS app. Runs on macOS only -- Xcode and CocoaPods
# have no Windows equivalent, so this is the one step that cannot happen on
# the machine the rest of the project is developed on.
#
#   ./rebuild-ios.sh            build web assets, sync, open Xcode
#   ./rebuild-ios.sh --archive  also archive to build/CraveCast.xcarchive
#
# Expects the repo checked out next to a Capacitor project laid out the same
# way as the Windows one. Override either path with TRACKER= / APP=.
set -euo pipefail

TRACKER="${TRACKER:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
APP="${APP:-$HOME/CraveCastApp}"

echo "==> web assets"
python3 "$TRACKER/build-native.py"

echo "==> capacitor"
cd "$APP"
[ -d ios ] || npx cap add ios
npx cap sync ios

if [ "${1:-}" = "--archive" ]; then
  echo "==> archive"
  cd "$APP/ios/App"
  xcodebuild -workspace App.xcworkspace -scheme App \
             -configuration Release -destination "generic/platform=iOS" \
             -archivePath "$APP/build/CraveCast.xcarchive" archive
  echo "archive at $APP/build/CraveCast.xcarchive"
  echo "open it in Xcode > Window > Organizer to validate and upload"
else
  npx cap open ios
fi
