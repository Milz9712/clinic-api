# Case study: Clinic API on AWS (Month 1)

I built a tested, containerised API for my sports recovery clinic, with a Postgres database, and deployed it live on AWS from a secrets-free CI/CD pipeline.

## The problem

My clinic's treatment list (names and prices) lived in people's heads and spreadsheets. Staff couldn't look it up reliably, and no other system could use it.

I wanted a single source of truth that a program could read and update. That is also the foundation an AI assistant needs: it can only answer clients accurately if it can call a real system for the facts.

## What I built

A REST API (Python, FastAPI) where staff can list, look up, create and delete treatments, backed by a Postgres database. It has 7 automated tests and runs in a Docker container.

```
                 GitHub Actions ──push via OIDC──> Amazon ECR
                 (test, build, push)               (private image registry)
                                                         │
                                                    pull image
                                                         ▼
Internet ──HTTPS──> Load balancer ──port 8000──> clinic-api (ECS Fargate) ──port 5432──> Postgres (RDS, not public)
```

Every push to GitHub runs the tests against a throwaway database; only if they pass is the image built and pushed to Amazon ECR, using OIDC so no AWS keys are stored. ECS Express Mode runs the container behind an HTTPS load balancer, and security groups let only the app reach the database.

## What broke and how I fixed it

**Symptom.** On the first deploy, the containers kept stopping and the service never went healthy.

**Evidence.** The application logs in CloudWatch showed my own startup code (`main.py`, line 19) failing with `psycopg.errors.ConnectionTimeout`, followed by "Application startup failed".

**Cause.** A timeout means no answer at all. A wrong password would have produced "password authentication failed", so the network was the problem, not the credentials: the database's security group did not allow traffic from the app.

**Fix.** I added one inbound rule to the database's security group: PostgreSQL (port 5432), with the app's security group as the only source. After a new deployment the app connected, finished starting up, and the load balancer's health checks passed.

**Other problems solved along the way:** a GitHub OIDC login failure caused by GitHub's 2026 change to its token format, a test that was deleting real data, and a one-letter typo that broke a CI step.

## Result

- Live over HTTPS on AWS: listed treatments (empty), created one, and read it back from the cloud database
- Every change is tested automatically before it can reach AWS, and no AWS keys are stored anywhere
- Built in about four weeks alongside running the clinic
- Torn down after testing to keep costs near zero; it can be redeployed from the stored image

Screenshots of the live service and test are in the [README](README.md#deployment-aws).

## What I'd do differently

Read every line more carefully before acting. My best fixes came from writing down what I expected to happen before running anything: when the result didn't match, the difference pointed straight at the bug.

## What's next

Month 2: a client assistant built on the Claude API that answers clients' questions about treatments, checks this API for what is available, and drafts booking replies. The model will call clinic-api as a tool, which is why it was built properly first.
