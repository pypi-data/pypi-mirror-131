# PaymentServiceUpdate

Request body for updating an active payment service.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**display_name** | **str** | A custom name for the payment service. This will be shown in the Admin UI. | [optional] 
**fields** | [**[PaymentServiceUpdateFields]**](PaymentServiceUpdateFields.md) | A list of fields, each containing a key-value pair for each field defined by the definition for this payment service e.g. for stripe-card &#x60;secret_key&#x60; is required and so must be sent with in this field. | [optional] 
**accepted_countries** | **[str]** | A list of countries that this payment service needs to support in ISO two-letter code format. | [optional] 
**accepted_currencies** | **[str]** | A list of currencies that this payment service needs to support in ISO 4217 three-letter code format. | [optional] 
**three_d_secure_enabled** | **bool** | Defines if 3-D Secure is enabled for the service (can only be enabled if the payment service definition supports the &#x60;three_d_secure_hosted&#x60; feature). This does not affect pass through 3-D Secure data. | [optional]  if omitted the server will use the default value of False
**acquirer_bin_visa** | **str, none_type** | Acquiring institution identification code for VISA. | [optional] 
**acquirer_bin_mastercard** | **str, none_type** | Acquiring institution identification code for Mastercard. | [optional] 
**acquirer_bin_amex** | **str, none_type** | Acquiring institution identification code for Amex. | [optional] 
**acquirer_bin_discover** | **str, none_type** | Acquiring institution identification code for Discover. | [optional] 
**acquirer_merchant_id** | **str, none_type** | Merchant identifier used in authorisation requests (assigned by the acquirer). | [optional] 
**merchant_name** | **str, none_type** | Merchant name (assigned by the acquirer). | [optional] 
**merchant_country_code** | **str, none_type** | ISO 3166-1 numeric three-digit country code. | [optional] 
**merchant_category_code** | **str, none_type** | Merchant category code that describes the business. | [optional] 
**merchant_url** | **str, none_type** | Fully qualified URL of 3-D Secure requestor website or customer care site. | [optional] 
**active** | **bool** | Defines if this service is currently active or not. | [optional]  if omitted the server will use the default value of True
**position** | **float** | The numeric rank of a payment service. Payment services with a lower position value are processed first. When a payment services is inserted at a position, any payment services with the the same value or higher are shifted down a position accordingly. When left out, the payment service is inserted at the end of the list. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


