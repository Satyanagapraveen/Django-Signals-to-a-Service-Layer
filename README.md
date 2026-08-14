# Enterprise Order Management: Architecture Refactor

A production-grade Django application demonstrating the architectural migration from implicit, signal-based event handling to a robust, explicit Service Layer pattern.

This repository serves as a masterclass in database integrity, test isolation, and PostgreSQL query optimization, highlighting the dangers of framework "magic" in high-throughput environments.

## 🧠 Core Engineering Concepts Demonstrated

- **Architectural Refactoring:** Moving business logic from Django Signals to an explicit Service Layer.
- **Database Transactional Integrity:** Utilizing `transaction.atomic()` to guarantee ACID compliance (Atomicity) during multi-table writes.
- **Performance Optimization:** Resolving the N+1 Query Problem using Django's `bulk_create()` and `F()` expressions for database-level mathematical computations.
- **Test Isolation:** Implementing clean-room environments using `post_save.disconnect()` to prevent state bleed across automated test suites.
- **Vulnerability Detection:** Proving through automated testing that bulk ORM operations (`QuerySet.update()`) dangerously bypass application-level signals.

## 🛠️ Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 🚀 Setup & Installation

**1. Environment Configuration**
Clone the repository and set up your environment variables. A template is provided.

```bash
cp .env.example .env
```

**2. Container Initialization**
The project is fully containerized. The app service is strictly dependent on the db service passing its pg_isready healthcheck. Migrations are applied automatically on startup.

```bash
docker-compose up -d --build
```

**3. Verification**
Ensure both containers (db and app) are running and healthy.

```bash
docker-compose ps
```

## 🧪 Running the Test Suite

The test suite explicitly proves the flaws of the signal architecture and the integrity of the new Service Layer. It validates test isolation and explicit data commits.

To run the isolated test suite inside the container:

```bash
docker-compose exec app python manage.py test orders
```

## 📈 Performance Benchmarking

A custom Django Management Command is included to scientifically prove the performance disparity between the implicit signal architecture and the optimized Service Layer.

The benchmark executes 1,000 order creations and compares the N+1 query execution against bulk_create coupled with F() expression updates.

To execute the benchmark:

```bash
docker-compose exec app python manage.py benchmark_updates
```

Expected Output Format:

```plaintext
Signal approach time: 4.7661s
Optimized service time: 0.0553s
Speedup factor: 86.18x
```
