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

## Error Handling

If the service returns an error JSON, show the error message. If the service cannot be reached, say:

```text
远程注意力计算器服务暂时不可用，请稍后再试。
```

Do not attempt local proof generation.

