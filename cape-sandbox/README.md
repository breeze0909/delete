# CAPE Sandbox Enrichment Connector

This connector enriches observables of type `StixFile` and `Artifact` in OpenCTI by submitting them to a CAPE Sandbox instance for analysis.

## 1. Installation

### From Source

If you prefer to build the connector from source, you can use the provided `Dockerfile`:

```bash
docker build -t opencti/connector-cape-sandbox .
```

## 2. Configuration

The connector is configured using environment variables. The following variables are available:

| Environment Variable | `docker-compose.yml` Parameter | `config.yml` Parameter | Description |
| -------------------- | ------------------------------ | ---------------------- | ----------- |
| `OPENCTI_URL` | `OPENCTI_URL` | `opencti.url` | The URL of your OpenCTI instance. |
| `OPENCTI_TOKEN` | `OPENCTI_TOKEN` | `opencti.token` | The token for your OpenCTI instance. |
| `CONNECTOR_ID` | `CONNECTOR_ID` | `connector.id` | A unique identifier for this connector. |
| `CONNECTOR_NAME` | `CONNECTOR_NAME` | `connector.name` | The name of the connector. |
| `CONNECTOR_SCOPE` | `CONNECTOR_SCOPE` | `connector.scope` | The scope of the connector (e.g., `StixFile,Artifact`). |
| `CONNECTOR_AUTO` | `CONNECTOR_AUTO` | `connector.auto` | Whether to automatically enrich observables. |
| `CONNECTOR_LOG_LEVEL` | `CONNECTOR_LOG_LEVEL` | `connector.log_level` | The log level for the connector. |
| `CAPE_SANDBOX_URL` | `CAPE_SANDBOX_URL` | `cape_sandbox.url` | The URL of your CAPE Sandbox API (e.g., `https://Base_URL/apiv2`). |
| `CAPE_SANDBOX_TOKEN` | `CAPE_SANDBOX_TOKEN` | `cape_sandbox.token` | The API token for your CAPE Sandbox instance. |
| `CAPE_SANDBOX_ROUTE` | `CAPE_SANDBOX_ROUTE` | `cape_sandbox.route` | The network routing to use for the analysis (e.g., `none`, `internet`, `tor`, `vpn0`). |
| `CAPE_SANDBOX_TIMEOUT` | `CAPE_SANDBOX_TIMEOUT` | `cape_sandbox.timeout` | The maximum time in seconds to run the analysis. |
| `CAPE_SANDBOX_ENFORCE_TIMEOUT` | `CAPE_SANDBOX_ENFORCE_TIMEOUT` | `cape_sandbox.enforce_timeout` | Whether to enforce the full timeout period for the analysis. |
| `CAPE_SANDBOX_PRIORITY` | `CAPE_SANDBOX_PRIORITY` | `cape_sandbox.priority` | The priority for submitted samples (1-3, where 3 is the highest). |
| `CAPE_SANDBOX_TRY_EXTRACT` | `CAPE_SANDBOX_TRY_EXTRACT` | `cape_sandbox.try_extract` | Whether to try and extract configs statically without a VM first. |
| `CAPE_SANDBOX_OPTIONS` | `CAPE_SANDBOX_OPTIONS` | `cape_sandbox.options` | A list of options to be passed to the analysis package. |
| `CAPE_SANDBOX_LESS_NOISE` | `CAPE_SANDBOX_LESS_NOISE` | `cape_sandbox.less_noise` | Whether to only upload Artifacts associated with Yara rule matches. |
| `CAPE_SANDBOX_COOLDOWN_TIME` | `CAPE_SANDBOX_COOLDOWN_TIME` | `cape_sandbox.cooldown_time` | The amount of seconds to wait between retries of the API. |
| `CAPE_SANDBOX_MAX_RETRIES` | `CAPE_SANDBOX_MAX_RETRIES` | `cape_sandbox.max_retries` | The maximum number of retries for the API before failing. |
| `CAPE_SANDBOX_MAX_TLP` | `CAPE_SANDBOX_MAX_TLP` | `cape_sandbox.max_tlp` | The maximum TLP level to process. |

You should edit both the `docker-compose.yml` file and `config.yml` file in the `src` directory to configure the connector.

## 3. Deployment

### Using Docker Compose

The recommended way to deploy the connector is using Docker Compose. A `docker-compose.yml` file is provided for this purpose.

1.  **Edit `docker-compose.yml`:**
    Modify the environment variables in the `docker-compose.yml` file to match your OpenCTI and CAPE Sandbox configuration.

2.  **Start the connector:**
    ```bash
    docker-compose up -d
    ```

## 4. Usage

Once the connector is running, it will automatically enrich observables of type `StixFile` and `Artifact` that are created in OpenCTI. The enrichment process includes:

*   Uploading the file to CAPE Sandbox for analysis.
*   Adding the analysis results, including a malice score, to the observable.
*   Creating external references to the CAPE Sandbox analysis report.
*   Adding labels based on malware family detections.
*   Attaching TTPs (Tactics, Techniques, and Procedures) based on the analysis.
*   Uploading process dumps and payloads as artifacts.
*   Extracting and attaching CnC (Command and Control) addresses.
*   Attaching network indicators (domains and IP addresses).

```
