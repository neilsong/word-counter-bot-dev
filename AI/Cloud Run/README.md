# Cloud Run Inference

Our Cloud Run Inference is manually invoked by a GitHub action checking for changes in this directory of the repo on push.

There is no testing documentation for 2 reasons.  
 1. All substitutions (env_variables) are specified for our own CI/CD Pipeline with Cloud Build
 2. Looking through the `gpt-2-cloud-run` repo's section on Cloud Build should be enough to get you started.