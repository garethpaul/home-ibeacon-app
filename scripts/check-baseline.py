#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-ios-privacy-baseline.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
NOTIFICATION_PLAN = ROOT / "docs/plans/2026-06-09-location-notification-privacy.md"
NOTIFICATION_PERMISSION_PLAN = ROOT / "docs/plans/2026-06-09-location-notification-permission.md"
NOTIFICATION_CODE_PLAN = ROOT / "docs/plans/2026-06-09-location-notification-code-removal.md"
LOCATION_STATE_PLAN = ROOT / "docs/plans/2026-06-09-location-state-memory-retention.md"
VIEW_STATE_PLAN = ROOT / "docs/plans/2026-06-09-stale-view-location-state.md"
BEACON_REGION_PLAN = ROOT / "docs/plans/2026-06-09-beacon-region-cast-guard.md"
BEACON_PAYLOAD_PLAN = ROOT / "docs/plans/2026-06-09-beacon-payload-cast-guard.md"
MODERNIZATION_PLAN = ROOT / "docs/plans/2026-06-10-legacy-sdk-modernization-boundary.md"
CI_PLAN = ROOT / "docs/plans/2026-06-10-hosted-project-validation.md"
STANDARD_LOCATION_PLAN = ROOT / "docs/plans/2026-06-10-standard-location-update-removal.md"
WORKFLOW_INTEGRITY_PLAN = ROOT / "docs/plans/2026-06-12-hosted-workflow-integrity.md"
REGION_RANGING_PLAN = ROOT / "docs/plans/2026-06-12-region-scoped-beacon-ranging.md"
EXPECTED_WORKFLOW = """name: Check

on:
  pull_request:
  push:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  check:
    runs-on: macos-15
    timeout-minutes: 10
    steps:
      - name: Check out repository
        uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10 # v6.0.3
        with:
          persist-credentials: false
      - name: Run privacy and project baseline
        run: make check
"""
EXPECTED_MAKEFILE = """.PHONY: build check lint test

lint test build: check

check:
\tpython3 scripts/check-baseline.py
"""


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def strip_swift_line_comments(text):
    stripped_lines = []
    for line in text.splitlines():
        output = []
        in_string = False
        escaped = False
        index = 0
        while index < len(line):
            character = line[index]
            if not in_string and character == "/" and index + 1 < len(line) and line[index + 1] == "/":
                break
            output.append(character)
            if character == '"' and not escaped:
                in_string = not in_string
            if character == "\\":
                escaped = not escaped
            else:
                escaped = False
            index += 1
        stripped_lines.append("".join(output))
    return "\n".join(stripped_lines)


def active_notification_calls(text):
    calls = []
    for line in text.splitlines():
        stripped = line.strip()
        if "sendLocalNotificationWithMessage(" in stripped and not stripped.startswith("func "):
            calls.append(stripped)
    return calls


def parse_plist(relative_path, failures):
    path = ROOT / relative_path
    try:
        with path.open("rb") as file:
            return plistlib.load(file)
    except Exception as error:
        failures.append(f"{relative_path} is not a readable plist: {error}")
        return {}


def parse_xml(relative_path, failures):
    try:
        ET.parse(str(ROOT / relative_path))
    except ET.ParseError as error:
        failures.append(f"{relative_path} is not well-formed XML: {error}")


