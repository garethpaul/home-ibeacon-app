#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs/plans/2026-06-08-ios-privacy-baseline.md"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def strip_swift_line_comments(text):
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


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
        "HomeBeacon/LoginViewController.swift",
        "HomeBeacon/ViewController.swift",
        "HomeBeacon/HomeBeacon/Info.plist",
        "HomeBeacon/HomeBeacon/AppDelegate.swift",
        "HomeBeacon/HomeBeaconTests/HomeBeaconTests.swift",
        "HomeBeaconTests/HomeBeaconTests.swift",
        "Fabric.framework/Fabric",
        "TwitterKit.framework/TwitterKit",
        "docs/plans/2026-06-08-ios-privacy-baseline.md",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    podfile = read("Podfile")
    podlock = read("Podfile.lock")
    project = read("HomeBeacon.xcodeproj/project.pbxproj")
    login = read("HomeBeacon/LoginViewController.swift")
    app_delegate = read("HomeBeacon/AppDelegate.swift")
    nested_app_delegate = read("HomeBeacon/HomeBeacon/AppDelegate.swift")
    active_login = strip_swift_line_comments(login)
    active_app_delegate = strip_swift_line_comments(app_delegate)
    plan = PLAN.read_text(encoding="utf-8") if PLAN.exists() else ""

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
    require("make check" in readme and "FABRIC_API_KEY" in readme and "HomeBeacon.xcworkspace" in readme,
            "README must document static verification, local credentials, and workspace usage",
            failures)
    require("scripts/check-baseline.py" in vision and "credential" in vision.lower(),
            "VISION must describe the privacy baseline and credential guardrails",
            failures)
    require("FABRIC_API_KEY" in security and "TWITTER_CONSUMER_SECRET" in security,
            "SECURITY must document local Fabric/Twitter credential settings",
            failures)
    require("credential" in changes.lower() and "phone-number" in changes and "payload" in changes,
            "CHANGES must record the credential and phone-number payload cleanup",
            failures)
    require("status: completed" in plan,
            "plan must be marked completed",
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
