# AI Security Red Team Assessment

## 1. Assessment Overview

This project is a local AI security red-team assessment of an MNIST image-classification API built with PyTorch and FastAPI.

The assessment focused on:

- Inference API reconnaissance
- Adversarial machine-learning attacks
- Input validation
- Model integrity
- Container security
- Post-mitigation verification

All testing was performed against the local assessment environment.

## 2. Baseline

The trained MNIST model achieved:

- Correct predictions: 9,703 / 10,000
- Baseline accuracy: **97.03%**

The baseline was established before adversarial testing.

## 3. Attack Surface

The API exposed the following relevant endpoints:

- `/health`
- `/model-info`
- `/predict`
- `/docs`
- `/openapi.json`

The `/predict` endpoint accepts an uploaded image and returns a model prediction.

The `/model-info`, `/docs`, and `/openapi.json` endpoints expose information about the model or API structure that can assist reconnaissance.

## 4. Adversarial Attack Results

### FGSM Attack 1

- Original label: 7
- Original prediction: 7
- Adversarial prediction: 3
- Epsilon: 0.1
- Result: Successful
- API verification: Successful

Evidence:

- `samples/original/fgsm_original.png`
- `samples/adversarial/fgsm_adversarial.png`

### FGSM Attack 2

- Original label: 2
- Original prediction: 2
- Adversarial prediction: 1
- Epsilon: 0.1
- Result: Successful
- API verification: Successful

Evidence:

- `samples/original/fgsm_original_02.png`
- `samples/adversarial/fgsm_adversarial_02.png`

### FGSM From Scratch

- Original label: 7
- Original prediction: 7
- Adversarial prediction: 3
- Epsilon: 0.1
- Result: Successful

Evidence:

- `samples/original/fgsm_original.png`
- `samples/adversarial/fgsm_from_scratch_7_to_3.png`

### PGD From Scratch

- Original label: 7
- Original prediction: 7
- Adversarial prediction: 3
- Epsilon: 0.1
- Alpha: 0.01
- Steps: 10
- Result: Successful
- API verification: Successful

Evidence:

- `samples/original/fgsm_original.png`
- `samples/adversarial/pgd_from_scratch_7_to_3.png`

## 5. Security Findings

### Finding 1 — Adversarial Input Vulnerability

The model produced incorrect predictions when tested with crafted adversarial inputs.

**Impact:** An attacker able to submit manipulated inputs may cause incorrect model predictions.

**Evidence:** Successful FGSM and PGD attacks.

**Mitigation:** Adversarial robustness should be considered during future model development and validation.

### Finding 2 — Insufficient Input Validation

Before hardening, the API accepted invalid files and oversized inputs.

**Mitigations implemented:**

- Invalid image rejection
- Empty file rejection
- 5 MB file-size limit
- 2048 × 2048 image-dimension limit

### Finding 3 — Model Integrity Risk

Unauthorized modification of `model.pth` could potentially change model behavior.

**Mitigations implemented:**

- SHA-256 model hash
- Integrity verification before model loading
- `weights_only=True` during model loading

A tampered-model test caused application startup to fail with:

`Model integrity check failed.`

### Finding 4 — Excessive Container Privileges

The original container ran as root and retained unnecessary Linux capabilities.

**Mitigations implemented:**

- Dedicated non-root `appuser`
- Read-only root filesystem
- Temporary writable `/tmp`
- `cap-drop=ALL`
- `no-new-privileges`

## 6. Post-Mitigation Verification

The hardened deployment was re-tested.

| Test                       | Result |
| -------------------------- | ------ |
| Health endpoint            | PASS   |
| Normal prediction          | PASS   |
| Invalid file rejection     | PASS   |
| Oversized file rejection   | PASS   |
| Oversized image rejection  | PASS   |
| Model SHA-256 verification | PASS   |
| Non-root execution         | PASS   |
| Read-only filesystem       | PASS   |
| All capabilities dropped   | PASS   |
| No-new-privileges          | PASS   |

Normal inference remained functional after the security controls were applied.

## 7. MITRE ATLAS Alignment

The assessment activities map to:

- AML.T0040 — AI Model Inference API Access
- AML.T0043 — Craft Adversarial Data
- AML.T0042 — Verify Attack
- AML.T0031 — Erode ML Model Integrity

Detailed mapping:

`report/mitre-atlas-mapping.md`

## 8. NIST AI RMF Alignment

The assessment also considered:

- GOVERN — security and AI-use documentation
- MAP — identification of the AI attack surface and risks
- MEASURE — baseline, adversarial attacks, and security tests
- MANAGE — implementation and verification of security mitigations

Detailed mapping:

`report/nist-ai-rmf-mapping.md`

## 9. Limitations

This assessment did not demonstrate:

- Model extraction
- Membership inference
- Data poisoning
- Backdoors
- Credential theft
- Unauthorized access to production systems

The demonstrated results are limited to the local test environment and the evidence collected during this assessment.

## 10. AI Usage

AI tools were used as assistants for technical guidance, documentation, security concepts, framework mapping, and troubleshooting.

Implementation and testing were performed locally, and AI-generated suggestions were reviewed and verified before use.

Detailed records are available in:

`ai-usage/AI_USAGE_LOG.md`

## 11. Conclusion

The assessment demonstrated that the MNIST inference API was susceptible to successful adversarial examples and initially had several security-hardening gaps.

Security controls were subsequently implemented and verified without breaking normal inference.

The final deployment uses:

- Input validation
- Model-integrity verification
- Pinned dependencies
- Non-root container execution
- Read-only filesystem
- Dropped Linux capabilities
- No-new-privileges

The assessment followed a red-team-to-defense cycle:

**Baseline → Reconnaissance → Attack → Findings → Mitigation → Verification**
