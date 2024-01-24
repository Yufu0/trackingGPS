# User Movement Simulation Project - TrackingGPS

The goal of this project is to simulate user movement on a map and enable drawing on an online interface. To achieve this, several technologies have been used:

- **Database:** PostgreSQL
- **Streaming Platform:** Kafka
- **Producer:** Python
- **Consumer:** Rust
- **Backend:** Spring Boot
- **Frontend:** Angular

## Data Flow

This diagram illustrates the flow of data in the project.
```
+----------+     +----++-+     +----------+     +------------+     +-------------+     +---------+
| Producer | --> | Kafka | --> | Consumer | --> | PostgreSQL | --> | Spring Boot | --> | Angular |
+----------+     +-------+     +----------+     +------------+     +-------------+     +---------+
```

## How to Run the Project:

1. **Git clone**
2. Update the `.env` file at the root
3. Run the `deploy.sh` script, which duplicates the `.env` file for each Docker compose

Two possibilities:

If you want to run the project on multiple machines, launch the composes in the following order (ensure to fill in the respective IPs in the `.env`):
  1. Kafka compose
  2. Producer compose
  3. Consumer compose
  4. Frontend compose

Or if you want to run everything on the same machine, launch the compose at the project's root (ensure to use the local machine's IP in the `.env`).

Note: After each update of the `.env`, it is necessary to rerun the `deploy.sh`.
