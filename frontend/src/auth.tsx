import { Log, User, UserManager } from "oidc-client";

export class Constants {
    public static stsAuthority =
        "https://id.t.newstore.net/auth/realms/gabriel-NA-43928/";
    public static clientId = "fake-nom";
    public static clientRoot = "https://keycloak.fulltest.co";
    public static clientScope =
        "openid profile email template:read template:write";

    public static apiRoot = "https://keycloak.fulltest.co/api/";
}

export class AuthService {
    public userManager: UserManager;

    constructor() {
        const settings = {
            authority: Constants.stsAuthority,
            client_id: Constants.clientId,
            redirect_uri: `${Constants.clientRoot}/oauth2/callback`,
            silent_redirect_uri: `${Constants.clientRoot}/oauth2/refresh`,
            // tslint:disable-next-line:object-literal-sort-keys
            post_logout_redirect_uri: `${Constants.clientRoot}`,
            response_type: "code",
            scope: Constants.clientScope
        };
        this.userManager = new UserManager(settings);

        Log.logger = console;
        Log.level = Log.INFO;
    }

    public login(): Promise<void> {
        return this.userManager.signinRedirect();
    }

    // public renewToken(): Promise<User> {
    //     return this.userManager.signinSilent();
    // }

    public logout(): Promise<void> {
        return this.userManager.signoutRedirect();
    }
    public handleCallback(): Promise<User> {
        return new UserManager({
            response_mode: "query"
        }).signinRedirectCallback();
    }
}
