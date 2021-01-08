package org.chvasu.sans.project;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

import org.zaproxy.clientapi.core.ApiResponse;
import org.zaproxy.clientapi.core.ApiResponseElement;
import org.zaproxy.clientapi.core.ClientApi;
import org.zaproxy.clientapi.core.ClientApiException;

public class ScriptBasedAuthenticatedScan {

    private static final String ZAP_ADDRESS = "myproxyserver";
    private static final int ZAP_PORT = 9090;
    private static final String ZAP_API_KEY = "mysecretapikey";
    private static final String contextId = "1";
    private static final String contextName = "Default Context";
    private static final String target = "http://myappserver:3000";
    private static void setIncludeAndExcludeInContext(ClientApi clientApi) throws UnsupportedEncodingException, ClientApiException {
        String includeInContext = "http://myappserver:3000.*";
        clientApi.context.includeInContext(contextName, includeInContext);
        clientApi.context.excludeFromContext(contextName, "\\Qhttp://myappserver:3000/login.php\\E");
        clientApi.context.excludeFromContext(contextName, "\\Qhttp://myappserver:3000/logout.php\\E");
        clientApi.context.excludeFromContext(contextName, "\\Qhttp://myappserver:3000/setup.php\\E");
        clientApi.context.excludeFromContext(contextName, "\\Qhttp://myappserver:3000/security.php\\E");
    }
    private static void setLoggedInIndicator(ClientApi clientApi) throws UnsupportedEncodingException, ClientApiException {
        // Prepare values to set, with the logged in indicator as a regex matching the logout link
        String loggedInIndicator = "\\Q<a href=\"logout.php\">Logout</a>\\E";
        String loggedOutIndicator = "(?:Location: [./]*login\\.php)|(?:\\Q<form action=\"login.php\" method=\"post\">\\E)";
        // Actually set the logged in indicator
        clientApi.authentication.setLoggedInIndicator( contextId, loggedInIndicator);
        clientApi.authentication.setLoggedOutIndicator( contextId, loggedOutIndicator);
        // Check out the logged in indicator that is set
        System.out.println("Configured logged in indicator regex: "
                + ((ApiResponseElement) clientApi.authentication.getLoggedInIndicator(contextId)).getValue());
    }
    private static void setScriptBasedAuthenticationForDVWA(ClientApi clientApi) throws ClientApiException,
            UnsupportedEncodingException {
        String postData = "username={%username%}&password={%password%}" + "&Login=Login&user_token={%user_token%}";
        String postDataEncode = URLEncoder.encode(postData, "UTF-8");
        String sb = ("scriptName=visscript.js&Login_URL=http://myappserver:3000/login.php&CSRF_Field=user_token&")
                .concat("POST_Data=").concat(postDataEncode);

        clientApi.authentication.setAuthenticationMethod(contextId, "scriptBasedAuthentication", sb.toString());
        System.out.println("Authentication config: " + clientApi.authentication.getAuthenticationMethod(contextId).toString(0));
    }
    private static String setUserAuthConfigForDVWA(ClientApi clientApi) throws ClientApiException, UnsupportedEncodingException {
        // Prepare info
        // These credentials can be read either from a property file or from a pipeline (e.g. Jenkins Credentails). For test purpose, these are hardcoded here.
        String user = "Admin";
        String username = "admin";
        String password = "password";

        // Make sure we have at least one user
        String userId = extractUserId(clientApi.users.newUser(contextId, user));

        // Prepare the configuration in a format similar to how URL parameters are formed. This
        // means that any value we add for the configuration values has to be URL encoded.
        StringBuilder userAuthConfig = new StringBuilder();
        userAuthConfig.append("Username=").append(URLEncoder.encode(username, "UTF-8"));
        userAuthConfig.append("&Password=").append(URLEncoder.encode(password, "UTF-8"));

        System.out.println("Setting user authentication configuration as: " + userAuthConfig.toString());
        clientApi.users.setAuthenticationCredentials(contextId, userId, userAuthConfig.toString());
        clientApi.users.setUserEnabled(contextId, userId, "true");
        clientApi.forcedUser.setForcedUser(contextId, userId);
        clientApi.forcedUser.setForcedUserModeEnabled(true);

        // Check if everything is set up ok
        System.out.println("Authentication config: " + clientApi.users.getUserById(contextId, userId).toString(0));
        return userId;
    }
    private static void uploadScript(ClientApi clientApi) throws ClientApiException {
        String script_name = "visscript.js";
        String script_type = "authentication";
        String script_engine = "Oracle Nashorn";
        String file_name = "C:\\Users\\vchir\\OWASP ZAP\\scripts\\scripts\\authentication\\visscript.js";
        clientApi.script.load(script_name, script_type, script_engine, file_name, null);
    }
    private static String extractUserId(ApiResponse response) {
        return ((ApiResponseElement) response).getValue();
    }
    private static void scanAsUser(ClientApi clientApi, String userId) throws ClientApiException {
        clientApi.spider.scanAsUser(contextId, userId, target, null, "true", null);
    }
    /**
     * The main method.
     *
     * @param args the arguments
     * @throws ClientApiException
     * @throws UnsupportedEncodingException
     */
    public static void main(String[] args) throws ClientApiException, UnsupportedEncodingException {
        ClientApi clientApi = new ClientApi(ZAP_ADDRESS, ZAP_PORT, ZAP_API_KEY);
        uploadScript(clientApi);
        setIncludeAndExcludeInContext(clientApi);
        setScriptBasedAuthenticationForDVWA(clientApi);
        setLoggedInIndicator(clientApi);
        String userId = setUserAuthConfigForDVWA(clientApi);
        scanAsUser(clientApi, userId);
        createHTMLReport(clientApi);        
    }
    
	private static void createHTMLReport(ClientApi clientApi) throws ClientApiException, UnsupportedEncodingException {		
		try (FileOutputStream fos = new FileOutputStream("C:\\ScriptScanReport.html")) {
			   fos.write(clientApi.core.htmlreport());
			   fos.close(); 
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		
	}

}
