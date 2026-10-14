"""Command-Line Interface for laya-sidecar."""

import sys
import argparse
import json
from laya_agy_sidecar.engine import LayaEngine
from laya_agy_sidecar.guardrail import CommandGuardrail
from laya_agy_sidecar.router import SwarmRouter
from laya_agy_sidecar.secret_scanner import SecretScanner


def main():
    parser = argparse.ArgumentParser(
        prog="laya-sidecar",
        description="System 1 Non-Autoregressive Decision Sidecar for Antigravity (agy)",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # 1. Guardrail subcommand
    guard_parser = subparsers.add_parser("guardrail", help="Evaluate bash command safety")
    guard_parser.add_argument("command", help="The command line string to evaluate")
    guard_parser.add_argument("--json", action="store_true", help="Output JSON result")

    # 2. Route subcommand
    route_parser = subparsers.add_parser("route", help="Route prompt to subagent and model tier")
    route_parser.add_argument("prompt", help="The user prompt to analyze")
    route_parser.add_argument("--json", action="store_true", help="Output JSON result")

    # 3. Scan secrets subcommand
    scan_parser = subparsers.add_parser("scan", help="Scan text for exposed secrets")
    scan_parser.add_argument("text", help="Text or payload to scan")
    scan_parser.add_argument("--json", action="store_true", help="Output JSON result")

    # 4. Generic decide subcommand
    decide_parser = subparsers.add_parser("decide", help="Make a non-autoregressive decision")
    decide_parser.add_argument("--state", required=True, help="Input state context")
    decide_parser.add_argument("--question", required=True, help="Typed question to evaluate")
    decide_parser.add_argument("--choices", nargs="+", help="Candidate choices (for choice primitive)")
    decide_parser.add_argument("--boolean", action="store_true", help="Evaluate boolean noul primitive")

    args = parser.parse_args()

    engine = LayaEngine()

    if args.subcommand == "guardrail":
        guard = CommandGuardrail(engine)
        res = guard.evaluate(args.command)
        if args.json:
            print(res.model_dump_json(indent=2))
        else:
            status_icon = "✅" if res.is_safe else "🛑"
            print(f"{status_icon} Action: {res.recommended_action} | Risk: {res.risk_level} ({res.latency_ms}ms)")
            for r in res.reasons:
                print(f"   • {r}")
        sys.exit(0 if res.is_safe else (2 if res.risk_level == "CRITICAL" else 1))

    elif args.subcommand == "route":
        router = SwarmRouter(engine)
        res = router.dispatch(args.prompt)
        if args.json:
            print(res.model_dump_json(indent=2))
        else:
            print(f"🎯 Target Subagent: {res.target_subagent}")
            print(f"✂️  Ponytail Skill:  {res.recommended_ponytail_skill} (level: {res.ponytail_level or 'n/a'})")
            print(f"⚡ Suggested Cmd:   {res.suggested_command}")
            print(f"⏱️  Decision Time:  {res.latency_ms}ms")
        sys.exit(0)

    elif args.subcommand == "scan":
        scanner = SecretScanner()
        res = scanner.scan(args.text)
        if args.json:
            print(res.model_dump_json(indent=2))
        else:
            if res.contains_secrets:
                print(f"🚨 Found {res.leak_count} potential secrets ({res.latency_ms}ms):")
                for f in res.findings:
                    print(f"   • {f['type']}: {f['match']}")
            else:
                print(f"✅ Clean: No secrets detected ({res.latency_ms}ms)")
        sys.exit(1 if res.contains_secrets else 0)

    elif args.subcommand == "decide":
        if args.boolean:
            res = engine.noul(state=args.state, question=args.question)
            print(res.model_dump_json(indent=2))
        elif args.choices:
            res = engine.choice(state=args.state, question=args.question, choices=args.choices)
            print(res.model_dump_json(indent=2))
        else:
            res = engine.score(state=args.state, question=args.question)
            print(res.model_dump_json(indent=2))
        sys.exit(0)


if __name__ == "__main__":
    main()
