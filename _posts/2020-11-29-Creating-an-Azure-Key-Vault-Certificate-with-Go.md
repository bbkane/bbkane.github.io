---
layout: default
title: Creating an Azure Key Vault Certificate with Go
---

So... I need to make a TLS certificate in an Azure Key Vault with Go. I thought this would be easy - just authenticate, then make the certificate. However, the Go SDK seems mostly auto-generated and is truly pitifully documented. Here's how I ended up creating my certificate.

## Get a dev Key Vault

The first thing to do is to make a Key Vault and a Service Principal to access it - This is doable through the portal, or, if you want to use the command line, [this blog post](https://withblue.ink/2019/04/07/getting-tls-certificates-from-azure-key-vault-with-go.html) explains how with the Azure CLI - this post is also worth reading for its explanation of authorizing to Key Vault. I ended up using Terraform to create my Key Vault and Service Principal. A bit slower to get started, but I find Terraform code more readable than a shell script.

You can see Service Principals at the [App registrations](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps) page. Mine's in the "All applications" tab. This gives you the Client ID and the Tenant ID needed to log in, as well as letting you reset the client secret if you didn't save it on SP creation.

## Logging in as a Service Principal

### With the Azure CLI

I tested the Service Principal and its access with the following commands:

```
az login \
    --service-principal \
    -u $client_id \
    -p "$client_secret" \
    --tenant "$tenant_id"
```

```
az keyvault show -n concert-eaus2-dev-kv -g concert-eaus2-dev-rg
```

### With Go code

The blog post above (and [this one](https://blog.abhi.host/blog/2019/08/17/fetch-certificates-from-keyvault-in-go/) by my friend Abhijeet) log in as an SP with environmental variables. I don't want to use environmental variables - I plan to put my tenant ID, my client ID, and my client secret in a config, so I went looking for other ways to log in.

I found the Azure Samples [repo](https://github.com/Azure-Samples/azure-sdk-for-go-samples/tree/master/keyvault/examples) which also uses environmental variables - `authorizer, err := kvauth.NewAuthorizerFromEnvironment()`. No problemo, I thought, I'll check out the docs for that and it'll show me the other ways to login.

The docs are @$%^ing useless. Check out [this gem](https://godoc.org/github.com/Azure/azure-sdk-for-go/services/keyvault/auth):

![auth godoc screenshot]({{ site.baseurl }}/img/2020-11-29-Creating-an-Azure-Key-Vault-Certificate-with-Go/auth_godoc.png)

Let's pick on `NewAuthorizerFromEnvironment` for a second. It basically says it "uses environmental variables". The environment is a big place, Mr. Documentation Guy!! Fortunately, [the README](https://github.com/Azure-Samples/azure-sdk-for-go-samples/tree/master/keyvault/examples) explains how to make a Managed Service Identity and the example source code contain comments about which environmental variables to export.

Unfortunately, none of the methods there help me authenticate. So I went source code spelunking through the functions these methods called and found [`ClientCredentialsConfig`](https://godoc.org/github.com/Azure/go-autorest/autorest/azure/auth#ClientCredentialsConfig). Here's a program to authenticate the keyvault client with Azure.

```go
package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/Azure/azure-sdk-for-go/profiles/latest/keyvault/keyvault"
	"github.com/Azure/go-autorest/autorest/azure"
	arauth "github.com/Azure/go-autorest/autorest/azure/auth"
)

func main() {
	// authorize with SPI
	clientSecret, exists := os.LookupEnv("sp_client_secret")
	if !exists {
		fmt.Printf("Don't see the password")
		os.Exit(1)
	}

	clientID := "34a6b681-4..."
	tenentID := "2cd5e3a0-3..."

	clientCredConfig := arauth.NewClientCredentialsConfig(clientID, clientSecret, tenentID)
	clientCredConfig.Resource = strings.Trim(azure.PublicCloud.KeyVaultEndpoint, "/")
	authorizer, err := clientCredConfig.Authorizer()

	if err != nil {
		fmt.Printf("unable to create vault authorizer: %v\n", err)
		os.Exit(1)
	}

	basicClient := keyvault.New()
	basicClient.Authorizer = authorizer
}
```

## Creating the certificate

Ok, let's create the certificate. The [Go Docs](https://godoc.org/github.com/Azure/azure-sdk-for-go/services/keyvault/2016-10-01/keyvault#BaseClient.CreateCertificate) contain very little other than the raw types, but I was able to cross-reference it with the [REST API Docs](https://docs.microsoft.com/en-us/rest/api/keyvault/createcertificate/createcertificate) and the the output of `az keyvault certificate show --name example --vault-name concert-kv-dev-weus2` (a certificate I made in the portal) to get parameters that seem to work.

Before the code, here are some notes.

- First off, the exact code in the following section is ripped out of a larger function and slightly modified, so there might be some small typos.
- Second, I'm trying to represent all fields possible (I might want to fill more of them in later), so I'm explicitly setting some things to `nil` instead of letting Go implicitly do it.
- Tertiarily, If you pass the ID of a certificate that already exists in your keyvault, it'll create a new version of that certificate with your new info. I wish there was a way to turn off this behavior, but I doubt there is.
- Finally, there are a lot of pointers in this call, and Go doesn't let you take the address of a raw value, so I'm using the following functions to get pointers to their parameters.

```go
// go doesn't allow addresses to constants, but it does to parameters
// Checkmate, athiests!
func boolPtr(v bool) *bool       { return &v }
func int32Ptr(v int32) *int32    { return &v }
func stringPtr(v string) *string { return &v }
```

```go
vaultName := "avengers-keyvault"
id := "my-cert-id"
commonName := "example.com"
san := []string{"www.example.com", "example.com"}
baseURL := "https://" + vaultName + ".vault.azure.net"
result, err := basicClient.CreateCertificate(
    context.Background(),
    baseURL,
    id,
    keyvault.CertificateCreateParameters{
        CertificateAttributes: nil, // godocs say it can be nil and the REST API example omits it
        CertificatePolicy: &keyvault.CertificatePolicy{
            // Not adding Response field, we'll use the default value
            ID: nil, // this is only useful in a response
            KeyProperties: &keyvault.KeyProperties{
                Exportable: boolPtr(true),
                KeyType:    stringPtr("RSA"),
                KeySize:    int32Ptr(2048),
                ReuseKey:   boolPtr(false),
            },
            SecretProperties: &keyvault.SecretProperties{
                ContentType: stringPtr("application/x-pkcs12"),
            },
            X509CertificateProperties: &keyvault.X509CertificateProperties{
                Subject: stringPtr("CN=" + commonName),
                Ekus:    nil,
                SubjectAlternativeNames: &keyvault.SubjectAlternativeNames{
                    DNSNames: &san,
                },
                KeyUsage:         nil,
                ValidityInMonths: int32Ptr(6),
            },
            LifetimeActions: &[]keyvault.LifetimeAction{
                {
                    Trigger: &keyvault.Trigger{
                        LifetimePercentage: nil,
                        DaysBeforeExpiry:   int32Ptr(30),
                    },
                    Action: &keyvault.Action{
                        ActionType: keyvault.AutoRenew,
                    },
                },
            },
            IssuerParameters: &keyvault.IssuerParameters{
                Name: stringPtr("Self"),
                // NOTE: az keyvault show shows a "certificateTransparency"
                // field that's not in the Go API
                CertificateType: nil,
            },
            // Not in the REST API and it looks like a repeat of CertificateAttributes
            Attributes: nil,
        },
        Tags: map[string]*string{"key": stringPtr("value")},
    },
)
```

Finally! We have a certificate in ~50 lines of code...

