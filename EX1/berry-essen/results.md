## 1.5 — Exponential samples across sample sizes

Exp(rate=1); population mean=1; seed=42; one independent sample vector per n.

| n | Empirical mean | Histogram |
| ---: | ---: | --- |
| 10 | 1.460416 | [Plot](plots/section_1_5_histogram_n_10.png) |
| 20 | 0.669412 | [Plot](plots/section_1_5_histogram_n_20.png) |
| 30 | 0.713080 | [Plot](plots/section_1_5_histogram_n_30.png) |
| 40 | 1.013015 | [Plot](plots/section_1_5_histogram_n_40.png) |
| 50 | 0.978297 | [Plot](plots/section_1_5_histogram_n_50.png) |
| 60 | 1.043875 | [Plot](plots/section_1_5_histogram_n_60.png) |
| 70 | 0.940368 | [Plot](plots/section_1_5_histogram_n_70.png) |
| 80 | 1.023637 | [Plot](plots/section_1_5_histogram_n_80.png) |
| 90 | 1.129026 | [Plot](plots/section_1_5_histogram_n_90.png) |
| 100 | 0.918683 | [Plot](plots/section_1_5_histogram_n_100.png) |

![Empirical means by sample size](plots/section_1_5_empirical_means.png)

## 2 — Multiple repeats

Exp(rate=1); M=100,000 independent repetitions per n; no fixed seed. Standard deviations use ddof=1.
Population mean of sample means: 1; population SD: 1/(rate × √n). Z-scores use population moments.

| n | Mean of sample means | SD of sample means | Theoretical SD | Mean histogram | Z-score CDF |
| ---: | ---: | ---: | ---: | --- | --- |
| 10 | 0.999504 | 0.316549 | 0.316228 | [Plot](plots/section_2_sample_means_n_10.png) | [Plot](plots/section_2_z_cdf_n_10.png) |
| 20 | 0.998900 | 0.224121 | 0.223607 | [Plot](plots/section_2_sample_means_n_20.png) | [Plot](plots/section_2_z_cdf_n_20.png) |
| 30 | 0.999644 | 0.181973 | 0.182574 | [Plot](plots/section_2_sample_means_n_30.png) | [Plot](plots/section_2_z_cdf_n_30.png) |
| 40 | 0.999128 | 0.157853 | 0.158114 | [Plot](plots/section_2_sample_means_n_40.png) | [Plot](plots/section_2_z_cdf_n_40.png) |
| 50 | 1.000105 | 0.141308 | 0.141421 | [Plot](plots/section_2_sample_means_n_50.png) | [Plot](plots/section_2_z_cdf_n_50.png) |
| 60 | 0.999381 | 0.128980 | 0.129099 | [Plot](plots/section_2_sample_means_n_60.png) | [Plot](plots/section_2_z_cdf_n_60.png) |
| 70 | 1.000570 | 0.119664 | 0.119523 | [Plot](plots/section_2_sample_means_n_70.png) | [Plot](plots/section_2_z_cdf_n_70.png) |
| 80 | 1.000252 | 0.112063 | 0.111803 | [Plot](plots/section_2_sample_means_n_80.png) | [Plot](plots/section_2_z_cdf_n_80.png) |
| 90 | 1.000127 | 0.106136 | 0.105409 | [Plot](plots/section_2_sample_means_n_90.png) | [Plot](plots/section_2_z_cdf_n_90.png) |
| 100 | 1.000213 | 0.100024 | 0.100000 | [Plot](plots/section_2_sample_means_n_100.png) | [Plot](plots/section_2_z_cdf_n_100.png) |

[All sample means and Z-scores](data/section_2_sample_means.csv) · [Summary CSV](data/section_2_summary.csv)
