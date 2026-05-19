# HIPE-2026 Evaluation Results

This file is generated from `results.d/system-rankings/*.tsv`.

## Teams

| team | name | affiliation |
| --- | --- | --- |
| baseline | Ministral-3-3B-Instruct GGUF baseline 0.2.2 random seed 42 | HIPE-2026 organizers |
| random | Random Decision Baseline | HIPE-2026 organizers |
| team1 | Awakened | National University of Science and Technology Politehnica Bucharest |
| team10 | BIU_NLP | Bar-Ilan University |
| team11 | gipplab | University of Göttingen |
| team12 | whereami | Alexandria University |
| team13 | Spinfo | Universität zu Köln |
| team14 | MILRIT | University of Toulouse & La Rochelle University |
| team15 | FI Code | University of the Bundeswehr |
| team16 | Rittik&Souvik | Jadavpur University, Kolkata |
| team17 | INSA Lyon | INSA Lyon - University of Lyon |
| team2 | DS@GT_HIPE | Georgia Institute of Technology |
| team3 | VerbaNexAI II | Universidad Tecnológica de Bolívar |
| team4 | FourBytes | Sri Sivasubramaniya Nadar College of Engineering |
| team5 | UMUTEAM | Universidad de Murcia |
| team6 | VerbaNexAI I | Universidad Tecnológica de Bolívar |
| team7 | ROSTI | Université Lumière Lyon |
| team8 | MaxFo-Ajie | Foshan University |
| team9 | Hansel&Gretel | IIT Roorkee |

## Table of Contents

