# Tensor Rails

Open-source tools for running AI inference infrastructure.

Getting a model from weights on disk to a serving GPU fleet, and keeping it
there, still takes a lot of hand-built plumbing. We build that plumbing as
small tools: each does one job, fits the stack you already run (vLLM,
Kubernetes, OCI registries, stock NVIDIA drivers), and comes with the
measurements behind its numbers.

### Projects

**[warmctl](https://warmctl.io)** · GPU checkpoint and restore for vLLM<br>
Warm an engine up once, snapshot it, restore it on any matching host in
seconds. GLM-5.3-Flash on 8×H100: 650 s cold start, 37 s restore, then stock
serving speed. `v2.0 beta` · [docs](https://warmctl.io/docs/)

### What we work on

- **Cold start and scaling**: new replicas in seconds, not minutes.
- **Distribution**: moving models, snapshots and caches between hosts and clouds.
- **Operations**: host checks, diagnostics and day-2 tooling for GPU fleets.

### How we work

- Open source, Apache-2.0.
- Numbers come from runs on real hardware, with the GPUs and versions stated.

---

Tensor Rails is at an early stage and works quietly. More tools are coming;
each is released once it is measured and documented.

Maintained by [Kirill Bespalov](https://www.linkedin.com/in/kirill-bespalov/).
