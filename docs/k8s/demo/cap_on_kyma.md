# Build CAP Application on Kyma

This is the memo of self-practice following the tutorials from [Deploy Your CAP Application on SAP BTP Kyma Runtime](https://developers.sap.com/mission.btp-deploy-cap-kyma.html).

Prerequisites:

* Register account in [Developer@SAP](https://developers.sap.com/).
* Register trial account in [SAP BTP](https://account.hanatrial.ondemand.com/).

Tasks:

* Configure Kyma in SAP Business Technology Platform (SAP BTP) subaccount and prepare Kyma development environment.
* Create an HDI container for an SAP HANA Cloud instance on Cloud Foundry and create credentials for this SAP HANA cloud instance in Kyma cluster.
* Develop a business application using SAP Cloud Application Programming Model (CAP).
* Start on local environment, enhance it with an SAP Fiori UI, add business logic to it, and also roles and authorization check.
* Add a Helm chart to the application, build docker images, push them to your container registry, and deploy your application to your Kyma cluster on SAP BTP.

Local environment:

* Applel Silicon M1 chipset
* macOS 12.6 (command `sw_vers`)
* Nodejs version:
* CDS version:
* jq - for JSON processing in CLI (`brew install jq`)

## SAP BTP subaccount configuration

For the SAP BTP free tier, the recommendation is as well to use an AWS-based subaccount. Kyma runtime in the free tier is only available on AWS.

Choose the entitlements for the subdomain:

* Alert Notification: Standard plan
* Continuous Integration & Delivery: default (Application) or the trial (Application) or free (Application) plans which are not charged
* Kyma runtime: any available plan in the list (trial and free are not charged)
* Launchpad Service: standard (Application) or free (Application)
* SAP HANA Cloud: hana
* SAP HANA Schemas & HDI Containers: hdi-shared

## Set up local BTP environment

Here we will use btp command to set up cloud environment. Details we can refer to help document [Working with Environments Using the btp CLI](https://help.sap.com/docs/BTP/65de2977205c403bbc107264b8eccf4b/48db1553eb18451e8f71fc56d99ede71.html).

Download BTP CLI package `btp-cli-darwin-amd64-<ver_num>.tar.gz` via [link](https://tools.hana.ondemand.com/#cloud) and unpackage it.

```bash
tar xvf btp-cli-darwin-amd64-<ver_num>.tar.gz
```

A new subfolder `darwin-amd64` will be created in current path and a bin file `btp` is under the subfolder. Move file `btp` to folder `/usr/local/bin/`.

```bash
sudo mv ./darwin-amd64/btp /usr/local/bin/
```

Log on to the subaccount on BTP.

```bash
btp login --url https://cpcli.cf.eu10.hana.ondemand.com --subdomain <your_subdomain> --user <your_registered_email_address>
```

Configuration file was stored at `/Users/$USER/Library/Application Support/.btp/config.json`.
In Linux, the configuration file is on `/home/$USER/.config/.btp/config.json`.
We can get current user via command `echo $USER`.

Tips:

* Commands are executed in the target, unless specified otherwise using a parameter. To change the target, use `btp target`.
* For an explanation of the targeting mechanism, use `btp help target`.

Get the subaccount ID in BTP and we will know that kyma and cloundfoundry are available in current trial account.

```bash
btp list accounts/available-environment --subaccount <your_subaccount_id>
```

Get details about an environment available for a subaccount

```bash
btp get accounts/available-environment --subaccount <your_subaccount_id> --environment cloudfoundry --service cloudfoundry --plan standard
btp get accounts/available-environment --subaccount <your_subaccount_id> --environment kyma --service kymaruntime --plan trial
```

Get status running instances. Here we will also get environment ID of running instances.

```bash
btp list accounts/environment-instance --subaccount <your_subaccount_id>
```

Delete a running instance if needed.

```bash
btp delete accounts/environment-instance <environment_ID> --subaccount <your_subaccount_id>
```

Create Kyma instance.

```bash
btp create accounts/environment-instance --subaccount <your_subaccount_id> --environment kyma --service kymaruntime --plan trial --parameters '{"name": "<your_kyma_instance_name>"}'
btp get accounts/environment-instance <environment_ID> --subaccount <your_subaccount_id>
```

Create CloudFoundry instance

```bash
btp create accounts/environment-instance --subaccount <your_subaccount_id> --environment cloudfoundry --service cloudfoundry --plan standard --parameters '{"instance_name": "<your_cf_instance_name>"}'
btp get accounts/environment-instance <environment_ID> --subaccount <your_subaccount_id>
```

Log onto CF to create space `DEV` by providing API endpoint, Email and Password, which are ready in the subaccount overview page.

```bash
cf login
cf create-space DEV
```

## Install Homebrew

Refer to [installation guide](http://mirrors.ustc.edu.cn/help/brew.git.html?highlight=brew).

Set environment variables

```bash
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.ustc.edu.cn/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.ustc.edu.cn/homebrew-core.git"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles"
```

Install Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://github.com/Homebrew/install/raw/HEAD/install.sh)"
```

Add below in file `~/.zprofile`.

```bash
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.ustc.edu.cn/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.ustc.edu.cn/homebrew-core.git"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles"
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Make it effected.

```bash
source ~/.zprofile
```

## Install kubetcl

The `kubectl` [installation guide](https://kubernetes.io/docs/tasks/tools/#kubectl)

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
sudo chown root: /usr/local/bin/kubectl
kubectl version --client
```

Install plugin [oidc-login](https://github.com/int128/kubelogin#setup).

```bash
curl -fsSLO https://github.com/kubernetes-sigs/krew/releases/latest/download/krew-darwin_arm64.tar.gz
tar xvf krew-darwin_arm64.tar.gz
./krew-darwin_arm64 install krew
```

Add the `$HOME/.krew/bin` directory to the `PATH` environment variable by updating `~/.zprofile`.

```bash
export PATH=$HOME/.krew/bin:$PATH:$PATH
```

Make it effected

```bash
source ~/.zprofile
```

Run `kubectl krew` to check the installation.

Install/uninstall plugin `oidc-login`.

```bash
kubectl krew install oidc-login
kubectl krew uninstall oidc-login
```

## SAP Kyma runtime

In the Overview area of your subaccount open the Link to dashboard link which appears next to the Console URL under the Kyma Environment area.
At the top left of the window choose the Clusters Overview drop down and choose your cluster.
In the Clusters Overview window choose the Download Kubeconfig for your Kyma runtime to download your KUBECONFIG.

Add below to `~/.zprofile` to set the kubeconfig to an environment variable.

```bash
export KUBECONFIG=<your_full_path_of_kubeconfig_file>
```

Make above change effected.

```bash
source ~/.zprofile
```

```bash
chmod 600 <your_full_path_of_kubeconfig_file>
```

Test connection between kubectl and Kyma on BTP.

```bash
kubectl cluster-info
```

## Install Node.js

Refer to [installation guide](https://nodejs.org/en/download/package-manager/)

```bash
brew search node
brew install node@16
brew unlink node
brew link node@16
node -v
```

## Install SQLite

Install SQLite via `brew`.

```bash
brew search sqlite
brew install sqlite
```

Add below to `~/.zprofile`

```bash
export PATH=/opt/homebrew/opt/sqlite/bin:$PATH
```

Make it effected

```bash
source ~/.zprofile
```

## Install Xcode

(For macOS) We have to install Command-Line Tools for [Xcode](https://developer.apple.com/xcode/), cause some node modules need binary modules (node-gyp).

```bash
xcode-select --install
xcode-select --help
```

## Install Git

Refer to [installation guide](https://git-scm.com/downloads).

```bash
brew install git
git version
```

## Install SAPUI5

Install the UI5 CLI.

```bash
npm search --global @ui5/cli
npm install --global @ui5/cli
npm list --global @ui5/cli
ui5 --version
```

```bash
npm search --global grunt-cli
npm install --global grunt-cli
npm list --global grunt-cli
```

## Install CF CLI

Refer to [installation guide](https://github.com/cloudfoundry/cli#installers-and-compressed-binaries).

```bash
brew install cloudfoundry/tap/cf-cli@8
cf --version
```

## Install CAP Tooling

See the details in the [CAP documentation](https://cap.cloud.sap/docs/get-started/in-a-nutshell).

```bash
npm search --global @sap/cds-dk
npm install --global @sap/cds-dk
npm list --global @sap/cds-dk
cds --version
```

## Install VSCode

In VS Code, invoke the Command Palette ( View → Command Palette or ⇧⌘P) and type `shell command` to find the Shell Command: `Install 'code' command in PATH`.

Install `SAP CDS Language Support` extension.

Install `SAP Fiori tools - Extension Pack` extension.

## Install Yeoman

[Yeoman](https://yeoman.io/) is a tool for scaffolding web apps. You’ll need it if you want to carry out the tutorial Add the SAP Launchpad Service.

```bash
npm install --global yo
yo --version
```

## Install Docker

```bash
brew install docker --cask
```

## Install Helm

Refer to [installation guide](https://helm.sh/docs/intro/install/)

```bash
brew install helm
```

## Install Paketo(pack)

Refer to [installation guide](https://buildpacks.io/docs/tools/pack/#install).

```bash
brew install buildpacks/tap/pack
```

## Install Rancher Desktop

Download the Rancher Desktop installer for macOS from the [release page](https://github.com/rancher-sandbox/rancher-desktop/releases).
Refer to [installation guide](https://docs.rancherdesktop.io/getting-started/installation/#macos).

## Download tutorial

Go to tutorial root directory and clone the code.

```bash
git clone https://github.com/SAP-samples/cloud-cap-risk-management tutorial
```

## Initialize the project

Install required Node.js modules in the app directory `cpapp`.

```bash
cd app
cds init
npm install
cds watch
```

## Add files to the project

Copy the file `schema.cds` from `templates/create-cap-application/db` to the `db` folder of the app.
It creates two entities in the namespace `sap.ui.riskmanagement`: `Risks` and `Mitigations`.

Copy the file `risk-service.cds` from `templates/create-cap-application/srv` to the `srv` folder of the app.
It creates a new service `RiskService` in the namespace `sap.ui.riskmanagement`. This service exposes two entities: `Risks` and `Mitigations`, which are exposing the entities of the database schema we've created in the step before.

Copy the folder `data` from `templates/create-cap-application/db` to the `db` folder of the app.
There are two comma-separated value (CSV) files that contain local data for both the `Risks` and the `Mitigations` entities.

Use Fiori Application Generator (VSCode extension) to generate `Risk` UI with Fiori element template.
The generation will create a `risks` and a `webapp` folder with a `Component.js` file in the `app` folder of the project.

Copy the file `risks-service-ui.cds` from `templates/create-ui-fiori-elements/srv` to the `srv` folder of the app. It defines annotations to show a work list with some columns and the data from the service in the `Risk` UI.

Edit `app/risks/webapp/manifest.json` file to make the header fields editable, that is, shows `title` and `description` in `Risk` UI.

Copy the file `risk-service.js` from `templates/cap-business-logic/srv`to the `srv` folder of the app.
It now shows the work list in `Risk` UI with the columns `Priority` and `Impact` with color and an icon, depending on the amount in `Impact`.

Use Fiori Application Generator (VSCode extension) to generate `Migration` UI with Fiori free-style template.
The generation will create a `migrations` and a `webapp` folder with a `Component.js` file in the `app` folder of the project.

Update file `cpapp/app/mitigations/webapp/view/Worklist.view.xml` to show `Description`, `Owner`, and `Timeline` columns, as well as in detail object page.

Till now, our `risks` and `mitigations` application have been generated by the SAP Fiori Tools Generator and can be started independently. They are launched without a launch page.

Copy the file `launchpage.html` from `templates/launchpage/app` to the `app` folder of the app. There are two applications in the launch page with URLs that point to the respective apps. We now see the `Mitigations` app next to the `Risks` app on the launch page.

Open the file `srv/risk-service.cds` and add role restrictions to entities.

Copy the file `templates/cap-roles/.cdsrc.json` to the project directory `cpapp`. The file defines two users `risk.viewer@tester.sap.com` and `risk.manager@tester.sap.com`. The default password can be found in the file `.cdsrc.json`.

We will see the CAP server to show above applications via link <http://localhost:4004>.

## Prepare Kyma Development Environment

Execute `cds version` to make sure the `package.json` is using `@sap/cds 6.0.1` or newer and we have `@sap/cds-dk 6.0.1` or newer globally installed.

Create namespace on Kyma.

```bash
kubectl create namespace risk-management
```

Switch to the namespace.

```bash
kubectl config set-context --current --namespace risk-management
```

Create container registry secret.

Copy the folder `scripts` from `templates/Kyma-Prepare-Dev-Environment` to the project root folder `cpapp`.

In the root folder `cpapp` of the project, run the script to create the secret.

```bash
./scripts/create-container-registry-secret.sh
```

Need provide below input:

```bash
docker-server=https://registry-1.docker.io
docker-username=<your_registered_docker_username>
docker-email=<your_registered_docker_email>
docker-password=<your_api_token>
```

Verify

```bash
kubectl get secret
```

## Set Up SAP HANA Cloud for Kyma

Add SAP HANA support to your project.
This adds the `db` module for SAP HANA access to the `package.json` file.
Execute the command below in the project root directory `cpapp`.

```bash
cds add hana --for production
```

Verify the access to both CF and Kyma by executing below commands.

```bash
cf login
```

```bash
kubectl cluster-info
```

Create HANA Cloud instance `cpapp-db` in CloudFoundry `DEV` namespace. The admin user id is `DBADMIN`.

In the root folder `cpapp` of the project, execute:

```bash
./scripts/create-db-secret.sh cpapp-db
```

Get the host name pattern of the cluster with the following command. Result looks like `*.c-<xyz123>.sap.kyma.ondemand.com`.

```bash
kubectl get gateway -n kyma-system kyma-gateway -o jsonpath='{.spec.servers[0].hosts[0]}'
```

The script will:

* Create service key `cpapp-db-key` for HANA Cloud service instance `cpapp-db` as `<your_btp_registered_email>`.
* Create Kubernetes secret `cpapp-db` for HANA DB instance. View it using `kubectl get secret cpapp-db -o yaml`.

## User Authentication and Authorization (XSUAA) Setup

Set up XSUAA.

```bash
cds add xsuaa --for production
```

Above command will do:

* Adds the XSUAA service to the `package.json` file of the project
* Creates the XSUAA security configuration `xs-security.json` for the project

## Add Helm Chart

Add Helm Chart.

```bash
cds add helm
```

Get docker server URL by command:

```bash
cat ~/.docker/config.json
```

Get the image pull secret for container registry. In the demo, it's `container-registry`.

```bash
kubectl get secret
```

Get the host name pattern of the cluster.

```bash
kubectl get gateway -n kyma-system kyma-gateway -o jsonpath='{.spec.servers[0].hosts[0]}'
```

Open the file `chart/values.yaml`:

* Replace the placeholder `<your-container-registry>` with docker server URL `https://docker.io/`.
* Set `imagePullSecret` with value `name: container-registry`.
* Add host name of the cluster without leading `*.`.
* Add the binding `db` pointing to the SAP HANA Cloud instance secret `cpapp-db`.
* Point the binding `hana` of the SAP HANA Cloud instance secret `cpapp-db`.
* Add the Authorization and Trust Management service to allow user login.

## Deploy CAP Application to Kyma

Build docker image.

```bash
CONTAINER_REGISTRY=https://index.docker.io/v1
CONTAINER_REGISTRY=https://registry-1.docker.io/yuhuihu
CONTAINER_REGISTRY=yuhuihu
```

CAP build.

```bash
cds build --production
```

Build CAP service.

```bash
pack build $CONTAINER_REGISTRY/cpapp-srv --path gen/srv \
 --buildpack gcr.io/paketo-buildpacks/nodejs \
 --builder paketobuildpacks/builder:base
```
