# Cloud Run Inference

Our Cloud Run Inference is manually invoked by a GitHub action checking for changes in this directory of the repo on push.

There is no testing documentation for 2 reasons.  
 1. All substitutions (env_variables) are specified for our own CI/CD Pipeline with Cloud Build
 2. Looking through the Max Woolf's `gpt-cloud-run` repo's section on Cloud Build ([here](https://github.com/minimaxir/gpt-2-cloud-run/blob/master/cloud_build.md)) should be enough to get you started.