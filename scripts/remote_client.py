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
import urllib.error
import urllib.parse
import urllib.request


def flip_comparison(comparison: str) -> str:
    return "<" if comparison == ">" else ">"


def post_form(base_url: str, path: str, data: dict[str, str]) -> dict:
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/")),
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8"))
            if isinstance(payload, dict):
                payload["_http_status"] = exc.code
                return payload
        except Exception:
            pass
        raise


def get_json(base_url: str, path: str, params: dict[str, str]) -> dict:
    url = urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    url = url + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def is_direction_error(response: dict) -> bool:
    return "不等号方向反了" in str(response.get("error", ""))


def main() -> int:
    parser = argparse.ArgumentParser(description="Call the remote 注意力计算器 API.")
    parser.add_argument("--base-url", default="http://zhuyidao.net")
    parser.add_argument("--type", required=True)
    parser.add_argument("--power", required=True)
    parser.add_argument("--comparison", choices=[">", "<"], required=True)
    parser.add_argument("--rational", required=True)
    args = parser.parse_args()

    try:
        request_data = {
            "type": args.type,
            "power": args.power,
            "comparison": args.comparison,
            "rational": args.rational,
        }
        solution = post_form(args.base_url, "/calculate", request_data)
        comparison = args.comparison
        reversed_direction = False

        if not solution.get("success") and is_direction_error(solution):
            reversed_data = dict(request_data)
            reversed_data["comparison"] = flip_comparison(args.comparison)
            reversed_solution = post_form(args.base_url, "/calculate", reversed_data)
            if not reversed_solution.get("success"):
                print(json.dumps(solution, ensure_ascii=False, indent=2))
                return 1
            solution = reversed_solution
            comparison = reversed_data["comparison"]
            reversed_direction = True
        elif not solution.get("success"):
            print(json.dumps(solution, ensure_ascii=False, indent=2))
            return 1

        params = dict(solution["parameters"])
        params.update(
            {
                "type": args.type,
                "coef": args.power,
                "comparison": comparison,
                "rational": args.rational,
            }
        )
        rendered = get_json(args.base_url, "/get_integral_image", params)
        if reversed_direction:
            print("你输入的不等号方向可能反了。原式暂未找到证明，但反向不等式可以由注意力计算器生成积分证明。")
        print(rendered.get("equation", ""))
        return 0
    except Exception as exc:
        print(f"远程注意力计算器服务暂时不可用，请稍后再试。({exc})", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
