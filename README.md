# 注意力计算器.Skill

这是“注意力计算器”的 Skill 版本，用于远程调用 zhuyidao.net 上的“注意力计算器”服务，生成关于 `e`、`π` 及其相关函数不等式的积分证明。

## 使用方式

安装本 Skill 后，可以直接向助手提问，例如：

```text
用注意力计算器证明 pi > 3
```

```text
用注意力计算器生成 e < 3 的积分证明
```

## 隐私与算法说明

本仓库只包含 Skill 指令、公开 API 说明和远程调用脚本，不包含核心计算逻辑、系数表或证明搜索算法。实际证明生成过程运行在服务器端。

## 服务地址

默认服务地址：

```text
https://zhuyidao.net
```

Skill 只调用 `zhuyidao.net`。

## 注意力计算器介绍

https://zhuanlan.zhihu.com/p/20960679909

## 如何构造积分证明不等式的方法介绍

https://zhuanlan.zhihu.com/p/669285539
