# Cloud Run Inference

Our Cloud Build (and Deploy) is invoked through webhook by the Github action, [DeployAI](https://github.com/neilsong/word-counter-bot-dev/blob/master/.github/workflows/DeployAI.yml), checking for changes in this directory of the repo on push. If you choose to replicate this, costs can be saved by setting a lifecycle rule on the automatically created artifacts bucket or using [GCR Cleaner](https://github.com/sethvargo/gcr-cleaner) to clean untagged images in GCR.

There is no testing documentation for 2 reasons.  
 1. All substitutions (env_variables) are specified for our own CI/CD Pipeline with Cloud Build
 2. Looking through the Max Woolf's `gpt-cloud-run` repo's section on Cloud Build ([here](https://github.com/minimaxir/gpt-2-cloud-run/blob/master/cloud_build.md)) should be enough to get you started.