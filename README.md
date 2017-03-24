# XL Release Skytap Plugin

[![Build Status](https://travis-ci.org/xebialabs-community/xlr-skytap-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-skytap-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e52529bdd2204207950a28876d02136b)](https://www.codacy.com/app/erasmussen39/xlr-skytap-plugin?utm_source=github.com&utm_medium=referral&utm_content=xebialabs-community/xlr-skytap-plugin&utm_campaign=badger)
[![Code Climate](https://codeclimate.com/github/xebialabs-community/xlr-skytap-plugin/badges/gpa.svg)](https://codeclimate.com/github/xebialabs-community/xlr-skytap-plugin)

## Preface
This document describes the functionality provide by the `xlr-skytap-plugin`

## Overview
This module offers a basic interface to Skytap functionality.

## Installation
Copy the plugin JAR file into the `SERVER_HOME/plugins` directory of XL Release.

## Skytap Authentication
Configures the credentials used to authenticate with the Skytap REST API. You should use the API security token shown on your [account](https://cloud.skytap.com/account) as the password. 
![SkytapAuthenticationConfiguration](images/SkytapAuthenticationConfiguration.png)

## Available Tasks
The available tasks for interfacing with Skytap. These tasks utilize the Skytap REST API and the provided Skytap Authentication Configuration.

![SkytapTaskList](images/SkytapTaskList.png)

#### Add Environment To Project 
Adds the specified Environment to the specified Project.

![SkytapAddEnvironmentToProject](images/SkytapAddEnvironmentToProject.png)

#### Add Template To Project 
Adds the specified Template to the specified Project.

![SkytapAddTemplateToProject](images/SkytapAddTemplateToProject.png)

#### Asset List 
Lists the Assets visible to the authenticated user.

![SkytapAssetList](images/SkytapAssetList.png)

#### Create Environment 
Creates an Environment from the specified Template ID. Optionally you can specify a Project ID to add the Environment to.

![SkytapCreateEnvironment](images/SkytapCreateEnvironment.png)

#### Create Project
Creates a Project with the specified name.

![SkytapCreateProject](images/SkytapCreateProject.png)

#### Delete Environment
Deletes the specified Environment.

![SkytapDeleteEnvironment](images/SkytapDeleteEnvironment.png)

#### Delete Project
Deletes the specified Project.

![SkytapDeleteProject](images/SkytapDeleteProject.png)

#### Environment List
Lists the Environments visible to the authenticated user.

![SkytapEnvironmentList](images/SkytapEnvironmentList.png)

#### Environment VM List
Lists the VMs for the specified Environment.

![SkytapEnvironmentVMList](images/SkytapEnvironmentVMList.png)

#### Get Environment
Get the details of the specified Environment.

![SkytapGetEnvironment](images/SkytapGetEnvironment.png)

#### Project List
Lists the Projects visible to the authenticated user.

![SkytapProjectList](images/SkytapProjectList.png)

#### Start Environment
Starts the VMs in the specified Environment.

![SkytapStartEnvironment](images/SkytapStartEnvironment.png)

#### Template List
Lists the Templates visible to the authenticated user.

![SkytapTemplateList](images/SkytapTemplateList.png)

#### User List
Lists the Users visible to the authenticated user.

![SkytapUserList](images/SkytapUserList.png)

---

## Development
There is a basic Skytap Authentication configuration as well as a XL Release Template leveraging the current Skytap functionality available in Docker. 
Execute: `./gradlew runDockerCompose` 

![SkytapReleaseTemplate](images/SkytapReleaseTemplate.png)

--- 

## References:
* [Skytap REST API](http://help.skytap.com/api.html)
