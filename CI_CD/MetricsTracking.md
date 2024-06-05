# GitHub Support for DORA Metrics

## Overview:
GitHub supports DORA (DevOps Research and Assessment) metrics through various integrations and tools. These metrics help teams measure their DevOps performance, focusing on four key areas: deployment frequency, lead time for changes, mean time to restore service, and change failure rate. Here’s how GitHub facilitates the tracking and calculation of these metrics.

## Tools and Integrations:

### Dorametrix:

### Dorametrix 
A Node.js-based service that helps calculate DORA metrics by inferring them from events created manually or with webhooks. It integrates with GitHub Actions, making it easy to set up and use for tracking DORA metrics like deployment frequency and change failure rate.
Dorametrix on GitHub​ (GitHub)​
Oobeya:

### Oobeya 
A comprehensive engineering intelligence platform that integrates with GitHub to calculate DORA metrics. It tracks deployment pipelines and provides accurate DORA metrics from commit to production deployment without requiring changes to existing pipelines.
Oobeya Documentation​ (Welcome to Oobeya! | Oobeya Docs)​
Four Keys:

The Four Keys project 
Developed by Google, is a platform for monitoring the four key software delivery metrics. It integrates with GitHub by collecting events through webhooks, processing them with Cloud Run and Pub/Sub, and storing the data in BigQuery for analysis.

### Four Keys on GitHub​ (GitHub)​
### Automated DORA Metrics Action:

This GitHub Action by Wednesday Solutions automates the generation of DORA metrics. It calculates and records metrics for each release, providing insights into the efficiency and quality of software delivery.

### Automated DORA Metrics on GitHub Marketplace​ (GitHub)​

Examples of Metrics
Metrics you can pull using GitHub and its integrations to measure CI/CD performance:

- Deployment Frequency: Number of deployments to production per day/week/month.
- Lead Time for Changes: Time from commit to code running in production.
- Change Failure Rate: Percentage of deployments causing production failures.
- Mean Time to Restore Service (MTTR): Average time to restore service after a failure.
- Build Success Rate: Ratio of successful builds to total builds.
- Build Time: Average time taken to complete a build.
- Test Pass Rate: Percentage of tests that pass during the CI process.
- Test Execution Time: Time taken to run the test suite.
- Code Coverage: Percentage of code covered by automated tests.
- Deployment Duration: Time taken to deploy code to production.
- Number of Commits: Total number of commits in a given period.
- Merge Request Throughput: Number of merge requests completed in a given period.
- Code Review Time: Average time taken to complete code reviews.
- Cycle Time: Time taken from work start to work end (including all stages of development).
- Artifact Size: Size of the generated build artifacts.
- Pipeline Failure Rate: Percentage of CI/CD pipelines that fail.
- Queue Time: Time spent waiting in the queue before the build starts.
- Infrastructure Cost: Cost associated with running CI/CD infrastructure.
- Resource Utilization: Efficiency of resource usage during CI/CD processes.
- Deployment Risk Metrics: Indicators measuring the risk associated with a deployment.
- Incident Count: Number of incidents reported after deployments.
- Average Hotfixes per Release: Average number of hotfixes deployed per release.
- Bug Fix Rate: Ratio of bugs fixed to new bugs reported.
- Feature Delivery Rate: Number of new features delivered per release cycle.
- By using these tools and metrics, teams can gain comprehensive insights into their CI/CD processes, helping them improve efficiency, reliability, and overall performance.