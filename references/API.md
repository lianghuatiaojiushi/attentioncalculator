# 注意力计算器 Remote API

This file documents how the skill calls the hosted service. It intentionally documents only public request/response behavior. It does not contain any proof-search logic or coefficient data.

## Supported Proof Types

```text
pi, e, pi_n, e_q, ln_q, ln_q_square,
sin_q, cos_q, tan_q, cot_q,
sin_q_degree, cos_q_degree,
sin_pi_q, cos_pi_q,
arctan_q, arccot_q,
sinh_q, cosh_q, tanh_q, coth_q,
artanh_q, arcoth_q,
gamma, golden, catalan, zeta3, e_pi, varpi, gauss
```

## Step 1: Calculate

Endpoint:

```text
POST /calculate
Content-Type: application/x-www-form-urlencoded
```

Form fields:

| Field | Meaning | Example |
| --- | --- | --- |
| `type` | proof type | `pi` |
| `power` | coefficient or argument | `1`, `3/2` |
| `comparison` | `>` or `<` | `>` |
| `rational` | rational number | `3`, `22/7` |

Successful response:

```json
{
  "success": true,
  "type": "pi",
  "parameters": {
    "m": 1,
    "n": 2,
    "a_val": "1/3",
    "b_val": "2/5",
    "c_val": "0",
    "au_val": "5",
    "bu_val": "6",
    "cu_val": "0",
    "u_val": "15"
  }
}
```

The numeric values above are only shape examples, not real proof data.

## Step 2: Render LaTeX

Endpoint:

```text
GET /get_integral_image
```

Query parameters:

Use every field returned under `parameters` from `/calculate`, plus:

| Field | Meaning |
| --- | --- |
| `type` | same proof type |
| `coef` | same value as `power` |
| `comparison` | same comparison |
| `rational` | same right rational |

Successful response:

```json
{
  "equation": "...LaTeX integral proof..."
}
```

Display the returned `equation` as a Markdown math block:

```text
$$
...LaTeX integral proof...
$$
```

Do not place the formula inside a Markdown code block.

## Error Handling

Use `http://zhuyidao.net` as the service base URL.

Before calling the service, check whether the requested inequality belongs to one of the 29 supported proof types above. If it does not, do not call the service. Reply:

```text
这个不等式目前不在注意力计算器支持的 29 种类型之列。
目前支持的类型有：pi, e, pi_n, e_q, ln_q, ln_q_square, sin_q, cos_q, tan_q, cot_q, sin_q_degree, cos_q_degree, sin_pi_q, cos_pi_q, arctan_q, arccot_q, sinh_q, cosh_q, tanh_q, coth_q, artanh_q, arcoth_q, gamma, golden, catalan, zeta3, e_pi, varpi, gauss。
```

If the service returns an error JSON, show the error message. If the service cannot be reached, say:

```text
远程注意力计算器服务暂时不可用，请稍后再试。
```

Do not attempt local proof generation.

If `/calculate` fails and the server error is:

```text
要证明的式子不等号方向反了
```

the skill may call `/calculate` once more with the comparison reversed. The direction judgment comes from the hosted server application; the skill must not compute the truth value locally. If the reversed request succeeds, reply:

```text
你输入的不等号方向可能反了。原式暂未找到证明，但反向不等式可以由注意力计算器生成积分证明。
```

Then show the reversed inequality and its returned proof. This retry still uses only the hosted service and must not infer or rebuild the proof locally.

The skill should display the LaTeX string returned by `/get_integral_image` directly as a Markdown math block wrapped with `$$`. It should not invoke visualization-guide, browser, screenshot, rendering, or image-generation workflows.
