# Q1 Cross-Benchmark Contrast Summary

## Purpose

This document compares model-level gender-preference results across the benchmark suite, including controlled benchmarks and real-world ArabJobs v7 data.

## Output

- Combined contrast table: `results\q1_cross_benchmark_contrast\q1_cross_benchmark_overall_contrast.csv`

## Cross-Benchmark Direction Changes

### Qwen/Qwen2.5-0.5B

- Benchmarks covered: 1
- Directions observed: feminine
- Direction changed across benchmarks: False

  - v2_main: avg=-0.3425130208333333, direction=feminine

### aubmindlab/aragpt2-base

- Benchmarks covered: 3
- Directions observed: masculine, feminine
- Direction changed across benchmarks: True

  - arabjobs_v7_real_world: avg=0.0894636630749459, direction=masculine
  - v2_main: avg=0.1257066498200098, direction=masculine
  - v6_job_roles: avg=-0.3019826209379567, direction=feminine

### aubmindlab/aragpt2-medium

- Benchmarks covered: 2
- Directions observed: masculine, feminine
- Direction changed across benchmarks: True

  - v2_main: avg=0.2230324496825536, direction=masculine
  - v6_job_roles: avg=-0.2435836901267369, direction=feminine

### bigscience/bloom-1b1

- Benchmarks covered: 2
- Directions observed: feminine
- Direction changed across benchmarks: False

  - v2_main: avg=-0.1655517578125, direction=feminine
  - v6_job_roles: avg=-0.0808241102430555, direction=feminine

### bigscience/bloom-560m

- Benchmarks covered: 3
- Directions observed: masculine, feminine, near-neutral / mixed
- Direction changed across benchmarks: True

  - arabjobs_v7_real_world: avg=0.1089576828292733, direction=masculine
  - v2_main: avg=-0.2174397786458333, direction=feminine
  - v6_job_roles: avg=-0.0163350423177083, direction=near-neutral / mixed

### facebook/xglm-564M

- Benchmarks covered: 1
- Directions observed: feminine
- Direction changed across benchmarks: False

  - v2_main: avg=-0.2137858072916666, direction=feminine

## Publication Claim

The cross-benchmark contrast supports the central paper claim that Arabic occupational gender-bias scores are not fixed model properties. Instead, they vary across benchmark design, template structure, job-title context, expanded job-role framing, and real-world recruitment-language data.