def main():
    failures = []
    swift_comment_fixture = 'let endpoint = "http://example.com/path" // trailing comment'
    require(strip_swift_line_comments(swift_comment_fixture) ==
            'let endpoint = "http://example.com/path" ',
            "Swift comment stripping must preserve quoted URL strings",
            failures)
    required_files = [
        ".gitignore",
        ".github/workflows/check.yml",
        "CHANGES.md",
        "Makefile",
        "Podfile",
        "Podfile.lock",
        "Pods/Manifest.lock",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "HomeBeacon.xcworkspace/contents.xcworkspacedata",
        "HomeBeacon.xcodeproj/project.pbxproj",
        "HomeBeacon/Info.plist",
        "HomeBeacon/AppDelegate.swift",
        "HomeBeacon/Hex.swift",
        "HomeBeacon/LoginViewController.swift",
        "HomeBeacon/ViewController.swift",
        "HomeBeacon/HomeBeacon/Info.plist",
        "HomeBeacon/HomeBeacon/AppDelegate.swift",
        "HomeBeacon/HomeBeaconTests/HomeBeaconTests.swift",
        "HomeBeaconTests/HomeBeaconTests.swift",
        "Fabric.framework/Fabric",
        "TwitterKit.framework/TwitterKit",
        "docs/plans/2026-06-08-ios-privacy-baseline.md",
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-08-location-log-privacy.md",
        "docs/plans/2026-06-08-hex-parser-invalid-input.md",
        "docs/plans/2026-06-09-location-notification-privacy.md",
        "docs/plans/2026-06-09-location-notification-permission.md",
        "docs/plans/2026-06-09-location-notification-code-removal.md",
        "docs/plans/2026-06-09-location-state-memory-retention.md",
        "docs/plans/2026-06-09-stale-view-location-state.md",
        "docs/plans/2026-06-09-beacon-region-cast-guard.md",
        "docs/plans/2026-06-09-beacon-payload-cast-guard.md",
        "docs/plans/2026-06-10-legacy-sdk-modernization-boundary.md",
        "docs/plans/2026-06-10-hosted-project-validation.md",
        "docs/plans/2026-06-10-standard-location-update-removal.md",
        "docs/plans/2026-06-12-hosted-workflow-integrity.md",
        "docs/plans/2026-06-12-region-scoped-beacon-ranging.md",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    makefile = read("Makefile")
    podfile = read("Podfile")
    podlock = read("Podfile.lock")
    project = read("HomeBeacon.xcodeproj/project.pbxproj")
    hex_source = read("HomeBeacon/Hex.swift")
    login = read("HomeBeacon/LoginViewController.swift")
    app_delegate = read("HomeBeacon/AppDelegate.swift")
    nested_app_delegate = read("HomeBeacon/HomeBeacon/AppDelegate.swift")
    view_controller = read("HomeBeacon/ViewController.swift")
    active_login = strip_swift_line_comments(login)
    active_app_delegate = strip_swift_line_comments(app_delegate)
    active_delegates = strip_swift_line_comments(app_delegate + "\n" + nested_app_delegate)
    active_view_controller = strip_swift_line_comments(view_controller)
    plan = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""
    make_gates_plan = MAKE_GATES_PLAN.read_text(encoding="utf-8") if MAKE_GATES_PLAN.exists() else ""
    log_plan = read("docs/plans/2026-06-08-location-log-privacy.md")
    hex_plan = read("docs/plans/2026-06-08-hex-parser-invalid-input.md")
    notification_plan = NOTIFICATION_PLAN.read_text(encoding="utf-8") if NOTIFICATION_PLAN.exists() else ""
    notification_permission_plan = NOTIFICATION_PERMISSION_PLAN.read_text(encoding="utf-8") if NOTIFICATION_PERMISSION_PLAN.exists() else ""
    notification_code_plan = NOTIFICATION_CODE_PLAN.read_text(encoding="utf-8") if NOTIFICATION_CODE_PLAN.exists() else ""
    location_state_plan = LOCATION_STATE_PLAN.read_text(encoding="utf-8") if LOCATION_STATE_PLAN.exists() else ""
    view_state_plan = VIEW_STATE_PLAN.read_text(encoding="utf-8") if VIEW_STATE_PLAN.exists() else ""
    beacon_region_plan = BEACON_REGION_PLAN.read_text(encoding="utf-8") if BEACON_REGION_PLAN.exists() else ""
    beacon_payload_plan = BEACON_PAYLOAD_PLAN.read_text(encoding="utf-8") if BEACON_PAYLOAD_PLAN.exists() else ""
    modernization_plan = MODERNIZATION_PLAN.read_text(encoding="utf-8") if MODERNIZATION_PLAN.exists() else ""
    standard_location_plan = STANDARD_LOCATION_PLAN.read_text(encoding="utf-8") if STANDARD_LOCATION_PLAN.exists() else ""
    workflow_integrity_plan = WORKFLOW_INTEGRITY_PLAN.read_text(encoding="utf-8") if WORKFLOW_INTEGRITY_PLAN.exists() else ""
    region_ranging_plan = REGION_RANGING_PLAN.read_text(encoding="utf-8") if REGION_RANGING_PLAN.exists() else ""

    for xml_file in [
        "HomeBeacon.xcworkspace/contents.xcworkspacedata",
        "HomeBeacon.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "HomeBeacon/Base.lproj/Main.storyboard",
        "HomeBeacon/Base.lproj/LaunchScreen.xib",
        "docs/readme-overview.svg",
    ]:
        parse_xml(xml_file, failures)

    app_plist = parse_plist("HomeBeacon/Info.plist", failures)
    nested_plist = parse_plist("HomeBeacon/HomeBeacon/Info.plist", failures)
    fabric = app_plist.get("Fabric", {})
    kits = fabric.get("Kits", [{}])
    kit_info = kits[0].get("KitInfo", {}) if kits else {}

    require(fabric.get("APIKey") == "$(FABRIC_API_KEY)",
            "HomeBeacon/Info.plist must use FABRIC_API_KEY instead of a checked-in Fabric API key",
            failures)
    require(kit_info.get("consumerKey") == "$(TWITTER_CONSUMER_KEY)",
            "HomeBeacon/Info.plist must use TWITTER_CONSUMER_KEY instead of a checked-in Twitter key",
            failures)
    require(kit_info.get("consumerSecret") == "$(TWITTER_CONSUMER_SECRET)",
            "HomeBeacon/Info.plist must use TWITTER_CONSUMER_SECRET instead of a checked-in Twitter secret",
            failures)
    require("FABRIC_API_KEY" in project and "FABRIC_BUILD_SECRET" in project,
            "Fabric build phase must use local build-setting placeholders",
            failures)
    fabric_phase = re.search(r"7F0B88C81AEDF5E800E9DE40 /\* ShellScript \*/ = \{(?P<body>.*?)\n\t\t\};", project, re.DOTALL)
    require(fabric_phase is not None and "showEnvVarsInLog = 0;" in fabric_phase.group("body"),
            "Fabric build phase must suppress environment variable logging",
            failures)
    require(not re.search(r"Fabric\.framework/run\s+[A-Za-z0-9]{20,}\s+[A-Za-z0-9]{20,}", project),
            "Fabric build phase must not include literal API key or build secret arguments",
            failures)

    first_party = "\n".join([
        read("HomeBeacon/Info.plist"),
        project,
        login,
        app_delegate,
        nested_app_delegate,
    ])
    require("consumerSecret</key>\n\t\t\t\t\t<string>$(" in first_party,
            "Twitter consumer secret must remain a build-setting placeholder",
            failures)
    require(not re.search(r"print(?:ln)?\s*\([^)]*(phoneNumber|userID|session)[^)]*\)", active_login),
            "Login flow must not print session, phone number, or user ID values",
            failures)
    require("phoneNumber" not in active_app_delegate and "userID" not in active_app_delegate,
            "Beacon region handlers must not assemble phone-number or Digits user ID payloads while reporting is disabled",
            failures)
    require("Alamofire.request(.POST" not in active_app_delegate,
            "Beacon home/away POST must stay disabled until endpoint and consent are documented",
            failures)
    require("http://" not in active_app_delegate,
            "Active first-party Swift code must not use plain HTTP endpoints",
            failures)
    require("NSLog" not in active_delegates,
            "Beacon region handlers must not write home/away or proximity state to device logs",
            failures)
    require("currentLocation" not in active_delegates and
            "var message:String" not in active_delegates and
            "playSound" not in active_delegates,
            "Beacon region handlers must not retain unused home/away state or notification payload strings",
            failures)
    require("appDelegate.currentLocation" not in active_view_controller and
            "UIApplication.sharedApplication().delegate as! AppDelegate" not in active_view_controller,
            "Top-level status UI must not read removed AppDelegate currentLocation state",
            failures)
    for location_phrase in [
        "You are far away from the beacon",
        "You are near the beacon",
        "You are in the immediate proximity of the beacon",
        "No beacons are nearby",
    ]:
        require(location_phrase not in active_delegates,
                f"Beacon region handlers must not retain unused occupancy text: {location_phrase}",
                failures)
    require(not active_notification_calls(active_delegates),
            "Beacon region handlers must not display home/away or proximity state in local notifications",
            failures)
    require("UILocalNotification" not in active_delegates and
            "scheduleLocalNotification" not in active_delegates and
            "sendLocalNotificationWithMessage" not in active_delegates,
            "App delegates must not retain local notification scheduling code while beacon-state notifications are disabled",
            failures)
    require("sendLocalNotificationWithMessage" not in app_delegate + nested_app_delegate,
            "App delegates must not retain commented local notification call sites",
            failures)
    require("registerUserNotificationSettings" not in active_delegates and "UIUserNotificationSettings" not in active_delegates,
            "App delegates must not request local notification permission while beacon-state notifications are disabled",
            failures)
    require("region as! CLBeaconRegion" not in active_delegates and
            active_delegates.count("if let beaconRegion = region as? CLBeaconRegion") >= 4,
            "App delegates must guard CLRegion values before calling beacon-only ranging APIs",
            failures)
    require("as! CLBeacon" not in active_delegates and
            "as! [CLBeacon]" not in active_delegates and
            "as! ViewController" not in active_delegates,
            "App delegates must not force-cast ranged beacon payloads or status view controllers",
            failures)
    require(len(re.findall(r"as\?\s+CLBeacon(?!Region)", active_delegates)) >= 2 and
            "as? [CLBeacon]" in active_delegates and
            "as? ViewController" in active_delegates,
            "App delegates must optional-cast ranged beacon payloads and status view controllers",
            failures)
    require("startUpdatingLocation" not in active_delegates and
            "stopUpdatingLocation" not in active_delegates and
            "pausesLocationUpdatesAutomatically" not in active_delegates,
            "Beacon-only delegates must not start continuous standard location updates",
            failures)
    require(active_delegates.count("startMonitoringForRegion(beaconRegion)") == 2 and
            active_delegates.count("startRangingBeaconsInRegion(beaconRegion)") == 2 and
            active_delegates.count("stopRangingBeaconsInRegion(beaconRegion)") == 2,
            "App delegates must monitor at launch and range only between region entry and exit",
            failures)
    require("let scanner = NSScanner(string: cString)" in hex_source and
            "scanner.scanHexInt(&rgbValue)" in hex_source and
            "scanner.atEnd" in hex_source and
            "return UIColor.grayColor()" in hex_source,
            "Hex color parser must reject partially scanned invalid hex strings with the gray fallback",
            failures)

    for plist_name, plist in [
        ("HomeBeacon/Info.plist", app_plist),
        ("HomeBeacon/HomeBeacon/Info.plist", nested_plist),
    ]:
        require(plist.get("NSLocationAlwaysUsageDescription"),
                f"{plist_name} must explain always-on location access",
                failures)
        require("location" in plist.get("UIBackgroundModes", []),
                f"{plist_name} must keep location background mode explicit",
                failures)

    require("platform :ios, '8.0'" in podfile and "pod 'Alamofire', '~> 1.2'" in podfile,
            "Podfile must preserve the legacy iOS 8 Alamofire dependency contract",
            failures)
    require("Alamofire (1.2.1)" in podlock and "COCOAPODS: 0.37.0.beta.1" in podlock,
            "Podfile.lock must preserve the pinned legacy CocoaPods resolution",
            failures)
    require(read("Podfile.lock") == read("Pods/Manifest.lock"),
            "Pods/Manifest.lock must match Podfile.lock",
            failures)

    swift_files = sorted((ROOT / "HomeBeacon").rglob("*.swift")) + sorted((ROOT / "HomeBeaconTests").rglob("*.swift"))
    require(len(swift_files) >= 8,
            "expected legacy Swift source/test inventory is missing",
            failures)
    require("HomeBeacon.xcodeproj" in read("HomeBeacon.xcworkspace/contents.xcworkspacedata") and "Pods/Pods.xcodeproj" in read("HomeBeacon.xcworkspace/contents.xcworkspacedata"),
            "workspace must include the app project and CocoaPods project",
            failures)
    require("*.local.xcconfig" in gitignore and "*.secrets.xcconfig" in gitignore and ".env" in gitignore,
            ".gitignore must exclude local secret configuration files",
            failures)
    require(makefile == EXPECTED_MAKEFILE,
            "Makefile must exactly preserve the local baseline aliases",
            failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "FABRIC_API_KEY" in readme and "HomeBeacon.xcworkspace" in readme and "device logs" in readme and "local notifications" in readme and "notification permission" in readme and "notification scheduling" in readme and "memory-only location state" in readme and "stale status UI" in readme and "beacon-region casts" in readme and "beacon payload casts" in readme and "invalid hex" in readme.lower(),
            "README must document static verification, local credentials, and workspace usage",
            failures)
    require("scripts/check-baseline.py" in vision and "make lint" in vision and "make test" in vision and "make build" in vision and "credential" in vision.lower() and "logs" in vision.lower() and "local notifications" in vision.lower() and "notification permission" in vision and "notification scheduling" in vision and "memory-only location state" in vision and "stale status UI" in vision and "beacon-region casts" in vision and "beacon payload casts" in vision and "invalid hex" in vision.lower(),
            "VISION must describe the privacy baseline and credential guardrails",
            failures)
    require("FABRIC_API_KEY" in security and "TWITTER_CONSUMER_SECRET" in security,
            "SECURITY must document local Fabric/Twitter credential settings",
            failures)
    require("standard coordinate updates" in readme and
            "standard coordinate updates" in vision and
            "continuous standard coordinate" in security and
            "continuous standard location updates" in changes,
            "Docs must preserve the beacon-only location update boundary",
            failures)
    require("credential" in changes.lower() and "phone-number" in changes and "payload" in changes and "device logs" in changes and "local notifications" in changes and "notification permission" in changes and "notification scheduling" in changes and "memory-only location state" in changes and "stale status UI" in changes and "beacon-region casts" in changes and "beacon payload casts" in changes and "invalid hex" in changes.lower(),
            "CHANGES must record the credential and phone-number payload cleanup",
            failures)
    require("status: completed" in plan,
            "plan must be marked completed",
            failures)
    require("status: completed" in make_gates_plan,
            "make gate aliases plan must be marked completed",
            failures)
    require("status: completed" in log_plan,
            "location log privacy plan must be marked completed",
            failures)
    require("status: completed" in hex_plan,
            "hex parser invalid-input plan must be marked completed",
            failures)
    require("status: completed" in notification_plan,
            "location notification privacy plan must be marked completed",
            failures)
    require("status: completed" in notification_permission_plan,
            "location notification permission plan must be marked completed",
            failures)
    require("status: completed" in notification_code_plan,
            "location notification code-removal plan must be marked completed",
            failures)
    require("status: completed" in location_state_plan,
            "location state memory-retention plan must be marked completed",
            failures)
    require("status: completed" in view_state_plan,
            "stale view location-state plan must be marked completed",
            failures)
    require("status: completed" in beacon_region_plan,
            "beacon region cast guard plan must be marked completed",
            failures)
    require("status: completed" in beacon_payload_plan,
            "beacon payload cast guard plan must be marked completed",
            failures)
    require("Swift 1-era" in readme and "iOS 8.3" in readme and "Alamofire 1.2" in readme and "current SDK" in readme,
            "README must document the legacy SDK modernization boundary",
            failures)
    require("Swift 1-era" in vision and "Alamofire 1.2" in vision and "modernization" in vision.lower(),
            "VISION must document the legacy SDK modernization sequence",
            failures)
    require("retired" in security and "TwitterKit" in security and "current SDK" in security,
            "SECURITY must identify retired SDK and current-toolchain risk",
            failures)
    require("legacy SDK modernization boundary" in changes,
            "CHANGES must record the legacy SDK modernization boundary",
            failures)
    require("status: completed" in modernization_plan and "Swift 1-era" in modernization_plan and "Alamofire 1.2" in modernization_plan,
            "legacy SDK modernization boundary must be completed and version-specific",
            failures)
    require("status: completed" in standard_location_plan and "make check" in standard_location_plan,
            "standard location update removal plan must be completed and record verification",
            failures)

    ci_plan = CI_PLAN.read_text(errors="replace") if CI_PLAN.exists() else ""
    require("status: completed" in ci_plan and "make check" in ci_plan,
            "hosted project validation plan must be completed and record verification",
            failures)
    require("status: completed" in workflow_integrity_plan and
            "persist-credentials: false" in workflow_integrity_plan and
            "hostile mutations" in workflow_integrity_plan,
            "hosted workflow integrity plan must record its completed contract",
            failures)
    region_ranging_statuses = re.findall(
        r"^status: .+$", region_ranging_plan, flags=re.MULTILINE
    )
    region_ranging_sections = region_ranging_plan.split("## Verification Completed\n", 1)
    region_ranging_verification = (
        region_ranging_sections[1] if len(region_ranging_sections) == 2 else ""
    )
    region_ranging_required_evidence = (
        "All four Make gates",
        "push run `27394030821`",
        "pull-request run `27394033398`",
        "push run `27394057050`",
        "CodeQL setup run `27402322010`",
        "Mutations restoring launch-time `startRangingBeaconsInRegion`",
    )
    require(region_ranging_statuses == ["status: completed"]
            and all(item in region_ranging_verification for item in region_ranging_required_evidence)
            and re.search(r"\b(?:pending|todo|tbd|not run)\b", region_ranging_verification, re.IGNORECASE) is None,
            "region-scoped beacon ranging plan must record completed status and actual verification",
            failures)
    require("region-scoped beacon ranging" in readme.lower() and
            "region-scoped beacon ranging" in vision.lower() and
            "region-scoped beacon ranging" in security.lower() and
            "region-scoped beacon ranging" in changes.lower(),
            "Docs must preserve the region-scoped beacon ranging boundary",
            failures)
    workflow = read(".github/workflows/check.yml")
    require(workflow == EXPECTED_WORKFLOW,
            "GitHub Actions must exactly match the bounded, least-privilege macOS project check",
            failures)

    if shutil.which("xcodebuild"):
        result = subprocess.run(
            ["xcodebuild", "-list", "-project", "HomeBeacon.xcodeproj"],
            cwd=str(ROOT),
            stdout=subprocess.DEVNULL,
            check=False,
        )
        require(result.returncode == 0,
                "HomeBeacon.xcodeproj must parse with installed Xcode",
                failures)
    else:
        print("xcodebuild unavailable; static iOS baseline only.")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("home-ibeacon-app iOS privacy baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
