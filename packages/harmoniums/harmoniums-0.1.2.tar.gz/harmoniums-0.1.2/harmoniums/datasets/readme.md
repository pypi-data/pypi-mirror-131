# Datasets
## NVALT-11
The NVALT-11 study [1] considered the effect of profylactic brain radiation
versus observation in ($`m`$=174) patients with advanced non-small cell lung
cancer. The dataset ([nvalt11.csv](nvalt11.csv)) consists of the following
fields:
- `age` in years
- `arm`
    Randomisation arm: intervention (1) vs observation (0).
- `bmi`
    Body-mass index, computed as $`\frac{\mathrm{mass}}{\mathrm{height}^2}`$ ([kg]/[m²]).
- `gender_female` (`0` is male, `1` is female).
- `os_mth`, `os_event`
    Overall survival event time and indicator variable.
- `performance_status`
    Performance status according to the World Health Organisation criteria [4]:
    - `WHO0`: Fully active, no restrictions on activities.
    - `WHO1`:  Unable to do strenuous activities, but able to carry out light housework and sedentary activities.
    - `WHO2`:  Able to walk and manage self-care, but unable to work.
- `prior_conditions`
    Whether the was patient suffering from, or ever suffered from significant medical conditions  (`1` is yes, `0` is no).
- `prior_malign`
    Did the patient have prior other malignancies (`1` is yes, `0` is no)?
- `smoker` with values `current`, `former`, or `never`.
- `squamous`
    Type of non-small cell lung cancer (`0` is non-squamous cell carcinoma, `1` is squamous cell carcinoma).
- `stage`: Extent of the disease
    - IIIa
    - IIIb
- `sympbmets_mth`, `sympbmets_event` Symptomatic brain metastases free survival time and indicator variable.
<!-- - bmet_mth
- nsymp_mth
- pfs_mth
- bmet_event
- nsymp_event
- pfs_event -->


## NVALT-8
The NVALT-8 study [2] is a randomised control experiment that evaluated the efficacy of the drug nadroparin in lung cancer patients by looking at the recurrence free survival.
The dataset ([nvalt8.csv](nvalt8.csv)) consists of the following fields:
- `arm`
    Randomization arm, indicating whether the participant was administered additional nadroparin (`CP/CG+N`) or not(`CP/CG`).
- `T-stage`
    Primary tumour staging [3]:
    - `T1`: tumour invades the lamina propria or the submucosa
    - `T2`: tumour invades the muscularis propria or the subserosa
    - `T3`: tumour penetrates the serosa (visceral peritoneum) without invasion of surrounding structures
    - `T4`: tumour invades surrounding structures
- `N-stage`
    Lymph node staging [3]:
    - `N0`: no evidence of regional lymph node metastasis.
    - `N1`: metastasis in 1-6 lymph nodes.
    - `N2`: metastasis in 7-15 lymph nodes.
    - `N3`: metastasis in > 15 regional lymph nodes.
    - `Nx`: regional lymph nodes cannot be assessed.
- `M-stage`
    Staging of distant metastases [3]:
    - `M0`: no evidence of distant metastasis.
    - `Mx`: distant metastasis cannot be assessed.
- `performance_status`
    Performance status according to the World Health Organisation criteria [4]:
    - `WHO0`: Fully active, no restrictions on activities.
    - `WHO1`:  Unable to do strenuous activities, but able to carry out light housework and sedentary activities.
    - `WHO2`:  Able to walk and manage self-care, but unable to work.
- `gender_female`
- `histology` of the tumour
    - `Squamous cell carcinoma`
    - `Adenocarcinoma`
    - `Large cell carcinoma`
    - `other`
- `age` in years.
- `smoker` with values `current`, `former`, or `never`.
- `bmi`
    Body-mass index, computed as $`\frac{\mathrm{mass}}{\mathrm{height}^2}`$ ([kg]/[m²]).
- `stage` Extent of the disease:
    - Ib
    - IIa
    - IIb
    - IIIa
    - IIIb
    - other
- `FDG-PET SUVmax`, `FDG-PET SUVmax>=10`
    FDG measures the metabolic activity of the tumour and is determined using a PET CT scan. The value represents the maximum standarized uptake value (SUV) .
- `os_mth`, `os_event`
    Overall survival event time and indicator variable.
- `rfs_mth`, `rfs_event`
    Recurrence free survival event time and indicator variable..
## References:
1. D. De Ruysscher _et al._ "[Prophylactic cranial irradiation versus observation in radically treated stage III non–small-cell lung cancer: A randomized phase III NVALT-11/DLCRG-02 study.](https://ascopubs.org/doi/10.1200/JCO.2017.77.5817)" Journal of Clinical Oncology 36.23 (2018): 2366-2377.
2. H. J. M. Groen _et al._ "[Randomised phase 3 study of adjuvant chemotherapy with or without nadroparin in patients with completely resected non-small-cell lung cancer: the NVALT-8 study.](https://www.nature.com/articles/s41416-019-0533-3)" British journal of cancer 121.5 (2019): 372-377.
3. https://www.oncoline.nl/index.php?pagina=/richtlijn/item/pagina.php&id=31870&richtlijn_id=740
4. https://www.verywellhealth.com/what-is-performance-status-2249416