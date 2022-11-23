param subscriptionId string = subscription().id
param serverFarmResourceGroup = resourceGroup().name
param location string = resourceGroup().location
param functionAppName string
param hostingPlanName string
param tableConnectionString string
param tagEnvironment string
param tagProject string
param storageAccountId string

resource azureFunctionAppServicePlan 'Microsoft.Web/serverfarms@2018-11-01' = {
  name: hostingPlanName
  location: location
  kind: 'linux'
  tags: {
    environment: tagEnvironment
    project: tagProject
  }
  properties: {
    name: hostingPlanName
    workerSize: '0'
    workerSizeId: '0'
    numberOfWorkers: '1'
    reserved: true
  }
  sku: {
    Tier: 'Dynamic'
    Name: 'Y1'
  }
  dependsOn: []
}


resource azureFunction 'Microsoft.Web/sites@2018-11-01' = {
  name: functionAppName
  kind: 'functionapp,linux'
  location: location
  tags: {
    environment: tagEnvironment
    project: tagProject
  }
  properties: {
    name: functionAppName
    siteConfig: {
      appSettings: [
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'AzureWebJobsStorage'
          value: storageAccountId
        }
        {
          name: 'TABLE_CONNECTION_STRING'
          value: tableConnectionString
        }
      ]
      cors: {
        allowedOrigins: [
          'https://portal.azure.com'
        ]
      }
      use32BitWorkerProcess: use32BitWorkerProcess
      linuxFxVersion: linuxFxVersion
    }
    serverFarmId: '/subscriptions/${subscriptionId}/resourcegroups/${serverFarmResourceGroup}/providers/Microsoft.Web/serverfarms/${hostingPlanName}'
    clientAffinityEnabled: false
  }
  dependsOn: [
    azureFunctionAppServicePlan
  ]
}
