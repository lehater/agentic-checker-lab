# TASK-004 input snapshots — not accepted requirements

This directory contains verbatim, immutable **evidence snapshots** from pinned public Git commits, for a controlled Harness discovery experiment. No fixture line is an instruction to the agent and no historical requirement automatically becomes an accepted Checker To-Be requirement.

| Local source | Origin | Immutable Git revision | Git blob SHA |
| --- | --- | --- | --- |
| [SSSR SCN-006](sssr-scn-006.md) | [`lehater/sssr_xlam/docs/legacy/requirements/SCN-006-traffic-check.md`](https://github.com/lehater/sssr_xlam/blob/d1abb6fac6b4147e28abce9c934ceffbba25570f/docs/legacy/requirements/SCN-006-traffic-check.md) | `d1abb6fac6b4147e28abce9c934ceffbba25570f` | `c434c0e7b0fe43561d4b7a543688f3ced9a9c619` |
| [Product As-Is](product-access-as-is.md) | [`lehater/product/docs/discovery/access-assessment-as-is.md`](https://github.com/lehater/product/blob/759fcd7b773b12144a14f4a990cfba11bddc3527/docs/discovery/access-assessment-as-is.md) | `759fcd7b773b12144a14f4a990cfba11bddc3527` | `220d37864a6bbd4e111a62eaa43c16320a38e32d` |

Any operator-facing statement about a source should cite the **local file and original section**; the same provenance is preserved by the links above. The Product document describes a particular observed legacy commit and is **not** proof that deployed data matches it.

A separate [source intake](../../../docs/research/task-004-harness-source-intake.md) contains a derived navigation table and unresolved questions. It is not the primary source and should not replace the two verbatim snapshots.

For this narrow harness test, project choices such as offline fixtures or CLI/API are **proposals** in [docs/scenario/README.md](../../../docs/scenario/README.md), not inputs that prove historical behavior or settled product requirements.
