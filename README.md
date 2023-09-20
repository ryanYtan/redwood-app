# Redwood
This directory contains the code for an example web application, to be
migrated to AWS from an on-premises workload. It is just a simple Flask
e-commerce app with a PostgreSQL database.

To run locally, export the following environment variables:

```bash
export REDWOOD_IS_DEV="anything"
export REDWOOD_SQLALCHEMY_DATABASE_URI="<DATABASE_CONNECTION_STRING>"
export REDWOOD_SQLALCHEMY_TRACK_MODIFICATIONS="True" #or "False"
```
