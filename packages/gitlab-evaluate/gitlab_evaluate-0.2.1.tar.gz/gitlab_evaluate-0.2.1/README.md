# Evaluate
Evaluate is a script that can be run to gather information about projects from a gitlab self-managed instance. This information is useful to the GitLab Professional Services (PS) team to accurately scope migration services. 

## Use Case
GitLab PS plans to share this script with a Customer to run against their self managed instance. Then the customer can send back the output files to enable GitLab engagement managers to scope engagements accurately. 

## Install

```
pip install gitlab_evaluate
```

## Usage

```bash
# For evaluating a GitLab instance
evaluate-gitlab -p <access-token-with-api-admin-privileges> -s https://gitlab.example.com

# For evaluating a single git repo's CI readiness
evaluate-ci-readiness -r|--repo <git-repo-url>
```

## Using a docker container

[Docker containers with evaluate installed](https://gitlab.com/gitlab-org/professional-services-automation/tools/utilities/evaluate/container_registry) are also available to use.

### Local usage

```bash
# Spin up container
docker run --name evaluate -it registry.gitlab.com/gitlab-org/professional-services-automation/tools/utilities/evaluate:latest /bin/bash

# In docker shell
evaluate-ci-readiness -r|--repo <git-repo-url>
evaluate-gitlab -p <access-token-with-api-admin-privileges> -s https://gitlab.example.com
```

### Example GitLab CI job using evaluate ci readiness script

```yaml
evaluate node-js:
  stage: test
  script:
    - evaluate-ci-readiness --repo=https://github.com/nodejs/node.git
  artifacts:
    paths:
      - node.csv
```

To **test**, consider standing up local docker container of gitlab. Provision a personal access token of a user who has system admin priviledges. Create multiple projects with varying number of commits, pipelines, merge requests, issues. Consider importing an open source repo or using [GPT](https://gitlab.com/gitlab-org/quality/performance) to add projects to the system.  

## Design
Design for the script can be found [here](https://gitlab.com/gitlab-com/customer-success/professional-services-group/ps-leadership-team/ps-practice-management/-/issues/83)

## Project Thresholds
_Below are the thresholds we will use to determine whether a project can be considered for normal migration or needs to have special steps taken in order to migrate_ 

### Project Data
- Pipelines - 1,500 max
- Issues - 1,500 total (not just open)
- Merge Requests - 1,500 total (not just merged)
- Container images - 400 images, 150GB total disk, individual image 2GB

### Repo Data
- commits - 20K
- branches - 1K
- tags - 1K
- Disk Size - 10GB
