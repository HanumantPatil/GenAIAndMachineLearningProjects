@description('Globally unique name for the Microsoft Foundry resource.')
param accountName string

@description('Azure region that supports Content Understanding.')
@allowed([
  'australiaeast'
  'eastus'
  'eastus2'
  'japaneast'
  'northeurope'
  'southcentralus'
  'southeastasia'
  'swedencentral'
  'uksouth'
  'westeurope'
  'westus'
  'westus3'
])
param location string = 'eastus'

@description('Object ID of a user, service principal, or managed identity. Leave empty to skip role assignment.')
param principalId string = ''

resource foundryAccount 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: accountName
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: { type: 'SystemAssigned' }
  properties: {
    customSubDomainName: accountName
    disableLocalAuth: false
    publicNetworkAccess: 'Enabled'
  }
  tags: {
    workload: 'content-understanding-workshop'
    scenario: 'invoice'
  }
}

var cognitiveServicesUserRoleId = subscriptionResourceId(
  'Microsoft.Authorization/roleDefinitions',
  'a97b65f3-24c7-4388-baec-2e87135dc908'
)

resource contentUnderstandingAccess 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(foundryAccount.id, principalId, cognitiveServicesUserRoleId)
  scope: foundryAccount
  properties: {
    principalId: principalId
    roleDefinitionId: cognitiveServicesUserRoleId
  }
}

output accountId string = foundryAccount.id
output endpoint string = foundryAccount.properties.endpoint
output managedIdentityPrincipalId string = foundryAccount.identity.principalId
