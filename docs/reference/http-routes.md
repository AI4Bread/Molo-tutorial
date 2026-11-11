# Complete HTTP routes

Source-audited on **2026-11-11**, Web app **1.6.0**. Generated from the [source contract](../provenance.md); do not edit tables by hand. Defaults below are **entry-point defaults**, not universal recommendations.

Only routers mounted by `app/main.py` are listed. Static files and framework-generated OpenAPI routes are omitted. Form/File declarations are form data, not JSON. Session authentication normally applies; see the [HTTP guide](../http-api.md). An omitted form field uses its declared default, but services can enforce additional constraints.

| Method | Path | Handler | Parameters |
| --- | --- | --- | --- |
| GET | `/` | `home_page` | none |
| GET | `/about` | `about_page` | none |
| HEAD | `/about` | `about_page` | none |
| GET | `/analyse/alignment/` | `get_alignment_page` | none |
| GET | `/analyse/alignment/download/{task_id}` | `download_result` | task_id: str = required |
| POST | `/analyse/alignment/run` | `run_alignment` | files: List[UploadFile] = File(default=[]); mode: str = Form(...); data_type: str = Form(...); sp_alignment: str = Form('Molo'); input_type: str = Form('upload'); server_path: Optional[str] = Form(None); project_id: Optional[str] = Form(None); dataset_asset_ids: Optional[List[str]] = Form(default=[]); dataset_name: Optional[str] = Form(None); tune_preset: str = Form('default'); tune_trials: Optional[str] = Form(None) |
| GET | `/analyse/alignment/status/{task_id}` | `get_status` | task_id: str = required |
| GET | `/analyse/downstream/artifacts/{task_id}` | `get_artifacts` | task_id: str = required |
| POST | `/analyse/downstream/cancel/{task_id}` | `cancel_task` | task_id: str = required |
| GET | `/analyse/downstream/preview/{task_id}/{filename:path}` | `get_preview` | task_id: str = required; filename: str = required |
| GET | `/analyse/downstream/status/{task_id}` | `get_status` | task_id: str = required |
| GET | `/analyse/downstream/{analysis_type}` | `get_analysis_page` | analysis_type: str = required |
| POST | `/analyse/downstream/{analysis_type}/submit` | `submit_analysis` | analysis_type: str = required; data_source: str = Form(...); file: Optional[UploadFile] = File(None); server_path: Optional[str] = Form(None); integrated_task_id: Optional[str] = Form(None); analysis_steps: List[str] = Form(default=[]); resolution: float = Form(0.5); n_neighbors: int = Form(30); species: str = Form('mouse'); n_feature_min: int = Form(2500); project_id: Optional[str] = Form(None); dataset_asset_id: Optional[str] = Form(None); dataset_name: Optional[str] = Form(None) |
| GET | `/api/auth/me` | `me` | none |
| POST | `/api/auth/password-reset/complete` | `complete_password_reset` | payload: PasswordResetCompleteRequest = required |
| POST | `/api/auth/password-reset/start` | `start_password_reset` | payload: PasswordResetStartRequest = required |
| POST | `/api/auth/register/complete` | `complete_registration` | payload: RegistrationCompleteRequest = required |
| POST | `/api/auth/register/start` | `start_registration` | payload: RegistrationStartRequest = required |
| GET | `/api/datasets` | `list_dataset_assets` | project_id: Optional[str] = None |
| POST | `/api/datasets/uploads` | `create_upload_asset` | files: List[UploadFile] = File(default=[]); project_id: Optional[str] = Form(None); name: str = Form(...); platform: str = Form(...); description: str = Form(''); species: Optional[str] = Form(None); tissue: Optional[str] = Form(None) |
| GET | `/api/datasets/{asset_id}` | `get_dataset_asset` | asset_id: str = required |
| POST | `/api/datasets/{asset_id}/validate` | `validate_dataset_asset` | asset_id: str = required |
| GET | `/api/projects` | `list_projects` | include_archived: bool = False |
| POST | `/api/projects` | `create_project` | payload: ProjectPayload = required |
| GET | `/api/projects/{project_id}` | `get_project` | project_id: str = required |
| PATCH | `/api/projects/{project_id}` | `update_project` | project_id: str = required; payload: ProjectPatchPayload = required |
| POST | `/api/projects/{project_id}/archive` | `archive_project` | project_id: str = required |
| GET | `/api/projects/{project_id}/datasets` | `list_project_assets` | project_id: str = required |
| GET | `/auth/login` | `login_page` | next: str &#124; None = None |
| POST | `/auth/login` | `login` | identity: str = Form(...); password: str = Form(...); next_url: str = Form('/') |
| POST | `/auth/logout` | `logout` | none |
| POST | `/auth/reviewer-login` | `reviewer_login` | next_url: str = Form('/jobs') |
| GET | `/chains/asset/{asset_id}` | `get_chain_for_asset` | asset_id: str = required |
| GET | `/chains/job/{job_id}` | `get_chain_for_job` | job_id: str = required |
| GET | `/chains/project/{project_id}` | `get_chains_for_project` | project_id: str = required; limit: int = Query(default=25, ge=1, le=100) |
| GET | `/contributors` | `contributors_page` | none |
| GET | `/health/live` | `health_live` | none |
| GET | `/health/ready` | `health_ready` | none |
| GET | `/jobs` | `jobs_page` | none |
| GET | `/jobs/{job_id}` | `get_job` | job_id: str = required |
| POST | `/jobs/{job_id}/cancel` | `cancel_job` | job_id: str = required |
| POST | `/jobs/{job_id}/clone` | `clone_job` | job_id: str = required |
| GET | `/jobs/{job_id}/clone-template` | `get_clone_template` | job_id: str = required |
| POST | `/jobs/{job_id}/resend-email` | `resend_job_email` | job_id: str = required |
| POST | `/jobs/{job_id}/retry` | `retry_job` | job_id: str = required |
| GET | `/projects` | `projects_page` | none |
| GET | `/results/download/{token}` | `download_result` | token: str = required |
| GET | `/reviewer` | `reviewer_dashboard` | none |
| GET | `/tutorial` | `tutorial_page` | none |
| HEAD | `/tutorial` | `tutorial_page` | none |
| GET | `/update_log` | `update_log_page` | none |