- [Accuracy Profile Ranking Overall](#accuracy-profile-ranking-overall)
- [Accuracy Profile Ranking German](#accuracy-profile-ranking-german)
- [Accuracy Profile Ranking English](#accuracy-profile-ranking-english)
- [Accuracy Profile Ranking French](#accuracy-profile-ranking-french)
- [Generalization Profile Ranking](#generalization-profile-ranking)
- [Generalization Profile Ranking French](#generalization-profile-ranking-french)
- [Efficiency Profile Ranking Overall](#efficiency-profile-ranking-overall)
- [Balanced Efficiency Profile Ranking Overall](#balanced-efficiency-profile-ranking-overall)
- [Efficiency Profile Ranking German](#efficiency-profile-ranking-german)
- [Efficiency Profile Ranking English](#efficiency-profile-ranking-english)
- [Efficiency Profile Ranking French](#efficiency-profile-ranking-french)

## Profile Score Definitions

- Accuracy Profile Ranking uses the `impresso` test files.
- Generalization Profile Ranking uses the `surprise` test files.
- For a label `l`, `recall_l = true_positives_l / gold_instances_l`.
- `at_macro_recall = mean(recall_TRUE, recall_PROBABLE, recall_FALSE)` for the `at` labels.
- `isAt_macro_recall = mean(recall_TRUE, recall_FALSE)` for the `isAt` labels.
- `impresso_profile_score`: score for one `impresso` language file, computed as the mean of `at_macro_recall` and `isAt_macro_recall`.
- `mean_impresso_profile_score`: mean of `impresso_profile_score` over the submitted `impresso` language files.
- `surprise_profile_score`: score on a `surprise` file, computed as `at_macro_recall`; `isAt` is not evaluated for `surprise`.
- Accuracy columns are included as contextual diagnostics; ranking is still determined by the macro-recall profile score.
- `mean_efficiency_profile_rank`: mean of `rank_impresso_profile_score`, `rank_hipe_parameter_count`, and `rank_hipe_model_size`; lower is better.
- `balanced_efficiency_profile_rank`: `0.5 * rank_impresso_profile_score + 0.25 * rank_hipe_parameter_count + 0.25 * rank_hipe_model_size`; lower is better.
- If `team_efficiency_opt_out=true` in a run's `*-info.json`, that run is excluded from efficiency ranking tables.
- If organizer fields `hipe_parameter_count` or `hipe_model_size` are `null`, they are internally treated as maxint for efficiency rank computation (worst resource rank), while remaining empty in table outputs.

## Accuracy Profile Ranking Overall

| rank | team | run | mean impresso profile score | languages | num language files |
| --- | --- | --- | --- | --- | --- |
| 1 | team13 | run1 | 0.7479 | de,en,fr | 3 |
| 2 | team13 | run3 | 0.7289 | de,en,fr | 3 |
| 3 | team8 | run1 | 0.7001 | de,en,fr | 3 |
| 4 | team13 | run2 | 0.689 | de,en,fr | 3 |
| 5 | team12 | run1 | 0.688 | de,en,fr | 3 |
| 6 | team12 | run2 | 0.6833 | de,en,fr | 3 |
| 7 | team8 | run2 | 0.669 | de,en,fr | 3 |
| 8 | team1 | run3 | 0.6671 | de,en,fr | 3 |
| 9 | team1 | run1 | 0.6584 | de,en,fr | 3 |
| 10 | team8 | run3 | 0.6544 | de,en,fr | 3 |
| 11 | team17 | run1 | 0.639 | de,en,fr | 3 |
| 12 | team11 | run2 | 0.6271 | de,en,fr | 3 |
| 13 | team9 | run3 | 0.6221 | de,en,fr | 3 |
| 14 | team11 | run1 | 0.6141 | de,en,fr | 3 |
| 15 | team14 | run3 | 0.5951 | de,en,fr | 3 |
| 16 | team5 | run2 | 0.5856 | de,en,fr | 3 |
| 17 | baseline | run1 | 0.5818 | de,en,fr | 3 |
| 18 | team3 | run3 | 0.5795 | de,en,fr | 3 |
| 19 | team9 | run2 | 0.5788 | de,en,fr | 3 |
| 20 | team10 | run2 | 0.5781 | de,en,fr | 3 |
| 21 | team14 | run1 | 0.5623 | de,en,fr | 3 |
| 22 | team1 | run2 | 0.5494 | de,en,fr | 3 |
| 23 | team9 | run1 | 0.5458 | de,en,fr | 3 |
| 24 | team10 | run3 | 0.539 | de,en,fr | 3 |
| 25 | team3 | run2 | 0.5187 | de,en,fr | 3 |
| 26 | team2 | run1 | 0.5142 | de,en,fr | 3 |
| 27 | team11 | run3 | 0.5069 | de,en,fr | 3 |
| 28 | team3 | run1 | 0.5004 | de,en,fr | 3 |
| 29 | team6 | run2 | 0.4842 | de,en,fr | 3 |
| 30 | team2 | run2 | 0.4836 | de,en,fr | 3 |
| 31 | team2 | run3 | 0.4771 | de,en,fr | 3 |
| 32 | team15 | run2 | 0.4734 | de,en,fr | 3 |
| 33 | team17 | run3 | 0.4731 | de,en,fr | 3 |
| 34 | team17 | run2 | 0.4708 | de,en,fr | 3 |
| 35 | team15 | run3 | 0.4645 | de,en,fr | 3 |
| 36 | team6 | run1 | 0.4628 | de,en,fr | 3 |
| 37 | team7 | run3 | 0.4564 | de,en,fr | 3 |
| 38 | team7 | run2 | 0.4507 | de,en,fr | 3 |
| 39 | team5 | run3 | 0.4495 | de,en,fr | 3 |
| 40 | team7 | run1 | 0.446 | de,en,fr | 3 |
| 41 | team10 | run1 | 0.4429 | de,en,fr | 3 |
| 42 | team5 | run1 | 0.4408 | de,en,fr | 3 |
| 43 | team15 | run1 | 0.427 | de,en,fr | 3 |
| 44 | team14 | run2 | 0.4264 | de,en,fr | 3 |
| 45 | team4 | run1 | 0.4061 | de,en,fr | 3 |
| 46 | random | run1 | 0.4049 | de,en,fr | 3 |

Top 3 teams by best run:

1. Spinfo (team13), run1, table rank 1, mean impresso profile score 0.7479
2. MaxFo-Ajie (team8), run1, table rank 3, mean impresso profile score 0.7001
3. whereami (team12), run1, table rank 5, mean impresso profile score 0.688

Only team runs that submitted all `impresso` language files are included in this overall ranking. Team runs with partial submissions are shown only in the dataset-specific ranking tables.

## Accuracy Profile Ranking German

| rank | team | run | submission | impresso profile score | at macro recall | at accuracy | isAt macro recall | isAt accuracy | diagnostics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | team13 | run3 | team13_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.771 | 0.7027 | 0.8277 | 0.8394 | 0.8866 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 2 | team13 | run1 | team13_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.7608 | 0.7017 | 0.8067 | 0.8199 | 0.8782 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 3 | team12 | run2 | team12_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.7072 | 0.611 | 0.7689 | 0.8034 | 0.8739 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 4 | team12 | run1 | team12_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.7041 | 0.5928 | 0.7521 | 0.8154 | 0.8782 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 5 | team13 | run2 | team13_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.686 | 0.6659 | 0.7647 | 0.706 | 0.8319 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 6 | team1 | run3 | team1_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.6746 | 0.5994 | 0.6639 | 0.7498 | 0.8361 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 7 | team1 | run1 | team1_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.6739 | 0.5857 | 0.6555 | 0.7621 | 0.8277 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 8 | team17 | run1 | team17_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.6725 | 0.4953 | 0.6681 | 0.8497 | 0.8361 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 9 | team8 | run1 | team8_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.672 | 0.6048 | 0.7311 | 0.7391 | 0.8403 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 10 | team8 | run2 | team8_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.6485 | 0.6146 | 0.7563 | 0.6823 | 0.8109 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 11 | team8 | run3 | team8_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.6335 | 0.5864 | 0.7353 | 0.6807 | 0.8151 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 12 | team5 | run2 | team5_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.6305 | 0.5229 | 0.5924 | 0.738 | 0.7605 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 13 | team9 | run3 | team9_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.5994 | 0.4877 | 0.6303 | 0.7112 | 0.8067 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 14 | team11 | run1 | team11_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.5957 | 0.587 | 0.7269 | 0.6045 | 0.7773 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 15 | team11 | run2 | team11_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.5941 | 0.6061 | 0.7143 | 0.5821 | 0.7647 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 16 | team14 | run3 | team14_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.5886 | 0.5339 | 0.5336 | 0.6433 | 0.7353 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 17 | team14 | run1 | team14_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.5802 | 0.4752 | 0.6597 | 0.6852 | 0.7563 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 18 | team3 | run3 | team3_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.5697 | 0.5301 | 0.7059 | 0.6093 | 0.7647 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 19 | baseline | run1 | baseline_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.5553 | 0.4977 | 0.6176 | 0.6129 | 0.7437 | [Comparison](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 20 | team10 | run3 | team10_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.5451 | 0.4452 | 0.6261 | 0.645 | 0.7899 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 21 | team1 | run2 | team1_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.5417 | 0.4952 | 0.5126 | 0.5882 | 0.7605 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 22 | team9 | run2 | team9_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.5254 | 0.5165 | 0.5588 | 0.5344 | 0.7353 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 23 | team7 | run3 | team7_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.5222 | 0.4302 | 0.584 | 0.6141 | 0.6933 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 24 | team9 | run1 | team9_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.521 | 0.515 | 0.6134 | 0.5269 | 0.7311 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 25 | team7 | run1 | team7_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.5196 | 0.4309 | 0.5756 | 0.6082 | 0.6849 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 26 | team7 | run2 | team7_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.5192 | 0.4361 | 0.5756 | 0.6024 | 0.6765 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 27 | team11 | run3 | team11_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.5181 | 0.5093 | 0.6555 | 0.5269 | 0.7311 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 28 | team2 | run1 | team2_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.516 | 0.4276 | 0.6008 | 0.6043 | 0.6597 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 29 | team6 | run2 | team6_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.5071 | 0.422 | 0.4496 | 0.5923 | 0.6555 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 30 | team2 | run3 | team2_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.5054 | 0.4204 | 0.5588 | 0.5904 | 0.6723 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 31 | team10 | run2 | team10_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.505 | 0.474 | 0.5882 | 0.536 | 0.7311 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 32 | team3 | run2 | team3_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.5022 | 0.4878 | 0.6471 | 0.5165 | 0.7227 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 33 | team2 | run2 | team2_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.4937 | 0.3895 | 0.4328 | 0.5978 | 0.6765 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 34 | team3 | run1 | team3_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.4808 | 0.4384 | 0.6134 | 0.5233 | 0.6933 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 35 | team15 | run2 | team15_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.4678 | 0.3906 | 0.3824 | 0.545 | 0.4244 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 36 | team5 | run3 | team5_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.4527 | 0.3536 | 0.2857 | 0.5517 | 0.395 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 37 | team10 | run1 | team10_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.4495 | 0.3765 | 0.6429 | 0.5224 | 0.7311 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 38 | team6 | run1 | team6_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.4488 | 0.3487 | 0.3361 | 0.5488 | 0.6387 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 39 | team17 | run2 | team17_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.4435 | 0.3792 | 0.5546 | 0.5078 | 0.7101 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 40 | team15 | run3 | team15_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.4378 | 0.3619 | 0.6303 | 0.5136 | 0.7185 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 41 | team14 | run2 | team14_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 0.4365 | 0.3507 | 0.5714 | 0.5224 | 0.7311 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 42 | team17 | run3 | team17_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 0.4351 | 0.3442 | 0.5546 | 0.5261 | 0.5798 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 43 | team5 | run1 | team5_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.4167 | 0.3333 | 0.6134 | 0.5 | 0.7185 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 44 | team15 | run1 | team15_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.4162 | 0.3324 | 0.416 | 0.5 | 0.7185 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 45 | random | run1 | random_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.4058 | 0.3211 | 0.3403 | 0.4906 | 0.4832 | [Comparison](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 46 | team4 | run1 | team4_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 0.372 | 0.2446 | 0.2353 | 0.4995 | 0.6134 | [Comparison](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |

Top 3 teams by best run:

1. Spinfo (team13), run3, table rank 1, impresso profile score 0.771
2. whereami (team12), run2, table rank 3, impresso profile score 0.7072
3. Awakened (team1), run3, table rank 6, impresso profile score 0.6746

## Accuracy Profile Ranking English

| rank | team | run | submission | impresso profile score | at macro recall | at accuracy | isAt macro recall | isAt accuracy | diagnostics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | team8 | run1 | team8_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.7493 | 0.7424 | 0.7593 | 0.7562 | 0.7901 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 2 | team13 | run1 | team13_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.7279 | 0.656 | 0.6667 | 0.7998 | 0.8272 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 3 | team8 | run2 | team8_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.7142 | 0.7133 | 0.7346 | 0.7151 | 0.7531 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 4 | team12 | run1 | team12_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.7023 | 0.6226 | 0.7222 | 0.7819 | 0.8148 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 5 | team8 | run3 | team8_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.7003 | 0.6776 | 0.7037 | 0.7229 | 0.7654 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 6 | team12 | run2 | team12_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.6992 | 0.6063 | 0.7099 | 0.7921 | 0.821 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 7 | team13 | run3 | team13_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.6808 | 0.5874 | 0.6111 | 0.7741 | 0.8025 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 8 | team13 | run2 | team13_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.6427 | 0.6215 | 0.6605 | 0.664 | 0.7222 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 9 | team1 | run3 | team1_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.6415 | 0.6009 | 0.6296 | 0.682 | 0.7407 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 10 | team9 | run3 | team9_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.6367 | 0.5582 | 0.6481 | 0.7151 | 0.7531 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 11 | team11 | run2 | team11_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.6174 | 0.5784 | 0.5309 | 0.6564 | 0.7222 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 12 | team11 | run1 | team11_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.6143 | 0.5542 | 0.537 | 0.6743 | 0.7346 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 13 | team17 | run1 | team17_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.5985 | 0.4745 | 0.5988 | 0.7225 | 0.7346 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 14 | team9 | run1 | team9_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.5976 | 0.5645 | 0.5062 | 0.6308 | 0.7037 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 15 | team14 | run3 | team14_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.5881 | 0.5099 | 0.5123 | 0.6663 | 0.7037 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 16 | team9 | run2 | team9_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.5866 | 0.5015 | 0.4321 | 0.6718 | 0.7346 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 17 | team1 | run1 | team1_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.5848 | 0.5289 | 0.5864 | 0.6408 | 0.6914 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 18 | team3 | run3 | team3_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.5812 | 0.5394 | 0.6605 | 0.623 | 0.6914 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 19 | team10 | run2 | team10_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.5762 | 0.4807 | 0.5309 | 0.6718 | 0.7346 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 20 | team3 | run2 | team3_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.5718 | 0.5566 | 0.6111 | 0.5871 | 0.6605 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 21 | team3 | run1 | team3_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.5607 | 0.4709 | 0.5988 | 0.6504 | 0.6543 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 22 | baseline | run1 | baseline_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.5551 | 0.4772 | 0.5494 | 0.6331 | 0.6852 | [Comparison](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 23 | team5 | run2 | team5_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.5384 | 0.4419 | 0.463 | 0.6349 | 0.6296 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 24 | team11 | run3 | team11_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.5221 | 0.4339 | 0.4198 | 0.6102 | 0.6852 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 25 | team17 | run2 | team17_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.5128 | 0.4515 | 0.5617 | 0.5741 | 0.642 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 26 | team17 | run3 | team17_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.5107 | 0.4074 | 0.4938 | 0.6141 | 0.5926 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 27 | team2 | run1 | team2_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.5103 | 0.3986 | 0.5 | 0.6221 | 0.6235 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 28 | team10 | run3 | team10_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.5101 | 0.4586 | 0.5062 | 0.5615 | 0.6481 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 29 | team1 | run2 | team1_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.4989 | 0.3392 | 0.3333 | 0.6586 | 0.6975 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 30 | team2 | run3 | team2_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.4834 | 0.3632 | 0.4506 | 0.6036 | 0.5679 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 31 | team6 | run2 | team6_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.4808 | 0.37 | 0.4506 | 0.5916 | 0.6173 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 32 | team14 | run1 | team14_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.4808 | 0.3885 | 0.4877 | 0.573 | 0.5556 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 33 | team6 | run1 | team6_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.4757 | 0.3293 | 0.358 | 0.622 | 0.6173 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 34 | team5 | run1 | team5_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.4702 | 0.3704 | 0.4877 | 0.5699 | 0.5123 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 35 | team15 | run2 | team15_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.4624 | 0.3781 | 0.5 | 0.5467 | 0.4815 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 36 | team10 | run1 | team10_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.4583 | 0.3962 | 0.4444 | 0.5205 | 0.6111 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 37 | team7 | run3 | team7_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.4541 | 0.3883 | 0.3951 | 0.52 | 0.5741 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 38 | team15 | run3 | team15_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.4466 | 0.3251 | 0.4198 | 0.568 | 0.5617 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 39 | team7 | run2 | team7_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.4431 | 0.3868 | 0.3827 | 0.4994 | 0.5556 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 40 | team2 | run2 | team2_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.4401 | 0.3707 | 0.463 | 0.5095 | 0.5494 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 41 | team14 | run2 | team14_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 0.4353 | 0.3501 | 0.3889 | 0.5205 | 0.6111 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 42 | team7 | run1 | team7_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.4335 | 0.383 | 0.3704 | 0.484 | 0.537 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 43 | team15 | run1 | team15_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.4313 | 0.3626 | 0.4321 | 0.5 | 0.5988 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 44 | team5 | run3 | team5_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 0.4312 | 0.3289 | 0.4568 | 0.5335 | 0.4444 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 45 | team16 | run1 | team16_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.4254 | 0.3258 | 0.3889 | 0.5249 | 0.5617 | [Comparison](results.d/diagnostics/team16_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team16_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 46 | team4 | run1 | team4_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.4187 | 0.3384 | 0.3457 | 0.4989 | 0.5123 | [Comparison](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 47 | random | run1 | random_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 0.3733 | 0.2532 | 0.3025 | 0.4935 | 0.4877 | [Comparison](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |

Top 3 teams by best run:

1. MaxFo-Ajie (team8), run1, table rank 1, impresso profile score 0.7493
2. Spinfo (team13), run1, table rank 2, impresso profile score 0.7279
3. whereami (team12), run1, table rank 4, impresso profile score 0.7023

## Accuracy Profile Ranking French

| rank | team | run | submission | impresso profile score | at macro recall | at accuracy | isAt macro recall | isAt accuracy | diagnostics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | team13 | run1 | team13_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.7551 | 0.6785 | 0.7815 | 0.8318 | 0.8529 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 2 | team13 | run2 | team13_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.7383 | 0.6774 | 0.7773 | 0.7991 | 0.8571 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 3 | team13 | run3 | team13_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.7349 | 0.6566 | 0.7941 | 0.8132 | 0.8403 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 4 | team1 | run1 | team1_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.7163 | 0.6843 | 0.8445 | 0.7483 | 0.7941 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 5 | team1 | run3 | team1_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.6854 | 0.6529 | 0.8109 | 0.7179 | 0.7815 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 6 | team8 | run1 | team8_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.679 | 0.6543 | 0.7479 | 0.7037 | 0.7983 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 7 | team11 | run2 | team11_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.6697 | 0.6946 | 0.7143 | 0.6448 | 0.7521 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 8 | team12 | run1 | team12_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.6578 | 0.5755 | 0.7941 | 0.74 | 0.8067 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 9 | team10 | run2 | team10_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.6529 | 0.5703 | 0.6387 | 0.7356 | 0.7773 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 10 | team17 | run1 | team17_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.6459 | 0.4772 | 0.6849 | 0.8147 | 0.8067 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 11 | team8 | run2 | team8_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.6444 | 0.5789 | 0.7101 | 0.7099 | 0.8025 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 12 | team12 | run2 | team12_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.6435 | 0.5502 | 0.7815 | 0.7368 | 0.8025 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 13 | baseline | run1 | baseline_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.6349 | 0.5893 | 0.6975 | 0.6804 | 0.7479 | [Comparison](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 14 | team11 | run1 | team11_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.6322 | 0.5886 | 0.7059 | 0.6758 | 0.7773 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 15 | team9 | run3 | team9_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.6303 | 0.5268 | 0.7311 | 0.7338 | 0.8025 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 16 | team8 | run3 | team8_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.6295 | 0.5861 | 0.7563 | 0.6728 | 0.7773 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 17 | team14 | run1 | team14_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.6261 | 0.5335 | 0.7437 | 0.7187 | 0.7353 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 18 | team9 | run2 | team9_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.6243 | 0.635 | 0.605 | 0.6137 | 0.7269 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 19 | team14 | run3 | team14_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.6087 | 0.5428 | 0.6092 | 0.6746 | 0.7521 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 20 | team1 | run2 | team1_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.6076 | 0.5397 | 0.5882 | 0.6754 | 0.7689 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 21 | team5 | run2 | team5_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.588 | 0.4458 | 0.5882 | 0.7302 | 0.7269 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 22 | team3 | run3 | team3_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.5877 | 0.5438 | 0.7731 | 0.6316 | 0.7269 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 23 | team10 | run3 | team10_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.5617 | 0.5743 | 0.6891 | 0.5492 | 0.6891 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 24 | team9 | run1 | team9_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.5189 | 0.467 | 0.5672 | 0.5707 | 0.7017 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 25 | team2 | run2 | team2_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.5171 | 0.4154 | 0.5756 | 0.6189 | 0.6471 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 26 | team2 | run1 | team2_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.5162 | 0.3969 | 0.479 | 0.6354 | 0.6807 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 27 | team15 | run3 | team15_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.5091 | 0.4112 | 0.542 | 0.607 | 0.584 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 28 | team15 | run2 | team15_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.4902 | 0.4001 | 0.4748 | 0.5802 | 0.458 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 29 | team3 | run2 | team3_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.4822 | 0.4525 | 0.6723 | 0.512 | 0.6597 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 30 | team11 | run3 | team11_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.4805 | 0.4057 | 0.5798 | 0.5554 | 0.6933 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 31 | team17 | run3 | team17_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.4734 | 0.3463 | 0.5462 | 0.6004 | 0.6345 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 32 | team6 | run2 | team6_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.4648 | 0.3524 | 0.416 | 0.5773 | 0.6513 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 33 | team5 | run3 | team5_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.4645 | 0.3521 | 0.4034 | 0.5768 | 0.4496 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 34 | team6 | run1 | team6_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.464 | 0.3597 | 0.4622 | 0.5683 | 0.6513 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 35 | team3 | run1 | team3_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.4597 | 0.4024 | 0.5924 | 0.5169 | 0.6387 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 36 | team17 | run2 | team17_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.4561 | 0.4045 | 0.6008 | 0.5078 | 0.6345 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 37 | team2 | run3 | team2_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.4424 | 0.4139 | 0.5126 | 0.4708 | 0.4832 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 38 | team5 | run1 | team5_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.4357 | 0.3747 | 0.5336 | 0.4967 | 0.5882 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 39 | random | run1 | random_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.4355 | 0.3449 | 0.4118 | 0.5262 | 0.5168 | [Comparison](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 40 | team15 | run1 | team15_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.4333 | 0.3667 | 0.4958 | 0.5 | 0.6597 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 41 | team4 | run1 | team4_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.4275 | 0.3494 | 0.4328 | 0.5056 | 0.5882 | [Comparison](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 42 | team10 | run1 | team10_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.4208 | 0.3387 | 0.5672 | 0.503 | 0.6597 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 43 | team14 | run2 | team14_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.4073 | 0.3278 | 0.5294 | 0.4869 | 0.6345 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 44 | team7 | run3 | team7_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 0.393 | 0.2757 | 0.416 | 0.5104 | 0.563 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 45 | team7 | run2 | team7_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 0.3896 | 0.2714 | 0.416 | 0.5078 | 0.5714 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 46 | team7 | run1 | team7_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 0.3849 | 0.2717 | 0.4118 | 0.4981 | 0.5546 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |

Top 3 teams by best run:

1. Spinfo (team13), run1, table rank 1, impresso profile score 0.7551
2. Awakened (team1), run1, table rank 4, impresso profile score 0.7163
3. MaxFo-Ajie (team8), run1, table rank 6, impresso profile score 0.679

## Generalization Profile Ranking

| rank | team | run | submission | surprise profile score | diagnostics |
| --- | --- | --- | --- | --- | --- |
| 1 | team8 | run3 | team8_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.8163 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 2 | team8 | run1 | team8_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.7945 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 3 | team8 | run2 | team8_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.7712 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 4 | team13 | run3 | team13_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.6984 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 5 | team13 | run1 | team13_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.691 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 6 | team10 | run1 | team10_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.6837 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 7 | team13 | run2 | team13_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.6674 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 8 | team12 | run2 | team12_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.6665 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 9 | team11 | run2 | team11_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.6647 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 10 | team1 | run3 | team1_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.6613 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 11 | team9 | run2 | team9_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.6349 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 12 | team1 | run1 | team1_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.6338 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 13 | team12 | run1 | team12_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.6325 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 14 | team9 | run3 | team9_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.6187 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 15 | team9 | run1 | team9_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.6107 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 16 | team11 | run1 | team11_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.6085 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 17 | team10 | run3 | team10_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.6 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 18 | team3 | run3 | team3_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.5724 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 19 | team5 | run2 | team5_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.5723 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 20 | team1 | run2 | team1_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.5509 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 21 | team11 | run3 | team11_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.5382 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 22 | team10 | run2 | team10_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.5265 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 23 | team14 | run3 | team14_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.5152 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 24 | team3 | run2 | team3_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.5076 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 25 | baseline | run1 | baseline_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.5062 | [Comparison](results.d/diagnostics/baseline_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/baseline_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 26 | team17 | run1 | team17_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.4705 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 27 | team14 | run1 | team14_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.4679 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 28 | team3 | run1 | team3_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.4419 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 29 | team17 | run2 | team17_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.4231 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 30 | team17 | run3 | team17_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.3986 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 31 | team2 | run3 | team2_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.3919 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 32 | team7 | run3 | team7_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.384 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 33 | team7 | run1 | team7_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3773 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 34 | team15 | run2 | team15_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.3755 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 35 | team14 | run2 | team14_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.3742 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 36 | team6 | run2 | team6_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.3726 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 37 | team2 | run2 | team2_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.3721 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 38 | team7 | run2 | team7_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.366 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 39 | random | run1 | random_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3628 | [Comparison](results.d/diagnostics/random_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/random_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 40 | team2 | run1 | team2_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3626 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 41 | team5 | run3 | team5_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.362 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 42 | team15 | run1 | team15_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.358 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 43 | team15 | run3 | team15_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.3546 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 44 | team4 | run1 | team4_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3445 | [Comparison](results.d/diagnostics/team4_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team4_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 45 | team6 | run1 | team6_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3346 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 46 | team5 | run1 | team5_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3333 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |

Top 3 teams by best run:

1. MaxFo-Ajie (team8), run3, table rank 1, surprise profile score 0.8163
2. Spinfo (team13), run3, table rank 4, surprise profile score 0.6984
3. BIU_NLP (team10), run1, table rank 6, surprise profile score 0.6837

## Generalization Profile Ranking French

| rank | team | run | submission | surprise profile score | at macro recall | at accuracy | diagnostics |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | team8 | run3 | team8_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.8163 | 0.8163 | 0.8729 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 2 | team8 | run1 | team8_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.7945 | 0.7945 | 0.8625 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 3 | team8 | run2 | team8_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.7712 | 0.7712 | 0.8542 | [Comparison](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team8_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 4 | team13 | run3 | team13_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.6984 | 0.6984 | 0.8104 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 5 | team13 | run1 | team13_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.691 | 0.691 | 0.7729 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 6 | team10 | run1 | team10_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.6837 | 0.6837 | 0.8354 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 7 | team13 | run2 | team13_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.6674 | 0.6674 | 0.7458 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 8 | team12 | run2 | team12_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.6665 | 0.6665 | 0.8333 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 9 | team11 | run2 | team11_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.6647 | 0.6647 | 0.7458 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 10 | team1 | run3 | team1_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.6613 | 0.6613 | 0.7292 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 11 | team9 | run2 | team9_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.6349 | 0.6349 | 0.6438 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 12 | team1 | run1 | team1_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.6338 | 0.6338 | 0.725 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 13 | team12 | run1 | team12_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.6325 | 0.6325 | 0.8167 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 14 | team9 | run3 | team9_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.6187 | 0.6187 | 0.7708 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 15 | team9 | run1 | team9_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.6107 | 0.6107 | 0.6896 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 16 | team11 | run1 | team11_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.6085 | 0.6085 | 0.75 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 17 | team10 | run3 | team10_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.6 | 0.6 | 0.6042 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 18 | team3 | run3 | team3_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.5724 | 0.5724 | 0.7708 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 19 | team5 | run2 | team5_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.5723 | 0.5723 | 0.575 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 20 | team1 | run2 | team1_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.5509 | 0.5509 | 0.5625 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 21 | team11 | run3 | team11_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.5382 | 0.5382 | 0.6375 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 22 | team10 | run2 | team10_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.5265 | 0.5265 | 0.4729 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 23 | team14 | run3 | team14_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.5152 | 0.5152 | 0.5646 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 24 | team3 | run2 | team3_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.5076 | 0.5076 | 0.6937 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 25 | baseline | run1 | baseline_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.5062 | 0.5062 | 0.5583 | [Comparison](results.d/diagnostics/baseline_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/baseline_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 26 | team17 | run1 | team17_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.4705 | 0.4705 | 0.6604 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 27 | team14 | run1 | team14_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.4679 | 0.4679 | 0.6583 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 28 | team3 | run1 | team3_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.4419 | 0.4419 | 0.6292 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 29 | team17 | run2 | team17_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.4231 | 0.4231 | 0.6438 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 30 | team17 | run3 | team17_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.3986 | 0.3986 | 0.6375 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 31 | team2 | run3 | team2_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.3919 | 0.3919 | 0.5 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 32 | team7 | run3 | team7_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.384 | 0.384 | 0.5104 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 33 | team7 | run1 | team7_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3773 | 0.3773 | 0.5062 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 34 | team15 | run2 | team15_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.3755 | 0.3755 | 0.3729 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 35 | team14 | run2 | team14_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.3742 | 0.3742 | 0.575 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 36 | team6 | run2 | team6_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.3726 | 0.3726 | 0.4542 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 37 | team2 | run2 | team2_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.3721 | 0.3721 | 0.5 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 38 | team7 | run2 | team7_HIPE-2026-v1.0-surprise-test-fr_run2.jsonl | 0.366 | 0.366 | 0.4938 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-surprise-test-fr_run2.diagnostic_metrics.json) |
| 39 | random | run1 | random_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3628 | 0.3628 | 0.3604 | [Comparison](results.d/diagnostics/random_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/random_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 40 | team2 | run1 | team2_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3626 | 0.3626 | 0.3708 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 41 | team5 | run3 | team5_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.362 | 0.362 | 0.3104 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 42 | team15 | run1 | team15_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.358 | 0.358 | 0.4437 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 43 | team15 | run3 | team15_HIPE-2026-v1.0-surprise-test-fr_run3.jsonl | 0.3546 | 0.3546 | 0.4813 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-surprise-test-fr_run3.diagnostic_metrics.json) |
| 44 | team4 | run1 | team4_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3445 | 0.3445 | 0.2667 | [Comparison](results.d/diagnostics/team4_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team4_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 45 | team6 | run1 | team6_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3346 | 0.3346 | 0.5375 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |
| 46 | team5 | run1 | team5_HIPE-2026-v1.0-surprise-test-fr_run1.jsonl | 0.3333 | 0.3333 | 0.6042 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-surprise-test-fr_run1.diagnostic_metrics.json) |

Top 3 teams by best run:

1. MaxFo-Ajie (team8), run3, table rank 1, surprise profile score 0.8163
2. Spinfo (team13), run3, table rank 4, surprise profile score 0.6984
3. BIU_NLP (team10), run1, table rank 6, surprise profile score 0.6837

## Efficiency Profile Ranking Overall

| rank | team | run | mean efficiency profile rank | rank impresso profile score | rank hipe parameter count | rank hipe model size | mean impresso profile score | hipe parameter count | hipe model size mb |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | team14 | run3 | 9.6667 | 12 | 8 | 9 | 0.5951 | 277730309 | 1111 |
| 2 | team15 | run2 | 10.3333 | 29 | 1 | 1 | 0.4734 | 0 | 0 |
| 3 | team2 | run1 | 10.6667 | 23 | 5 | 4 | 0.5142 | 2087375 | 87 |
| 4 | team2 | run2 | 12 | 27 | 5 | 4 | 0.4836 | 2087375 | 87 |
| 5 | team2 | run3 | 12.3333 | 28 | 5 | 4 | 0.4771 | 2087375 | 87 |
| 6 | team14 | run1 | 13.6667 | 18 | 12 | 11 | 0.5623 | 466577920 | 1780 |
| 6 | team7 | run1 | 13.6667 | 37 | 2 | 2 | 0.446 | 12279 | 0.8 |
| 6 | team7 | run2 | 13.6667 | 35 | 3 | 3 | 0.4507 | 12365 | 0.81 |
| 6 | team7 | run3 | 13.6667 | 34 | 4 | 3 | 0.4564 | 12399 | 0.81 |
| 7 | random | run1 | 15 | 43 | 1 | 1 | 0.4049 | 0 | 0 |
| 8 | team1 | run2 | 15.3333 | 19 | 14 | 13 | 0.5494 | 560965127 | 2140 |
| 9 | baseline | run1 | 15.6667 | 14 | 19 | 14 | 0.5818 | 3000000000 | 2147.023 |
| 9 | team6 | run2 | 15.6667 | 26 | 11 | 10 | 0.4842 | 355000000 | 1424 |
| 10 | team17 | run2 | 16 | 31 | 9 | 8 | 0.4708 | 278043651 | 1061 |
| 11 | team12 | run1 | 16.6667 | 4 | 22 | 24 | 0.688 | 5123178979 | 9600 |
| 12 | team12 | run2 | 17 | 5 | 22 | 24 | 0.6833 | 5123178979 | 9600 |
| 12 | team15 | run1 | 17 | 40 | 6 | 5 | 0.427 | 208935168 | 816 |
| 12 | team3 | run3 | 17 | 15 | 20 | 16 | 0.5795 | 4000000000 | 2840 |
| 13 | team5 | run1 | 17.3333 | 39 | 7 | 6 | 0.4408 | 270000000 | 1030 |
| 14 | team11 | run2 | 17.6667 | 9 | 21 | 23 | 0.6271 | 4465470464 | 9012 |
| 15 | team6 | run1 | 18 | 33 | 11 | 10 | 0.4628 | 355000000 | 1424 |
| 16 | team5 | run2 | 18.3333 | 13 | 20 | 22 | 0.5856 | 4000000000 | 7600 |
| 17 | team3 | run1 | 18.6667 | 25 | 16 | 15 | 0.5004 | 1500000000 | 2340 |
| 18 | team11 | run3 | 19.6667 | 24 | 17 | 18 | 0.5069 | 1949101888 | 3845 |
| 18 | team4 | run1 | 19.6667 | 42 | 10 | 7 | 0.4061 | 278054405 | 1060 |
| 19 | team9 | run1 | 20 | 20 | 19 | 21 | 0.5458 | 3000000000 | 6248 |
| 20 | team13 | run1 | 20.3333 | 1 | 30 | 30 | 0.7479 | 116830000000 | 65238 |
| 21 | team11 | run1 | 20.6667 | 11 | 25 | 26 | 0.6141 | 9300029952 | 18398 |
| 21 | team13 | run3 | 20.6667 | 2 | 30 | 30 | 0.7289 | 116830000000 | 65238 |
| 21 | team17 | run3 | 20.6667 | 30 | 15 | 17 | 0.4731 | 838778678 | 3217 |
| 22 | team13 | run2 | 21 | 3 | 30 | 30 | 0.689 | 116830000000 | 65238 |
| 23 | team3 | run2 | 21.6667 | 22 | 23 | 20 | 0.5187 | 5900000000 | 5980 |
| 23 | team9 | run2 | 21.6667 | 16 | 24 | 25 | 0.5788 | 7000000000 | 15300 |
| 24 | team14 | run2 | 22 | 41 | 13 | 12 | 0.4264 | 466585989 | 1866 |
| 25 | team17 | run1 | 22.6667 | 8 | 29 | 31 | 0.639 | 101927226758 | 195716 |
| 26 | team15 | run3 | 23 | 32 | 18 | 19 | 0.4645 | 2274069824 | 4442 |
| 27 | team1 | run3 | 23.6667 | 6 | 32 | 33 | 0.6671 | 999999999999 | 999999 |
| 28 | team1 | run1 | 24 | 7 | 32 | 33 | 0.6584 | 999999999999 | 999999 |
| 29 | team9 | run3 | 24.3333 | 10 | 31 | 32 | 0.6221 | 120000000000 | 240000 |
| 30 | team10 | run2 | 24.6667 | 17 | 28 | 29 | 0.5781 | 27000000000 | 54000 |
| 30 | team10 | run3 | 24.6667 | 21 | 26 | 27 | 0.539 | 24000000000 | 48000 |
| 31 | team5 | run3 | 26 | 36 | 20 | 22 | 0.4495 | 4000000000 | 7600 |
| 32 | team10 | run1 | 31 | 38 | 27 | 28 | 0.4429 | 26000000000 | 52000 |

Top 3 teams by best run:

1. MILRIT (team14), run3, table rank 1, mean efficiency profile rank 9.6667
2. FI Code (team15), run2, table rank 2, mean efficiency profile rank 10.3333
3. DS@GT_HIPE (team2), run1, table rank 3, mean efficiency profile rank 10.6667

## Balanced Efficiency Profile Ranking Overall

| rank | team | run | balanced efficiency profile rank | rank impresso profile score | rank hipe parameter count | rank hipe model size | mean impresso profile score | hipe parameter count | hipe model size mb |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | team14 | run3 | 10.25 | 12 | 8 | 9 | 0.5951 | 277730309 | 1111 |
| 2 | team12 | run1 | 13.5 | 4 | 22 | 24 | 0.688 | 5123178979 | 9600 |
| 3 | team2 | run1 | 13.75 | 23 | 5 | 4 | 0.5142 | 2087375 | 87 |
| 4 | team12 | run2 | 14 | 5 | 22 | 24 | 0.6833 | 5123178979 | 9600 |
| 5 | team14 | run1 | 14.75 | 18 | 12 | 11 | 0.5623 | 466577920 | 1780 |
| 6 | team15 | run2 | 15 | 29 | 1 | 1 | 0.4734 | 0 | 0 |
| 7 | baseline | run1 | 15.25 | 14 | 19 | 14 | 0.5818 | 3000000000 | 2147.023 |
| 8 | team11 | run2 | 15.5 | 9 | 21 | 23 | 0.6271 | 4465470464 | 9012 |
| 8 | team13 | run1 | 15.5 | 1 | 30 | 30 | 0.7479 | 116830000000 | 65238 |
| 9 | team2 | run2 | 15.75 | 27 | 5 | 4 | 0.4836 | 2087375 | 87 |
| 10 | team13 | run3 | 16 | 2 | 30 | 30 | 0.7289 | 116830000000 | 65238 |
| 11 | team1 | run2 | 16.25 | 19 | 14 | 13 | 0.5494 | 560965127 | 2140 |
| 11 | team2 | run3 | 16.25 | 28 | 5 | 4 | 0.4771 | 2087375 | 87 |
| 12 | team13 | run2 | 16.5 | 3 | 30 | 30 | 0.689 | 116830000000 | 65238 |
| 12 | team3 | run3 | 16.5 | 15 | 20 | 16 | 0.5795 | 4000000000 | 2840 |
| 13 | team5 | run2 | 17 | 13 | 20 | 22 | 0.5856 | 4000000000 | 7600 |
| 14 | team11 | run1 | 18.25 | 11 | 25 | 26 | 0.6141 | 9300029952 | 18398 |
| 14 | team6 | run2 | 18.25 | 26 | 11 | 10 | 0.4842 | 355000000 | 1424 |
| 15 | team7 | run3 | 18.75 | 34 | 4 | 3 | 0.4564 | 12399 | 0.81 |
| 16 | team17 | run1 | 19 | 8 | 29 | 31 | 0.639 | 101927226758 | 195716 |
| 16 | team7 | run2 | 19 | 35 | 3 | 3 | 0.4507 | 12365 | 0.81 |
| 17 | team1 | run3 | 19.25 | 6 | 32 | 33 | 0.6671 | 999999999999 | 999999 |
| 18 | team7 | run1 | 19.5 | 37 | 2 | 2 | 0.446 | 12279 | 0.8 |
| 19 | team1 | run1 | 19.75 | 7 | 32 | 33 | 0.6584 | 999999999999 | 999999 |
| 19 | team17 | run2 | 19.75 | 31 | 9 | 8 | 0.4708 | 278043651 | 1061 |
| 20 | team9 | run1 | 20 | 20 | 19 | 21 | 0.5458 | 3000000000 | 6248 |
| 21 | team3 | run1 | 20.25 | 25 | 16 | 15 | 0.5004 | 1500000000 | 2340 |
| 21 | team9 | run2 | 20.25 | 16 | 24 | 25 | 0.5788 | 7000000000 | 15300 |
| 22 | team11 | run3 | 20.75 | 24 | 17 | 18 | 0.5069 | 1949101888 | 3845 |
| 22 | team9 | run3 | 20.75 | 10 | 31 | 32 | 0.6221 | 120000000000 | 240000 |
| 23 | team3 | run2 | 21.75 | 22 | 23 | 20 | 0.5187 | 5900000000 | 5980 |
| 23 | team6 | run1 | 21.75 | 33 | 11 | 10 | 0.4628 | 355000000 | 1424 |
| 24 | random | run1 | 22 | 43 | 1 | 1 | 0.4049 | 0 | 0 |
| 25 | team10 | run2 | 22.75 | 17 | 28 | 29 | 0.5781 | 27000000000 | 54000 |
| 25 | team15 | run1 | 22.75 | 40 | 6 | 5 | 0.427 | 208935168 | 816 |
| 25 | team5 | run1 | 22.75 | 39 | 7 | 6 | 0.4408 | 270000000 | 1030 |
| 26 | team17 | run3 | 23 | 30 | 15 | 17 | 0.4731 | 838778678 | 3217 |
| 27 | team10 | run3 | 23.75 | 21 | 26 | 27 | 0.539 | 24000000000 | 48000 |
| 28 | team15 | run3 | 25.25 | 32 | 18 | 19 | 0.4645 | 2274069824 | 4442 |
| 28 | team4 | run1 | 25.25 | 42 | 10 | 7 | 0.4061 | 278054405 | 1060 |
| 29 | team14 | run2 | 26.75 | 41 | 13 | 12 | 0.4264 | 466585989 | 1866 |
| 30 | team5 | run3 | 28.5 | 36 | 20 | 22 | 0.4495 | 4000000000 | 7600 |
| 31 | team10 | run1 | 32.75 | 38 | 27 | 28 | 0.4429 | 26000000000 | 52000 |

Top 3 teams by best run:

1. MILRIT (team14), run3, table rank 1, balanced efficiency profile rank 10.25
2. whereami (team12), run1, table rank 2, balanced efficiency profile rank 13.5
3. DS@GT_HIPE (team2), run1, table rank 3, balanced efficiency profile rank 13.75

This is an additional analysis ranking. It is not the guideline-defined Efficiency Profile Ranking; it gives equal total weight to accuracy and to the combined resource ranks.

## Efficiency Profile Ranking German

| rank | team | run | submission | mean efficiency profile rank | rank impresso profile score | rank hipe parameter count | rank hipe model size | impresso profile score | hipe parameter count | hipe model size mb | diagnostics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | team7 | run1 | team7_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 8.6667 | 22 | 2 | 2 | 0.5196 | 12279 | 0.8 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 2 | team7 | run3 | team7_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 9 | 20 | 4 | 3 | 0.5222 | 12399 | 0.81 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 3 | team7 | run2 | team7_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 9.6667 | 23 | 3 | 3 | 0.5192 | 12365 | 0.81 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 4 | team14 | run3 | team14_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 10 | 13 | 8 | 9 | 0.5886 | 277730309 | 1111 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 5 | team15 | run2 | team15_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 11.3333 | 32 | 1 | 1 | 0.4678 | 0 | 0 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 5 | team2 | run1 | team2_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 11.3333 | 25 | 5 | 4 | 0.516 | 2087375 | 87 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 6 | team2 | run3 | team2_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 12 | 27 | 5 | 4 | 0.5054 | 2087375 | 87 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 7 | team14 | run1 | team14_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 12.3333 | 14 | 12 | 11 | 0.5802 | 466577920 | 1780 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 8 | team2 | run2 | team2_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 13 | 30 | 5 | 4 | 0.4937 | 2087375 | 87 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 9 | random | run1 | random_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 14.6667 | 42 | 1 | 1 | 0.4058 | 0 | 0 | [Comparison](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 10 | team1 | run2 | team1_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 15 | 18 | 14 | 13 | 0.5417 | 560965127 | 2140 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 11 | team6 | run2 | team6_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 15.6667 | 26 | 11 | 10 | 0.5071 | 355000000 | 1424 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 12 | baseline | run1 | baseline_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 16.3333 | 16 | 19 | 14 | 0.5553 | 3000000000 | 2147.023 | [Comparison](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 12 | team12 | run2 | team12_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 16.3333 | 3 | 22 | 24 | 0.7072 | 5123178979 | 9600 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 13 | team12 | run1 | team12_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 16.6667 | 4 | 22 | 24 | 0.7041 | 5123178979 | 9600 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 14 | team3 | run3 | team3_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 17 | 15 | 20 | 16 | 0.5697 | 4000000000 | 2840 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 14 | team5 | run2 | team5_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 17 | 9 | 20 | 22 | 0.6305 | 4000000000 | 7600 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 15 | team15 | run1 | team15_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 17.3333 | 41 | 6 | 5 | 0.4162 | 208935168 | 816 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 16 | team17 | run2 | team17_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 17.6667 | 36 | 9 | 8 | 0.4435 | 278043651 | 1061 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 16 | team5 | run1 | team5_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 17.6667 | 40 | 7 | 6 | 0.4167 | 270000000 | 1030 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 17 | team11 | run2 | team11_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 18.6667 | 12 | 21 | 23 | 0.5941 | 4465470464 | 9012 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 17 | team6 | run1 | team6_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 18.6667 | 35 | 11 | 10 | 0.4488 | 355000000 | 1424 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 18 | team11 | run3 | team11_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 19.6667 | 24 | 17 | 18 | 0.5181 | 1949101888 | 3845 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 19 | team4 | run1 | team4_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 20 | 43 | 10 | 7 | 0.372 | 278054405 | 1060 | [Comparison](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 20 | team13 | run3 | team13_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 20.3333 | 1 | 30 | 30 | 0.771 | 116830000000 | 65238 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 20 | team9 | run1 | team9_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 20.3333 | 21 | 19 | 21 | 0.521 | 3000000000 | 6248 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 21 | team11 | run1 | team11_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 20.6667 | 11 | 25 | 26 | 0.5957 | 9300029952 | 18398 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 21 | team13 | run1 | team13_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 20.6667 | 2 | 30 | 30 | 0.7608 | 116830000000 | 65238 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 21 | team3 | run1 | team3_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 20.6667 | 31 | 16 | 15 | 0.4808 | 1500000000 | 2340 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 22 | team14 | run2 | team14_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 21 | 38 | 13 | 12 | 0.4365 | 466585989 | 1866 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 23 | team13 | run2 | team13_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 21.6667 | 5 | 30 | 30 | 0.686 | 116830000000 | 65238 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 24 | team17 | run1 | team17_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 22.6667 | 8 | 29 | 31 | 0.6725 | 101927226758 | 195716 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 24 | team9 | run2 | team9_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 22.6667 | 19 | 24 | 25 | 0.5254 | 7000000000 | 15300 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 25 | team10 | run3 | team10_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 23.3333 | 17 | 26 | 27 | 0.5451 | 24000000000 | 48000 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 26 | team1 | run3 | team1_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 23.6667 | 6 | 32 | 33 | 0.6746 | 999999999999 | 999999 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 26 | team17 | run3 | team17_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 23.6667 | 39 | 15 | 17 | 0.4351 | 838778678 | 3217 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 27 | team1 | run1 | team1_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 24 | 7 | 32 | 33 | 0.6739 | 999999999999 | 999999 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |
| 27 | team3 | run2 | team3_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 24 | 29 | 23 | 20 | 0.5022 | 5900000000 | 5980 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 28 | team9 | run3 | team9_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 24.3333 | 10 | 31 | 32 | 0.5994 | 120000000000 | 240000 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 29 | team15 | run3 | team15_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 24.6667 | 37 | 18 | 19 | 0.4378 | 2274069824 | 4442 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 30 | team5 | run3 | team5_HIPE-2026-v1.0-impresso-test-de_run3.jsonl | 25 | 33 | 20 | 22 | 0.4527 | 4000000000 | 7600 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-de_run3.diagnostic_metrics.json) |
| 31 | team10 | run2 | team10_HIPE-2026-v1.0-impresso-test-de_run2.jsonl | 28.3333 | 28 | 28 | 29 | 0.505 | 27000000000 | 54000 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run2.diagnostic_metrics.json) |
| 32 | team10 | run1 | team10_HIPE-2026-v1.0-impresso-test-de_run1.jsonl | 29.6667 | 34 | 27 | 28 | 0.4495 | 26000000000 | 52000 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-de_run1.diagnostic_metrics.json) |

Top 3 teams by best run:

1. ROSTI (team7), run1, table rank 1, mean efficiency profile rank 8.6667
2. MILRIT (team14), run3, table rank 4, mean efficiency profile rank 10
3. FI Code (team15), run2, table rank 5, mean efficiency profile rank 11.3333

## Efficiency Profile Ranking English

| rank | team | run | submission | mean efficiency profile rank | rank impresso profile score | rank hipe parameter count | rank hipe model size | impresso profile score | hipe parameter count | hipe model size mb | diagnostics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | team14 | run3 | team14_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 10.3333 | 12 | 9 | 10 | 0.5881 | 277730309 | 1111 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 2 | team15 | run2 | team15_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 11.3333 | 32 | 1 | 1 | 0.4624 | 0 | 0 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 2 | team2 | run1 | team2_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 11.3333 | 24 | 6 | 4 | 0.5103 | 2087375 | 87 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 3 | team2 | run3 | team2_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 12.3333 | 27 | 6 | 4 | 0.4834 | 2087375 | 87 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 4 | team17 | run2 | team17_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 13.6667 | 22 | 10 | 9 | 0.5128 | 278043651 | 1061 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 5 | team7 | run3 | team7_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 14 | 34 | 5 | 3 | 0.4541 | 12399 | 0.81 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 6 | team7 | run2 | team7_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 14.3333 | 36 | 4 | 3 | 0.4431 | 12365 | 0.81 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 7 | team7 | run1 | team7_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 14.6667 | 39 | 3 | 2 | 0.4335 | 12279 | 0.8 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 8 | random | run1 | random_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 15.3333 | 44 | 1 | 1 | 0.3733 | 0 | 0 | [Comparison](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 8 | team5 | run1 | team5_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 15.3333 | 31 | 8 | 7 | 0.4702 | 270000000 | 1030 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 9 | team2 | run2 | team2_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 15.6667 | 37 | 6 | 4 | 0.4401 | 2087375 | 87 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 10 | team16 | run1 | team16_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 16.3333 | 42 | 2 | 5 | 0.4254 | 110 | 433 | [Comparison](results.d/diagnostics/team16_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team16_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 11 | team12 | run1 | team12_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 16.6667 | 2 | 23 | 25 | 0.7023 | 5123178979 | 9600 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 12 | team12 | run2 | team12_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 17 | 3 | 23 | 25 | 0.6992 | 5123178979 | 9600 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 12 | team3 | run1 | team3_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 17 | 18 | 17 | 16 | 0.5607 | 1500000000 | 2340 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 12 | team6 | run2 | team6_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 17 | 28 | 12 | 11 | 0.4808 | 355000000 | 1424 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 13 | team15 | run1 | team15_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 17.6667 | 40 | 7 | 6 | 0.4313 | 208935168 | 816 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 13 | team3 | run3 | team3_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 17.6667 | 15 | 21 | 17 | 0.5812 | 4000000000 | 2840 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 13 | team6 | run1 | team6_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 17.6667 | 30 | 12 | 11 | 0.4757 | 355000000 | 1424 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 13 | team9 | run1 | team9_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 17.6667 | 11 | 20 | 22 | 0.5976 | 3000000000 | 6248 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 14 | baseline | run1 | baseline_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 18 | 19 | 20 | 15 | 0.5551 | 3000000000 | 2147.023 | [Comparison](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 14 | team11 | run2 | team11_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 18 | 8 | 22 | 24 | 0.6174 | 4465470464 | 9012 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 14 | team14 | run1 | team14_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 18 | 29 | 13 | 12 | 0.4808 | 466577920 | 1780 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 15 | team1 | run2 | team1_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 18.3333 | 26 | 15 | 14 | 0.4989 | 560965127 | 2140 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 16 | team17 | run3 | team17_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 19 | 23 | 16 | 18 | 0.5107 | 838778678 | 3217 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 17 | team11 | run3 | team11_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 19.3333 | 21 | 18 | 19 | 0.5221 | 1949101888 | 3845 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 18 | team11 | run1 | team11_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 20.6667 | 9 | 26 | 27 | 0.6143 | 9300029952 | 18398 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 18 | team3 | run2 | team3_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 20.6667 | 17 | 24 | 21 | 0.5718 | 5900000000 | 5980 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 18 | team4 | run1 | team4_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 20.6667 | 43 | 11 | 8 | 0.4187 | 278054405 | 1060 | [Comparison](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 19 | team13 | run1 | team13_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 21 | 1 | 31 | 31 | 0.7279 | 116830000000 | 65238 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 20 | team5 | run2 | team5_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 21.3333 | 20 | 21 | 23 | 0.5384 | 4000000000 | 7600 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 20 | team9 | run2 | team9_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 21.3333 | 13 | 25 | 26 | 0.5866 | 7000000000 | 15300 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 21 | team14 | run2 | team14_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 21.6667 | 38 | 14 | 13 | 0.4353 | 466585989 | 1866 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 22 | team13 | run3 | team13_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 22 | 4 | 31 | 31 | 0.6808 | 116830000000 | 65238 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 23 | team13 | run2 | team13_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 22.3333 | 5 | 31 | 31 | 0.6427 | 116830000000 | 65238 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 24 | team17 | run1 | team17_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 24 | 10 | 30 | 32 | 0.5985 | 101927226758 | 195716 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 24 | team9 | run3 | team9_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 24 | 7 | 32 | 33 | 0.6367 | 120000000000 | 240000 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 25 | team1 | run3 | team1_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 24.3333 | 6 | 33 | 34 | 0.6415 | 999999999999 | 999999 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 26 | team15 | run3 | team15_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 24.6667 | 35 | 19 | 20 | 0.4466 | 2274069824 | 4442 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 27 | team10 | run2 | team10_HIPE-2026-v1.0-impresso-test-en_run2.jsonl | 25 | 16 | 29 | 30 | 0.5762 | 27000000000 | 54000 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run2.diagnostic_metrics.json) |
| 28 | team10 | run3 | team10_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 26.6667 | 25 | 27 | 28 | 0.5101 | 24000000000 | 48000 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 29 | team1 | run1 | team1_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 27 | 14 | 33 | 34 | 0.5848 | 999999999999 | 999999 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |
| 30 | team5 | run3 | team5_HIPE-2026-v1.0-impresso-test-en_run3.jsonl | 28.3333 | 41 | 21 | 23 | 0.4312 | 4000000000 | 7600 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-en_run3.diagnostic_metrics.json) |
| 31 | team10 | run1 | team10_HIPE-2026-v1.0-impresso-test-en_run1.jsonl | 30 | 33 | 28 | 29 | 0.4583 | 26000000000 | 52000 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-en_run1.diagnostic_metrics.json) |

Top 3 teams by best run:

1. MILRIT (team14), run3, table rank 1, mean efficiency profile rank 10.3333
2. FI Code (team15), run2, table rank 2, mean efficiency profile rank 11.3333
3. DS@GT_HIPE (team2), run1, table rank 2, mean efficiency profile rank 11.3333

## Efficiency Profile Ranking French

| rank | team | run | submission | mean efficiency profile rank | rank impresso profile score | rank hipe parameter count | rank hipe model size | impresso profile score | hipe parameter count | hipe model size mb | diagnostics |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | team15 | run2 | team15_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 9 | 25 | 1 | 1 | 0.4902 | 0 | 0 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 2 | team2 | run2 | team2_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 10.3333 | 22 | 5 | 4 | 0.5171 | 2087375 | 87 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 3 | team2 | run1 | team2_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 10.6667 | 23 | 5 | 4 | 0.5162 | 2087375 | 87 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 4 | team14 | run3 | team14_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 11 | 16 | 8 | 9 | 0.6087 | 277730309 | 1111 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 5 | team14 | run1 | team14_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 12.3333 | 14 | 12 | 11 | 0.6261 | 466577920 | 1780 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 6 | random | run1 | random_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 12.6667 | 36 | 1 | 1 | 0.4355 | 0 | 0 | [Comparison](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/random_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 7 | team2 | run3 | team2_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 14.3333 | 34 | 5 | 4 | 0.4424 | 2087375 | 87 | [Comparison](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team2_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 8 | baseline | run1 | baseline_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 14.6667 | 11 | 19 | 14 | 0.6349 | 3000000000 | 2147.023 | [Comparison](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/baseline_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 8 | team1 | run2 | team1_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 14.6667 | 17 | 14 | 13 | 0.6076 | 560965127 | 2140 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 9 | team7 | run1 | team7_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 15.6667 | 43 | 2 | 2 | 0.3849 | 12279 | 0.8 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 10 | team15 | run1 | team15_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 16 | 37 | 6 | 5 | 0.4333 | 208935168 | 816 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 10 | team5 | run1 | team5_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 16 | 35 | 7 | 6 | 0.4357 | 270000000 | 1030 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 10 | team7 | run2 | team7_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 16 | 42 | 3 | 3 | 0.3896 | 12365 | 0.81 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 10 | team7 | run3 | team7_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 16 | 41 | 4 | 3 | 0.393 | 12399 | 0.81 | [Comparison](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team7_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 11 | team11 | run2 | team11_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 16.6667 | 6 | 21 | 23 | 0.6697 | 4465470464 | 9012 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 11 | team17 | run2 | team17_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 16.6667 | 33 | 9 | 8 | 0.4561 | 278043651 | 1061 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 11 | team6 | run2 | team6_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 16.6667 | 29 | 11 | 10 | 0.4648 | 355000000 | 1424 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 12 | team6 | run1 | team6_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 17.3333 | 31 | 11 | 10 | 0.464 | 355000000 | 1424 | [Comparison](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team6_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 13 | team12 | run1 | team12_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 17.6667 | 7 | 22 | 24 | 0.6578 | 5123178979 | 9600 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 14 | team3 | run3 | team3_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 18.3333 | 19 | 20 | 16 | 0.5877 | 4000000000 | 2840 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 14 | team4 | run1 | team4_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 18.3333 | 38 | 10 | 7 | 0.4275 | 278054405 | 1060 | [Comparison](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team4_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 15 | team12 | run2 | team12_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 18.6667 | 10 | 22 | 24 | 0.6435 | 5123178979 | 9600 | [Comparison](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team12_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 16 | team17 | run3 | team17_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 20 | 28 | 15 | 17 | 0.4734 | 838778678 | 3217 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 16 | team5 | run2 | team5_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 20 | 18 | 20 | 22 | 0.588 | 4000000000 | 7600 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 17 | team13 | run1 | team13_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 20.3333 | 1 | 30 | 30 | 0.7551 | 116830000000 | 65238 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 17 | team15 | run3 | team15_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 20.3333 | 24 | 18 | 19 | 0.5091 | 2274069824 | 4442 | [Comparison](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team15_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 17 | team9 | run1 | team9_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 20.3333 | 21 | 19 | 21 | 0.5189 | 3000000000 | 6248 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 18 | team11 | run3 | team11_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 20.6667 | 27 | 17 | 18 | 0.4805 | 1949101888 | 3845 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 18 | team13 | run2 | team13_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 20.6667 | 2 | 30 | 30 | 0.7383 | 116830000000 | 65238 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 19 | team11 | run1 | team11_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 21 | 12 | 25 | 26 | 0.6322 | 9300029952 | 18398 | [Comparison](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team11_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 19 | team13 | run3 | team13_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 21 | 3 | 30 | 30 | 0.7349 | 116830000000 | 65238 | [Comparison](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team13_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 19 | team3 | run1 | team3_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 21 | 32 | 16 | 15 | 0.4597 | 1500000000 | 2340 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 20 | team9 | run2 | team9_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 21.3333 | 15 | 24 | 25 | 0.6243 | 7000000000 | 15300 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 21 | team10 | run2 | team10_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 21.6667 | 8 | 28 | 29 | 0.6529 | 27000000000 | 54000 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 21 | team14 | run2 | team14_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 21.6667 | 40 | 13 | 12 | 0.4073 | 466585989 | 1866 | [Comparison](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team14_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 22 | team1 | run1 | team1_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 23 | 4 | 32 | 33 | 0.7163 | 999999999999 | 999999 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 22 | team17 | run1 | team17_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 23 | 9 | 29 | 31 | 0.6459 | 101927226758 | 195716 | [Comparison](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team17_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |
| 22 | team3 | run2 | team3_HIPE-2026-v1.0-impresso-test-fr_run2.jsonl | 23 | 26 | 23 | 20 | 0.4822 | 5900000000 | 5980 | [Comparison](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostics.json) / [Metrics](results.d/diagnostics/team3_HIPE-2026-v1.0-impresso-test-fr_run2.diagnostic_metrics.json) |
| 23 | team1 | run3 | team1_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 23.3333 | 5 | 32 | 33 | 0.6854 | 999999999999 | 999999 | [Comparison](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team1_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 24 | team5 | run3 | team5_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 24 | 30 | 20 | 22 | 0.4645 | 4000000000 | 7600 | [Comparison](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team5_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 25 | team10 | run3 | team10_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 24.3333 | 20 | 26 | 27 | 0.5617 | 24000000000 | 48000 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 26 | team9 | run3 | team9_HIPE-2026-v1.0-impresso-test-fr_run3.jsonl | 25.3333 | 13 | 31 | 32 | 0.6303 | 120000000000 | 240000 | [Comparison](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostics.json) / [Metrics](results.d/diagnostics/team9_HIPE-2026-v1.0-impresso-test-fr_run3.diagnostic_metrics.json) |
| 27 | team10 | run1 | team10_HIPE-2026-v1.0-impresso-test-fr_run1.jsonl | 31.3333 | 39 | 27 | 28 | 0.4208 | 26000000000 | 52000 | [Comparison](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostics.json) / [Metrics](results.d/diagnostics/team10_HIPE-2026-v1.0-impresso-test-fr_run1.diagnostic_metrics.json) |

Top 3 teams by best run:

1. FI Code (team15), run2, table rank 1, mean efficiency profile rank 9
2. DS@GT_HIPE (team2), run2, table rank 2, mean efficiency profile rank 10.3333
3. MILRIT (team14), run3, table rank 4, mean efficiency profile rank 11
