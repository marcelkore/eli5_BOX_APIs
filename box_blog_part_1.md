## BOX Python APIs - eli5 Part 1
### Date: 2022-04-16
####  Description: This is a first part of a two part blog that reviews how to interact with BOX APIs.<br>

<br>

This post will review how to use BOX Python SDKs/APIs. I will try to include all the information required (eli5) to help you get started quickly.

We will be reviewing the following topics in this post:
1. Creating a box app
2. Setting up Authentication and Authorization

To follow this guide, please create a free account by following the link

Once you have access to Box, navigate to the following link. This is the developer console where you will create your box app. The link above also
assumes you signed up for a new account. If you are following this with a company account, your URL might look something like
this -> https://<yourorganization.app.box.com.

Below is a screenshot of the page you should be seeing if you have made it this far.

![Create New App Page](https://koremarcelblog.blob.core.windows.net/box-blog/a-box-developer-page.png)

Select the ‘Create New App’ option above to reveal the window below. We will be selecting a Custom App for this post as it serves our specified use cases above.
<br>

![New App Options](https://koremarcelblog.blob.core.windows.net/box-blog/b-create-new-app.png)

<!-- <img src="https://koremarcelblog.blob.core.windows.net/box-blog/b-create-new-app.png" alt = "authentication options" style="width=900px height=550px" /> -->

The following window presents to the user three options for authenticating your application. Each option contains a link to what they each are/and are used for. Feel free to explore and read up on each option before proceeding. We will be selecting the first option, Server Authentication (with JWT). Enter an app name of your choice and click ‘Create App.


![Custom App](https://koremarcelblog.blob.core.windows.net/box-blog/c-auth-options.png)

Navigate to the authorization tab and select **Review and Submit**.

![Authorization Tab](https://koremarcelblog.blob.core.windows.net/box-blog/d-authorization-types.png)

The review app authorization submission window will be displayed. Using a company box account, this request will be routed to your BOX admin. <br>
If you signed up for a BOX account, this request would simply be routed to your email. Enter a brief description and click submit.

![Review App Authorization](https://koremarcelblog.blob.core.windows.net/box-blog/e-submit.png)

If you are using a company account, you will not be able to use a service account with JWT authorization until your administrator approves the app.

![App Pending Authorization](https://koremarcelblog.blob.core.windows.net/box-blog/f-auth-pending-approval.png)

If you have the administrator role, below is where you navigate to approve your app. You should also have received an email where you can follow a <br>
link to approve the application. Navigate back to your account from the developer console. Once you are back to your account at the root level, <br>
you should see the Admin Console option shown below if you are in the administrator role. Click on it. <br>

![Admin Console](https://koremarcelblog.blob.core.windows.net/box-blog/g-admin-console.png)

Navigate to apps

![Apps Tab Location](https://koremarcelblog.blob.core.windows.net/box-blog/h-app-section.png)

Once in the app’s windows, click on the Custom Apps Manager tab. You should see the app name you created earlier as a line item with authorization <br>
as pending. Select the options for the app and select ‘Authorize App’. Click 'Authorize' to approve the app.


![Authorize App](https://koremarcelblog.blob.core.windows.net/box-blog/i-authorize-app.png)

Once your app has been authorized either through the steps above or by an admin from your organization, navigate back to the developer console. <br>
Select your app name/icon to enter the configuration page. Under general settings, your app should now have a service account id under the ‘Service <br>
Account Info .’This is the ID that you will use moving forward to run your automation task. This follows the typical use of service accounts for deployments instead of your own.


![Service Account Info](https://koremarcelblog.blob.core.windows.net/box-blog/j-service-account.png)

Navigate to the configuration tab. You will see a couple of options for managing authentication methods and app permissions. For testing and development,<br>
you can use the developer token, which is only valid for 60 minutes, after which you have to generate a new token. This is not a solution to use for <br>
production and automated tasks. You require credentials that will persist during each automation run.

![Developer Tokens](https://koremarcelblog.blob.core.windows.net/box-blog/k-developer-token.png)

We will be using OAuth 2.0 with JWT server authentication for this post. For more information, follow the link below on the BOX portal.

![OAuth 2 Documentation](https://koremarcelblog.blob.core.windows.net/box-blog/l-jwt-auth-png)

For the JWT authentication to work, there are two steps that you need to follow. The first step is to generate a public/private Keypair. The screenshot <br>
below shows the section in the developer console under configuration where you need to do this. Click on ‘Generate a Public/Private Keypair’, and a JSON <br>
file will be generated, and you will be prompted to download the file based on your browser settings.


![Generate a Public/Private Keypair](https://koremarcelblog.blob.core.windows.net/box-blog/n-public-private-key.png)


This JSON will have the credentials required to connect to your BOX app, so do not lose or delete it otherwise you will have to generate a new one.

Under application scope in the configuration tab, select ‘Write all files and folders stored in Box’ check box to allow our service account to <br>
create/read/delete files in BOX. Make sure to save the changes afterward.


![Configuration Settings](https://koremarcelblog.blob.core.windows.net/box-blog/m-app-scope.png)


The remaining settings can be left to their default values unless you have specific requirements.Next, we will navigate back to your BOX account <br>
and provide your service account access to your folder of choice. This will be the folder we will interact with in the next part of this blog post.<br>
Select the folder of your choice and navigate to manage collaborators.Under the collaborator’s section, click on the ‘Share’ button and add the service <br>
account email from the previous section. <br>

![Provide Service Account Access to Folders](https://koremarcelblog.blob.core.windows.net/box-blog/o-share-permissions.png)

This email can be found in the developer’s console under ‘Service Account Info’. Next, confirm that your service account is a collaborator with Editor <br>
access, as shown below.


![Collaborators Pane - Confirm Access](https://koremarcelblog.blob.core.windows.net/box-blog/p-collaborators.png)

At this point, we should be ready to start interacting with BOX using our custom app/service account. We will see how to do this in the next post.