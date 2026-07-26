# Deployment Notes

## Docker Build Times
Due to the size of the dependencies (specifically `torch`), the Docker image build time has noticeably increased. This is expected behavior.
Please factor in extended build times (approximately 3-5 minutes depending on the build environment and network speed) during future deployment planning and CI/CD pipeline configuration.
