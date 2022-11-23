param storageAccountName string
param location string = resourceGroup().location
param tagEnvironment string
param tagProject string
param queueName string
param tableName string



// STORAGE ACCOUNT RESOURCE
resource storageAccount_resource 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  name: storageAccounts_piplantstorage_name
  location: location
  tags: {
    environment: tagEnvironment
    project: tagProject
  }
  sku: {
    name: 'Standard_LRS'
    tier: 'Standard'
  }
  kind: 'StorageV2'
  properties: {
    defaultToOAuthAuthentication: false
    publicNetworkAccess: 'Enabled'
    allowCrossTenantReplication: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: true
    allowSharedKeyAccess: true
    networkAcls: {
      bypass: 'AzureServices'
      virtualNetworkRules: []
      ipRules: []
      defaultAction: 'Allow'
    }
    supportsHttpsTrafficOnly: true
    encryption: {
      requireInfrastructureEncryption: false
      services: {
        file: {
          keyType: 'Account'
          enabled: true
        }
        blob: {
          keyType: 'Account'
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    accessTier: 'Hot'
  }
}


// STORAGE QUEUE RESOURCE
resource storageAccountsQueue_resource 'Microsoft.Storage/storageAccounts/queueServices/queues@2021-09-01' = {
  parent: Microsoft_Storage_storageAccounts_queueServices_storageAccounts_piplantstorage_name_default
  name: queueName
  properties: {
    metadata: {}
  }
  dependsOn: [
    storageAccount_resource
  ]
}


// STORAGE TABLE RESOURCE
resource storageAccountsTable_resource 'Microsoft.Storage/storageAccounts/tableServices/tables@2021-09-01' = {
  parent: Microsoft_Storage_storageAccounts_tableServices_storageAccounts_piplantstorage_name_default
  name: tableName
  properties: {}
  dependsOn: [
    storageAccount_resource
  ]
}
