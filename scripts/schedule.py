#!/usr/bin/env python3
"""NL cron setup — set up recurring content generation via cron or Hermes schedule."""

import argparse
import json
import os
import re
import sys

CONTENT_TYPES = [
    "instagram_caption",
    "email_subject",
    "blog_intro",
    "tweet",
    "linkedin_post",
]

_DAY_MAP: dict[str, str] = {
    "monday": "1",
    "tuesday": "2",
    "wednesday": "3",
    "thursday": "4",
    "friday": "5",
    "saturday": "6",
    "sunday": "0",
    "mon": "1",
    "tue": "2",
    "wed": "3",
    "thu": "4",
    "fri": "5",
    "sat": "6",
    "sun": "0",
}


def _parse_nl_to_cron(schedule: str) -> str | None:
    s = schedule.lower().strip()

    day = None
    for name, num in _DAY_MAP.items():
        if name in s:
            day = num
            break

    hour = "9"
    minute = "0"

    time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", s)
    if time_match:
        h = int(time_match.group(1))
        m = int(time_match.group(2)) if time_match.group(2) else 0
        ampm = time_match.group(3)
        if ampm == "pm" and h < 12:
            h += 12
        if ampm == "am" and h == 12:
            h = 0
        hour = str(h)
        minute = str(m)

    if day is None:
        if "daily" in s or "every day" in s:
            return f"{minute} {hour} * * *"
        return None

    return f"{minute} {hour} * * {day}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="NL cron setup — recurrent content generation"
    )
    parser.add_argument("--profile", required=True, help="Path to brand_profile.json")
    parser.add_argument(
        "--schedule",
        required=True,
        help='Natural language schedule (e.g. "every Monday at 9am")',
    )
    parser.add_argument(
        "--type",
        default="instagram_caption",
        choices=CONTENT_TYPES,
        help="Content type",
    )
    parser.add_argument(
        "--output-dir", default="./output", help="Directory for generated content"
    )
    args = parser.parse_args()

    profile_path = os.path.abspath(args.profile)
    if not os.path.exists(profile_path):
        print(f"ERROR: Profile not found: {profile_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    cron_expr = _parse_nl_to_cron(args.schedule)
    script_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "content.py",
    )

    cron_entry: str | None = None
    if cron_expr:
        cron_entry = (
            f"{cron_expr} python3 {script_path} "
            f'--profile "{profile_path}" --type {args.type} '
            f'--output-dir "{output_dir}"'
        )

    hermes_cron_config = {
        "schedule_nl": args.schedule,
        "cron_expression": cron_expr,
        "profile": profile_path,
        "content_type": args.type,
        "output_dir": output_dir,
        "command": f"python3 {script_path} --profile {profile_path} --type {args.type}",
    }

    hermes_config_path = os.path.join(output_dir, ".hermes_cron.json")
    with open(hermes_config_path, "w") as f:
        json.dump(hermes_cron_config, f, indent=2)
    print(f"[+] Hermes cron config: {hermes_config_path}")

    if cron_entry:
        print(f"\n=== Cron Entry ===")
        print(cron_entry)
        print(
            f"\nTo install: (crontab -l 2>/dev/null; echo '{cron_entry}') | crontab -"
        )
    else:
        print(
            f"\nWARNING: Could not parse cron expression from '{args.schedule}'",
            file=sys.stderr,
        )
        print("Hermes will handle scheduling via .hermes_cron.json instead.")


if __name__ == "__main__":
    main()
