param tableConnectionString string

module AzureStorageAccount 'modules/storage_account.bicep' = {
  name: 'DeployAzureStorageAccount'
  params: {
    storageAccountName: 'sciotstorage'
    tagEnvironment: 'dev'
    tagProject: 'iot-plant-monitoring'
    queueName: 'IOTPlantData'
    tableName: 'IOTPlantData'
  }
}


module AzureFunctionApp 'modules/functions_app.bicep' = {
  name: 'DeployAzureFunctionApp'
  params: {
    functionAppName: 'fa-iot-plant-api'
    tagEnvironment: 'dev'
    tagProject: 'iot-plant-monitoring'
    tableConnectionString: tableConnectionString
    hostingPlanName: 'asp-iot-plant-monitoring'
    storageAccountId: AzureStorageAccount.outputs.storageAccountId
  }
}


