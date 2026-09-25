# AI Security Red Team Assessment — Pipeline Review

## 1. Scope

This review evaluates the security of the local ML inference pipeline, including:

- Model loading
- Model integrity
- Input handling
- Dependency management
- Docker container security
- Runtime privileges

## 2. Model Loading

### Original Risk

The application loads the trained PyTorch model during API startup.

A modified model file could potentially change inference behavior if its integrity was not verified.

### Mitigation

A SHA-256 hash is stored in:

model/model.sha256

Before loading the model, the application calculates the SHA-256 hash of model/model.pth and compares it with the expected value.

If the hashes do not match, startup fails with:

Model integrity check failed.

The model is also loaded using:

weights_only=True

This reduces the loading scope to model weights rather than unrestricted serialized objects.

## 3. Input Validation

### Risks Identified

The original API accepted uploaded files without sufficient validation.

Potential problems included:

- Invalid file types
- Empty uploads
- Excessively large files
- Excessively large image dimensions

### Mitigations

The final API implements:

- Empty-file rejection
- Image validation using Pillow
- Maximum file size of 5 MB
- Maximum image dimension of 2048 × 2048
- HTTP 400 for invalid images
- HTTP 413 for oversized inputs

These controls were re-tested successfully after deployment.

## 4. Dependency Management

### Original Risk

Unpinned dependencies can change between installations and may introduce unexpected compatibility or security differences.

### Mitigation

The final pi/requirements.txt pins the versions used by the project:

- FastAPI 0.141.1
- Uvicorn 0.53.0
- python-multipart 0.0.32
- PyTorch 2.14.0
- torchvision 0.29.0
- Pillow 12.3.0

## 5. Docker Container Security

### Original Risks

The initial container configuration ran the application as root and retained default Linux capabilities.

### Mitigations

The final image and runtime configuration use:

- Dedicated non-root ppuser
- Read-only root filesystem
- Writable temporary /tmp through tmpfs
- cap-drop=ALL
- 
o-new-privileges

Final runtime verification confirmed:

uid=1000(appuser)

and:

ReadonlyRootfs=true

CapDrop=["ALL"]

SecurityOpt=["no-new-privileges:true"]

## 6. Runtime Verification

The hardened container was tested after mitigation.

| Control | Result |
|---|---|
| API health | PASS |
| Normal prediction | PASS |
| Invalid image rejection | PASS |
| File-size limit | PASS |
| Image-dimension limit | PASS |
| Model integrity | PASS |
| Non-root execution | PASS |
| Read-only filesystem | PASS |
| Capabilities dropped | PASS |
| No-new-privileges | PASS |

Normal model inference continued to work after the security controls were applied.

## 7. Remaining Security Considerations

The implemented controls reduce several infrastructure and input-handling risks, but they do not make the model immune to adversarial examples.

Successful FGSM and PGD attacks were demonstrated during this assessment.

Further robustness work could include adversarial training, stronger model evaluation, rate limiting, authentication, monitoring, and production-specific deployment controls. These are outside the demonstrated mandatory implementation scope of this assessment.

## 8. Conclusion

The pipeline review identified weaknesses in input validation, model integrity protection, dependency reproducibility, and container privileges.

Mitigations were implemented and verified through post-mitigation testing.

The final deployment maintains normal inference functionality while applying stronger application and container security controls.
