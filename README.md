# Project Name

## Prerequisites

1. **Google Cloud Console Setup:**

   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the **Google Drive API**:
     - In the left sidebar, go to **APIs & Services** > **Library**.
     - Search for "Google Drive API" and enable it for your project.
   - **Create OAuth 2.0 Credentials**:
     - Go to **APIs & Services** > **Credentials**.
     - Click on **Create Credentials** and select **OAuth 2.0 Client IDs**.
     - Select **Desktop application** or **Other** (depending on your use case).
     - After creation, download the `credentials.json` file.
     - **IMPORTANT**: Make sure to store the `credentials.json` file in a secure location, and do **not** upload it to GitHub.

2. **Install Required Libraries:**

   - Install the necessary libraries in your local environment:
   ```bash
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

3. **Run the script**
