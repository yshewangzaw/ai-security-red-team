# Attack Evidence

## Purpose

This document records the successful adversarial examples produced during the AI Security Red Team Assessment.

The evidence demonstrates that modified inputs were able to change the prediction of the MNIST classification model.

---

## 1. FGSM Attack #1

### Evidence Files

Original image:

`/samples/original/fgsm_original.png`

Adversarial image:

`/samples/adversarial/fgsm_adversarial.png`

### Result

- True label: 7
- Original prediction: 7
- Adversarial prediction: 3
- Epsilon: 0.1
- Result: Successful adversarial attack

### API Verification

The adversarial image was submitted to the `/predict` API and returned HTTP 200 with prediction `3`.

This confirms that the adversarial example was accepted by the inference pipeline and produced a different prediction from the original image.

---

## 2. FGSM Attack #2

### Evidence Files

Original image:

`/samples/original/fgsm_original_02.png`

Adversarial image:

`/samples/adversarial/fgsm_adversarial_02.png`

### Result

- True label: 2
- Original prediction: 2
- Adversarial prediction: 1
- Epsilon: 0.1
- Result: Successful adversarial attack

### API Verification

The adversarial image was submitted to the `/predict` API and returned HTTP 200 with prediction `1`.

---

## 3. FGSM From Scratch

### Evidence Files

Original image:

`/samples/original/fgsm_original.png`

Adversarial image:

`/samples/adversarial/fgsm_from_scratch_7_to_3.png`

### Result

- Original prediction: 7
- Adversarial prediction: 3
- Result: Successful adversarial example

This example was generated using the FGSM implementation created from scratch.

---

## 4. PGD From Scratch

### Evidence Files

Original image:

`/samples/original/fgsm_original.png`

Adversarial image:

`/samples/adversarial/pgd_from_scratch_7_to_3.png`

### Result

- Original prediction: 7
- Adversarial prediction: 3
- Epsilon: 0.1
- Alpha: 0.01
- Steps: 10
- Result: Successful adversarial attack

This example was generated using the PGD implementation created from scratch.

---

## Attack Evidence Summary

| Attack | Original Prediction | Adversarial Prediction | Result |
|---|---:|---:|---|
| FGSM #1 | 7 | 3 | Successful |
| FGSM #2 | 2 | 1 | Successful |
| FGSM from scratch | 7 | 3 | Successful |
| PGD from scratch | 7 | 3 | Successful |

At least two successful adversarial examples were required for the assessment. This project contains four documented successful examples.

## Evidence Location

Original samples:

`/samples/original/`

Adversarial samples:

`/samples/adversarial/`

Attack implementations:

`/attacks/`

API endpoint used for verification:

`POST /predict`
