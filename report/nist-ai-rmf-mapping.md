# NIST AI Risk Management Framework Mapping

## Project

AI Security Red Team Assessment

## Framework

NIST Artificial Intelligence Risk Management Framework (AI RMF) 1.0

NIST AI RMF organizes AI risk management into four core functions:

- GOVERN
- MAP
- MEASURE
- MANAGE

This project maps the security assessment activities to these functions based on the work actually performed.

---

## 1. GOVERN

### Relevant Activities

The project established security-related development and assessment practices, including:

- Maintaining an AI usage log.
- Documenting security testing activities.
- Recording attack results and security observations.
- Applying security controls to the model-serving API and Docker environment.
- Documenting identified risks and implemented mitigations.

### Project Evidence

- `ai-usage/AI_USAGE_LOG.md`
- `report/attack-report.md`
- `report/pipeline-review.md`
- `logs/sample_logs.json`

### Status

Implemented for the scope of this individual security assessment.

---

## 2. MAP

### Relevant Activities

The project identified the AI system context and potential security risks by examining:

- The MNIST classification model.
- The FastAPI inference API.
- The `/predict` endpoint.
- The `/model-info` endpoint.
- API documentation through `/docs`.
- The OpenAPI schema through `/openapi.json`.
- Image upload handling.
- Docker container configuration.
- Model loading and integrity.

### Identified Risks

The assessment identified risks including:

1. Adversarial inputs could cause incorrect model predictions.
2. The prediction endpoint accepted uploaded files and required input validation.
3. Large files could create resource-consumption concerns.
4. Very large image dimensions could create resource-consumption concerns.
5. Model modification could affect prediction integrity.
6. API documentation and model information expose information useful for reconnaissance.
7. The original Docker container operated as root.

### Project Evidence

- Reconnaissance testing
- FGSM attack results
- PGD attack results
- Input validation tests
- Docker security review
- Model integrity testing

### Status

Completed for the assessed system.

---

## 3. MEASURE

### Relevant Activities

The project measured AI and security behavior using repeatable tests.

### Model Performance

Baseline evaluation:

- Dataset: MNIST
- Test samples: 10,000
- Correct predictions: 9,703
- Baseline accuracy: 97.03%

### Adversarial Testing

#### FGSM Attack

- Original prediction: 7
- Adversarial prediction: 3
- Epsilon: 0.1
- Result: Successful adversarial attack

#### Second FGSM Attack

- Original prediction: 2
- Adversarial prediction: 1
- Epsilon: 0.1
- Result: Successful adversarial attack

#### PGD Attack

- Original prediction: 7
- Adversarial prediction: 3
- Epsilon: 0.1
- Alpha: 0.01
- Steps: 10
- Result: Successful adversarial attack

### Input Security Measurements

The API was also tested with invalid and oversized inputs.

| Test | Result |
|---|---|
| Valid image | HTTP 200 |
| Invalid file | HTTP 400 |
| File larger than 5 MB | HTTP 413 |
| Image dimensions larger than 2048 pixels | HTTP 413 |
| Tampered model | Application startup rejected |

### Project Evidence

- `model/evaluate.py`
- `attacks/attack_01_fgsm.py`
- `attacks/attack_02_fgsm.py`
- `attacks/fgsm_from_scratch.py`
- `attacks/pgd_from_scratch.py`
- `logs/sample_logs.json`

### Status

Completed for the performed tests.

---

## 4. MANAGE

### Relevant Activities

Based on identified risks, security controls were implemented.

### API Input Controls

Implemented:

- Maximum upload size: 5 MB
- Maximum image dimension: 2048 × 2048
- Empty-file rejection
- Invalid-image rejection
- HTTP 413 for oversized input
- HTTP 400 for invalid input

### Model Integrity

A SHA-256 hash was generated for the trained model.

The API verifies the model hash before loading the model.

A tampering test was performed by modifying the model file. The application rejected the modified model with:

`Model integrity check failed.`

### Docker Hardening

The container was hardened with:

- Non-root `appuser`
- Read-only root filesystem
- Writable `/tmp` through tmpfs
- All Linux capabilities dropped
- `no-new-privileges`

### Project Evidence

- `api/app.py`
- `api/Dockerfile`
- `model/model.sha256`
- Docker security testing results
- Model tamper test

### Status

Implemented and tested individually. Final end-to-end regression testing is still required after the latest API changes.

---

## NIST AI RMF Summary

| Function | Project Implementation | Status |
|---|---|---|
| GOVERN | AI usage and security documentation | Completed for project scope |
| MAP | Attack-surface and risk identification | Completed |
| MEASURE | Baseline, adversarial, API and security testing | Completed |
| MANAGE | Security mitigations and hardening | Implemented |

## Limitations

This mapping represents the activities performed during this individual red-team assessment. It does not claim that the project implements every NIST AI RMF category or subcategory.

Organizational governance, regulatory analysis, stakeholder analysis, production monitoring, incident response processes, and other enterprise-level activities were outside the scope of this assessment.

## Reference

National Institute of Standards and Technology (NIST), Artificial Intelligence Risk Management Framework (AI RMF) 1.0.
