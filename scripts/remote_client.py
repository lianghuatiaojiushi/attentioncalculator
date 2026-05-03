#!/usr/bin/env python3
"""
Thin client for the hosted 注意力计算器 service.

This script contains no proof-search logic and no coefficient tables. It only
submits user parameters to the hosted API and prints the returned LaTeX proof.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request


def post_form(base_url: str, path: str, data: dict[str, str]) -> dict:
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/")),
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_json(base_url: str, path: str, params: dict[str, str]) -> dict:
    url = urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    url = url + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Call the remote 注意力计算器 API.")
    parser.add_argument("--base-url", default="https://zhuyidao.net")
    parser.add_argument("--type", required=True)
    parser.add_argument("--power", required=True)
    parser.add_argument("--comparison", choices=[">", "<"], required=True)
    parser.add_argument("--rational", required=True)
    args = parser.parse_args()

    try:
        solution = post_form(
            args.base_url,
            "/calculate",
            {
                "type": args.type,
                "power": args.power,
                "comparison": args.comparison,
                "rational": args.rational,
            },
        )
        if not solution.get("success"):
            print(json.dumps(solution, ensure_ascii=False, indent=2))
            return 1

        params = dict(solution["parameters"])
        params.update(
            {
                "type": args.type,
                "coef": args.power,
                "comparison": args.comparison,
                "rational": args.rational,
            }
        )
        rendered = get_json(args.base_url, "/get_integral_image", params)
        print(rendered.get("equation", ""))
        return 0
    except Exception as exc:
        print(f"远程注意力计算器服务暂时不可用，请稍后再试。({exc})", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

