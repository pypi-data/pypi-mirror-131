![PowerBot Logo](https://www.powerbot-trading.com/wp-content/uploads/2018/03/PowerBot_Weblogo.png "PowerBot")

# **PowerBot Clients**

This repository serves as a way to host and publish PowerBot clients.

### Checklist

The following checklist outlines the necessary steps to take in order to publish a new version of the PowerBot Clients for Python.

1. The auto-update workflow regularly checks if there are any changes in the swagger file on PowerBot staging/development. If changes have been detected, a new
   pull request is created. This PR includes the updated swagger file as well as the corresponding Python clients, which were generated with the respective
   parameterization as seen in the [configs](./configs) directory.
2. Before making a new release, make sure that the clients were built from the correct version of the swagger definition.
3. Update both setup files (e.g. bump version number to match API specification). Make sure that the clients are compatible with the specified dependency
   versions.
4. Tag the latest commit with the corresponding PowerBot version (*git tag <tag_name> <commit_hash>*). This will trigger a GitHub Workflow, which automatically uploads both packages to test.pypi.
5. Make sure that the jobs ran successfully. Test that the packages have been published to test.pypi as intended.
6. Create a new release on GitHub. This will trigger a GitHub Workflow, which automatically uploads both packages to the regular pypi.