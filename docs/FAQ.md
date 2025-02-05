# FAQ

## Docker Installation Failure  
- **Issue**: Errors occur when pulling Docker images or running Docker containers.  
- **Resolution**: No significant anomalies have been detected in current tests. Please refer to the [Docker official documentation](https://docs.docker.com/). If the issue persists, save the complete environment information and logs, then submit the problem following the instructions in the [**Issue Reporting**](#issue-reporting) section.  

## RUN Button Inactive  
- **Issue**: The RUN button remains grayed out even after placing data and configuring parameters.  
- **Resolution**: Verify that:  
  1. Data is stored in the designated subfolder under `data_path` (e.g., `data_path/visium`).  
  2. Files are correctly named and complete (refer to data requirements in [4 Basic Pipeline]).  
  3. The **File Input** checkbox in the sidebar is re-selected to confirm data validation.  
  Once data passes integrity checks, the RUN button will turn yellow and become clickable.  

## Web Page Deployment  
- **Issue**: Failure to deploy the local web interface.  
- **Resolution**: Ensure:  
  1. Shiny Server is properly installed and running.  
  2. Firewall settings allow access to the specified port (default: `3838`).  

## Issue Reporting  

We fully acknowledge that the current version requires further refinement. We sincerely apologize for any inconvenience and commit to the following:  

1. **Response Mechanism** 
   For any technical issues encountered, contact us via **Github Issue** or email at **gyxu_123@163.com**. Please include core code snippets and error logs to facilitate rapid reproduction and resolution.  

2. **Fix Commitment** 
   All valid feedback will receive an initial response within **24 hours**, with critical issues tagged (**Label**) for prioritized tracking. We will: 
   ✅ Thoroughly review and discuss every reported issue/suggestion, providing comprehensive feedback. 
   ✅ Prioritize fixes for defects impacting core workflows. 
   ✅ Release periodic updates, with urgent patches for major defects. 
   ✅ Publish repair progress and version previews in update logs.  

3. **Collaboration Program** 
   Special thanks to developers who help improve Molo through feedback! Contributors of:  
   
   - Valid Issue submissions  
   - Reproducible anomaly cases  
   - Optimization suggestions 
   will be listed on the project’s **Contributors** honor wall.  
   
   We also welcome participation in beta testing for new versions and actionable improvement proposals. Every piece of feedback drives Molo’s evolution. We pledge to continuously enhance toolchain stability and collaborate with the community to advance spatial omics standardization!
