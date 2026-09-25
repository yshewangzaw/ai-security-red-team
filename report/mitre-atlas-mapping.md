# MITRE ATLAS Mapping

## Purpose

This document maps the AI Security Red Team Assessment activities to relevant MITRE ATLAS techniques.

## 1. AI Model Inference API Access — AML.T0040

**Our activity:** Reconnaissance and interaction with the /predict inference API.

**Evidence:**
- Identified the /predict endpoint.
- Sent normal and adversarial images to the API.
- Observed prediction responses.

**Security relevance:** An exposed inference interface provides an attacker with a query surface for testing and adversarial input.

---

## 2. Craft Adversarial Data — AML.T0043

**Our activity:** Created adversarial MNIST images using FGSM and PGD.

**Evidence:**
- FGSM: 7 ? 3
- FGSM: 2 ? 1
- PGD: 7 ? 3
- Adversarial examples were successfully verified through the API.

**Security relevance:** Small input perturbations can cause incorrect model predictions while preserving the general appearance of the original input.

---

## 3. Verify Attack — AML.T0042

**Our activity:** Submitted generated adversarial examples to the inference API and verified the resulting predictions.

**Evidence:**
- FGSM adversarial examples returned incorrect predictions through /predict.
- PGD adversarial example returned an incorrect prediction through /predict.

**Security relevance:** API-level verification demonstrates that the crafted adversarial examples affect the deployed inference service, not only the offline attack script.

---

## 4. Erode ML Model Integrity — AML.T0031

**Our activity:** Assessed the risk of unauthorized modification of the model file and implemented model integrity verification.

**Evidence:**
- SHA-256 hash stored in model/model.sha256.
- Model hash verified before model loading.
- A tampered model test caused startup failure with Model integrity check failed.

**Security relevance:** Unauthorized model modification could change inference behavior. Hash verification provides a basic integrity control.

---

## Limitations

This assessment did not demonstrate:

- Model extraction
- Membership inference
- Data poisoning
- Backdoors
- Credential theft
- Unauthorized access to production systems

The techniques above are mapped only to activities actually performed during this assessment.

## Conclusion

The assessment demonstrated an inference API attack surface, successful adversarial-example attacks, attack verification through the deployed API, and a model-integrity threat/control. The mapping is limited to the techniques supported by the evidence collected during this project.
