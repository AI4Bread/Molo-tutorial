# Installation

## Hosted users: no local installation

Open [Molo](https://molo.ai4bread.com/), register or log in, and follow the
[web workflow](web.md). The alternate address is
[molopipeline.site](https://molopipeline.site/). Read-only reviewer access is
available only when the administrator enables it.

## Documentation preview only

```bash
git clone https://github.com/AI4Bread/Molo-tutorial.git
cd Molo-tutorial
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-docs.txt
mkdocs build --strict
mkdocs serve -a 127.0.0.1:8001
```

These packages build documentation. They do **not** install Molo's scientific
Python/R stack. Port 8001 avoids the application's usual loopback port 8000.

## Scientific or self-hosted installation

!!! warning "Obtain a matching complete source/environment release"
    The audited server has intentional working-tree changes. Cloning an older
    public commit or installing only `Molo_FastAPI/requirements.txt` is not enough
    to reproduce the entire scientific environment. See [provenance](provenance.md).

The current implementation uses a Python 3.10 scientific environment on the
examined host; this is an observed environment, not a declared minimum version.
It requires PyTorch and associated numerical/graph packages plus R dependencies
such as Seurat, Arrow, and analysis-specific packages. CellChat, trajectory, and
ATAC workers have distinct environment/library needs. Match CUDA/PyTorch to the
actual GPU; do not copy a GPU index from another host.

Obtain from maintainers:

1. A complete source snapshot matching the intended documentation revision.
2. Conda/Python package specifications and matching R/renv environments.
3. A portable downstream configuration with your own filesystem paths.
4. Input data, preprocessing, and provenance sufficient for the workflow to run.

Before accepting jobs, verify the web packages, the alignment worker's Python
and `Rscript`, and each requested downstream worker. Keep trajectory and ATAC
special environments distinct where configured. See [server deployment](deployment.md).

## Container status

The historical page advertised a ready-made Docker environment without naming an
image. **This documentation does not claim a verified public image/tag or provide
an invented `docker pull` command.** Use the hosted service or a maintainer-supplied
matching runtime until a versioned image is released and tested.
