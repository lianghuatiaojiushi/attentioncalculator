---
name: attention-calculator
description: Use the remote 注意力计算器 service to generate integral proofs for inequalities between supported constants/functions and rational numbers. The skill is a thin client only: it must call the server API and must never contain or reconstruct coefficient tables, proof-search tables, or solver logic.
metadata:
  display-name: 注意力计算器
  short-description: 远程生成 29 类不等式的积分证明
---

# 注意力计算器

Use this skill when the user asks to prove an inequality supported by the 注意力计算器, such as comparisons involving `pi`, `e`, `pi^q`, `e^q`, `ln q`, trigonometric/hyperbolic functions, Euler's constant, Catalan's constant, Apéry's constant, the golden ratio, the lemniscate constant, or Gauss's constant.

## Privacy And IP Boundary

This skill is intentionally a thin client.

- Do not include, reveal, infer, summarize, or recreate server-side solver internals.
- Do not include coefficient tables, search-order tables, solver functions, or any code copied from the server application.
- Do not calculate proofs locally.
- Always call the hosted service API and return only the API result.
- If the API is unavailable, report that the remote calculator service is unavailable. Do not attempt to rebuild the algorithm.

## Hosted Service

Default service base URL:

```text
https://zhuyidao.net
```

Fallback during HTTP-only deployment:

```text
http://zhuyidao.net
```

## Workflow

1. Ask the user for:
   - proof type, such as `pi`, `e`, `pi_n`, `e_q`, `ln_q`, `sin_q`, `gamma`, etc.
   - left coefficient or argument, as an integer or fraction.
   - comparison direction, either `>` or `<`.
   - right rational number, as an integer or fraction.
2. Submit the values to the remote `/calculate` endpoint.
3. If `/calculate` succeeds, call `/get_integral_image` with the returned parameters.
4. Present the returned LaTeX equation to the user.
5. Briefly explain that the non-negativity of the displayed integral proves the inequality.

Read `references/API.md` when exact endpoint parameters are needed.

## Response Style

Return:

- the normalized inequality requested by the user;
- the generated integral proof in LaTeX;
- a short note that the computation was performed by the remote 注意力计算器 service.

Never state or imply that the skill contains the underlying coefficient tables.
