# DBTonFHIR

## Description

<!-- Describe the feature and how it solves the problem. -->

The goal is to be able to map from a given source to a FHIR server without the help of a gui leveraging existing tools
such as git and DBT.

## Project template repository

[dbtonfhir-templtate](https://github.com/arkhn/dbtonfhir-template)

## Setup and installation

### Prerequisites
- Python 3.9+

### Base setup

- Create an `.env` file and specify your own configuration (you can copy `.env.template` 
and customize)

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements/tests.txt
pre-commit install 
```

### Vscode setup

#### Configure your environment

In `.vscode/settings.json`, add your environment variables as such
```json
{
  "terminal.integrated.env.linux": {
    "DBT_PROFILES_DIR": "."
  },
  "terminal.integrated.env.osx": {
    "DBT_PROFILES_DIR": "."
  },
  "terminal.integrated.env.windows": {
    "DBT_PROFILES_DIR": "."
  }
}
```

### IntelliJ/Pycharm setup

#### Configure your environment

Add the `DBT_PROFILE_DIR` environment variable to your shell environment

<img width="1231" alt="dbt_profile_dir" src="https://user-images.githubusercontent.com/34629112/145067114-807e5bb7-a752-4f4e-adbe-d21d9bd4149e.png">

## Fhir Cli

### Install

```shell
make install 
```

### Build package

```shell
make build
```

### Usage

```shell
fhir --help
```

<img width="747" alt="fhir help" src="https://user-images.githubusercontent.com/34629112/145067163-632b2eac-1e95-4699-9cc1-33ab5b70346b.png">

### Postgresql foreign data wrapper

A foreign data wrapper allows to add foreign tables from a distant database into a local schema

```postgresql
CREATE SERVER server_name
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'host', port 'port', dbname 'dbname');

CREATE USER MAPPING FOR local_user
    SERVER server_name
    OPTIONS (user 'username', password 'password');

CREATE SCHEMA local_schema;

IMPORT FOREIGN SCHEMA foreign_schema
FROM SERVER server_name INTO local_schema;

SET search_path TO local_schema;

-- show foreign tables
\detr
```

## OMOP

### Vocabulary

- Download vocabularies at https://athena.ohdsi.org/
- Create a `vocabulary` folder and extract the files there

### CDM 5.4

To build the OMOP CDM 5.4 schema in your target database, execute the following files in this order:

1. `OMOPCDM_postgresql_5.4_ddl.sql`
2. `OMOPCDM_postgresql_5.4_primary_keys.sql`
3. `vocabulary.sql`
4. `OMOPCDM_postgresql_5.4_constraints.sql`
5. `OMOPCDM_postgresql_5.4_indices.sql`

## Tests

### Unit tests
```shell
make unit-tests
```
### End to end tests
```shell
make e2e-tests
```

## Versioning and publishing
This project follows the [semver](https://semver.org/) versioning.

To bump the version, edit the `version` attribute in `setup.cfg` and add a tag on the `main` branch
with the version prefixed with a `v` (eg. `v0.1.0`). Be careful to tag with the same version
specified in `setup.cfg`.

```shell
git tag v0.1.0
git push --tags
```

As soon as the tag is pushed, a package will be built and published to Pypi.

## Implementation

![arkhn](https://user-images.githubusercontent.com/34629112/143152402-6b2522b2-7cd3-4fc5-8843-381a723ea3d8.jpg)
