# BM25 Suggestion Service - Coding Challenge

*Timebox*: at most **~6–8** hours.

## Overview

The goal of this challenge is to transform an existing BM25-based
suggestion algorithm into a web service and deploy it
to Kubernetes. The service should implement a simple REST-Service with
an Endpoint `/suggestions` returning a list of strings. A simple statistic
of the found and returned strings shall be kept and persisted. Assume that the statistical data will be used for
further processing and improvements. Assume that the REST-Service is called by many
users at once.

## Starting Point

You will receive a tar archive (`dkb-devops-challenge.tgz`,
`dkb-devops-challenge.zip`) containing the following files:

 * `main.py` - Python code with BM25 implementation
 * `suggestions_challenge.parquet` - Data foundation with suggestions
 * `CHALLENGE.md` - This file

The existing code implements a BM25 ranking algorithm for text
suggestions, but is currently only usable as a local script.

## Your Task

### Theory part

1. Design a solution based on the provided implementation.
2. Discuss obstacles, requirements and optimizations for your solution.
3. What do you think the statistics could be used for in the future (as mentioned). Does this impact your design?

### Hands On part

Transform the provided code into a complete, deployment-ready service
with the following requirements. Your provided solution does not need
to be 100% perfect, but improvements should be noted, so that we can talk
about them.

1. Web Service Implementation

  - Wrap and possibly refactor the BM25 functionality in a web service
  - The choice of web framework is up to you (e.g., Flask, FastAPI, Django)
  - The service should provide at least one endpoint that returns suggestions for a given query
    - Endpoint `/suggestions` react to HTTP POST.
    - Post request data should be in JSON
    - response data should also be in JSON

2. Containerization

  - Create a Dockerfile for the service
  - The container should be production-ready or at least comment what needed to be considered before you would see it as production-ready

3. Kubernetes Deployment

  - Create the necessary Kubernetes manifests (e.g., Deployment, Service, ConfigMap if needed)
  - The service *should* be deployable to a Kubernetes cluster
  - Document the deployment steps for us to reproduce locally

4. Persistence

  - Implement the strategy for the persistence you designed in a reproducable way
  - Consider how the data should be made available and stored in the Kubernetes deployment
  - Think/Discuss/Document possible improvements

5. Documentation

  - Document your work and thought process
  - Describe possible improvements and optimizations
  - Explain design decisions you made
  - Consider Possible Enhancements

You may additionally consider and implement the following aspects in your solution:

  - **Performance Optimization**: Optimizations for parallel query processing
  - **API Design**: Versioning and error handling
  - **Monitoring**: Health checks, metrics, logging
  - **Scalability**: Horizontal scaling, caching strategies
  - **Testing**: Unit tests, integration tests

## Submission

Create a Git repository with your solution and export it as a tar archive:

``` bash
git archive --format=tar.gz --output=lastname-firstname-bm25-solution.tar.gz HEAD
```

### Git Commit History

Important: Commit your changes in meaningful, traceable steps. We
want to be able to follow your development process. The structure of
your repository and the organization of your commits are part of the
evaluation.

### Confidentiality

Please keep this challenge private.

We kindly ask that you do not share this coding challenge or its
materials publicly on the internet. This includes posting it to public
repositories (GitHub, GitLab, etc.), forums, or social media platforms.

Feel free to use private repositories for your work, and of course,
you're welcome to discuss your solution with us during the interview
process.

## Timeline

You have **7 days** to complete the challenge.

## Questions?

If you have any questions, please contact simon.schwarzmeier@dkb.de and eric.schmidt@dkb.de (please include both).

Have fun!

