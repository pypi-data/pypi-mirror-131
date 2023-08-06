import logbook

from keycloak import KeycloakOpenID

from cloud_sdk.state_service_client import StateServiceClient
import cloud_sdk.sdk


def get_user_token(login, password):
    client = KeycloakOpenID(server_url="http://dev-keycloak.apps.d0-oscp.corp.dev.vtb/auth/",
                            client_id="portal-cli",
                            realm_name="Portal",
                            verify=False)

    token = client.token(login, password, scope="offline_access")
    return token["access_token"]


def main():
    with logbook.FileHandler("ss.log"):

        token = "d3a6567b98b55d3deb929e27d80bc44d93d10aa7"
        client = StateServiceClient("http://d2puos-ap2001ln.corp.dev.vtb/", token, timeout=1)
        for i in range(100000):
            try:
                q = client.events.list(order_id="05a3600d-2e35-4826-ba84-3382243722a7")
            except Exception as e:
                print(e)






# http://dev-kong-service.apps.d0-oscp.corp.dev.vtb/product-catalog/graphs/4735c177-a66c-4184-9bc4-cafec0a69de6/?version=1.0.14



if __name__ == "__main__":
    main()