## JSON request models

### `RegistrationStartRequest`

| Field | Type | Default |
| --- | --- | --- |
| `username` | `str` | `required` |
| `email` | `str` | `required` |
| `password` | `str` | `required` |
| `password_confirm` | `str` | `required` |

### `RegistrationCompleteRequest`

| Field | Type | Default |
| --- | --- | --- |
| `challenge_id` | `str` | `required` |
| `email` | `str` | `required` |
| `code` | `str` | `required` |

### `PasswordResetStartRequest`

| Field | Type | Default |
| --- | --- | --- |
| `email` | `str` | `required` |

### `PasswordResetCompleteRequest`

| Field | Type | Default |
| --- | --- | --- |
| `challenge_id` | `str` | `required` |
| `email` | `str` | `required` |
| `code` | `str` | `required` |
| `password` | `str` | `required` |
| `password_confirm` | `str` | `required` |

### `ProjectPayload`

| Field | Type | Default |
| --- | --- | --- |
| `name` | `str` | `required` |
| `description` | `str` | `''` |
| `species` | `Optional[str]` | `None` |
| `tissue` | `Optional[str]` | `None` |
| `platform` | `Optional[str]` | `None` |
| `default_params` | `Dict[str, Any]` | `Field(default_factory=dict)` |

### `ProjectPatchPayload`

| Field | Type | Default |
| --- | --- | --- |
| `name` | `Optional[str]` | `None` |
| `description` | `Optional[str]` | `None` |
| `species` | `Optional[str]` | `None` |
| `tissue` | `Optional[str]` | `None` |
| `platform` | `Optional[str]` | `None` |
| `default_params` | `Optional[Dict[str, Any]]` | `None` |
