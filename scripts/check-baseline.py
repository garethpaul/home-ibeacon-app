#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
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


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def strip_swift_line_comments(text):
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


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
    required_files = [
        ".gitignore",
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
    require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile,
            "Makefile must expose lint, test, and build aliases for the local baseline",
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

    if shutil.which("xcodebuild"):
        print("xcodebuild is available; run a scheme-specific Xcode test on macOS before release.")
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
