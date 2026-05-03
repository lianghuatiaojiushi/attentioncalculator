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

Service base URL:

```text
https://zhuyidao.net
```

Use `zhuyidao.net` only.

## Workflow

1. First identify whether the requested inequality belongs to one of the 29 supported proof types listed below. If it does not, do not call the server. Reply in Chinese:

   ```text
   这个不等式目前不在注意力计算器支持的 29 种类型之列。
   目前支持的类型有：pi, e, pi_n, e_q, ln_q, ln_q_square, sin_q, cos_q, tan_q, cot_q, sin_q_degree, cos_q_degree, sin_pi_q, cos_pi_q, arctan_q, arccot_q, sinh_q, cosh_q, tanh_q, coth_q, artanh_q, arcoth_q, gamma, golden, catalan, zeta3, e_pi, varpi, gauss。
   ```

2. Ask the user for:
   - proof type, such as `pi`, `e`, `pi_n`, `e_q`, `ln_q`, `sin_q`, `gamma`, etc.
   - left coefficient or argument, as an integer or fraction.
   - comparison direction, either `>` or `<`.
   - right rational number, as an integer or fraction.
3. Submit the values to the remote `/calculate` endpoint.
4. If `/calculate` fails because the server returns `要证明的式子不等号方向反了`, try the same request once more with the comparison direction reversed (`>` becomes `<`, `<` becomes `>`). The direction check must come from the hosted server API, not from local calculation in the skill.
5. If the reversed comparison succeeds, tell the user in Chinese:

   ```text
   你输入的不等号方向可能反了。原式暂未找到证明，但反向不等式可以由注意力计算器生成积分证明。
   ```

   Then present the reversed inequality and its returned proof.
6. If the original request fails for any other reason, or if the reversed request also fails, show the service error briefly and ask the user to check the type, integer/fraction format, and comparison direction.
7. If `/calculate` succeeds, call `/get_integral_image` with the returned parameters.
8. Present the returned LaTeX equation to the user.
9. Briefly explain that the non-negativity of the displayed integral proves the inequality.

Read `references/API.md` when exact endpoint parameters are needed.

## Response Style

Return:

- the normalized inequality requested by the user;
- the generated integral proof in LaTeX;
- a short note that the computation was performed by the remote 注意力计算器 service.

Never state or imply that the skill contains the underlying coefficient tables.
