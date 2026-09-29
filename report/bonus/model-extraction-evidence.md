# Model Extraction Bonus Evidence

## Objective

Demonstrate a controlled black-box model extraction scenario against the local MNIST inference API.

The target model was accessed only through the local `/predict` API. The original model file was not modified.

## Experiment 1 - 50 Queries

- Training queries: 50
- Evaluation queries: 50 unseen samples
- Matching predictions: 33
- Fidelity: 66.00%

Evidence:

- Query images: `samples/extraction/images/`
- Query labels: `samples/extraction/query_labels.json`
- Substitute model: `samples/extraction/substitute_model.pth`

## Experiment 2 - 500 Queries

- Training queries: 500
- Evaluation queries: 100 unseen samples
- Matching predictions: 83
- Fidelity: 83.00%

Evidence:

- Query images: `samples/extraction_500/images/`
- Query labels: `samples/extraction_500/query_labels.json`
- Substitute model: `samples/extraction_500/substitute_model.pth`
- Training script: `attacks/model_extraction/train_substitute_500.py`
- Evaluation script: `attacks/model_extraction/evaluate_substitute_500.py`

## Attack Method

The extraction process was label-only black-box extraction.

The API returned only the predicted digit. It did not expose model weights, logits, or confidence scores.

The collected query/label pairs were used to train a separate substitute model with the same general MNIST architecture.

The substitute model was then evaluated against the target API using new samples that were not part of the extraction training set.

## Result

The 500-query experiment achieved:

**83% prediction fidelity on 100 unseen queries.**

This means that the substitute model produced the same top-1 prediction as the target API for 83 of the 100 evaluation samples.

## Interpretation

The result demonstrates partial reproduction of the target model's decision behavior using black-box query access.

This does not mean that the original model weights were recovered or that the substitute is an exact copy of the target model.

## Integrity Verification

After completing the extraction experiments, the SHA-256 hash of the original target model was verified.

Expected/current hash:

`5F8FF54138F8F8F242FDC3AE6A89CE4D0A9404EE4A35A2842356191D2500A8FE`

The hash remained unchanged.

Therefore, the model extraction experiment did not modify the original `model/model.pth`.

## Limitations

- Only top-1 prediction labels were available.
- Confidence scores and logits were not exposed.
- The experiment was performed against the local assessment API.
- The substitute model was not an exact copy of the target model.
- Fidelity was measured on 100 unseen queries for the 500-query experiment.
- No production system or third-party model was targeted.
