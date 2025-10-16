# **Scaffolding Guide: From Zero to Ready-to-Code**

Welcome. This guide will walk you through every setup step required to build our DOJ scraper project. We will not skip anything. Follow these instructions precisely, and you will have a perfect, working environment ready for our class.

The goal is to eliminate all the frustrating little setup problems that tutorials often ignore.

### **Our Goal: A Mental Model**

Before we begin, let's understand the three main pieces we are setting up. This will help you see how everything fits together.

1. **The Editor (VS Code)**: A specialized text editor where we will *write* our code. Think of it as Microsoft Word for programmers.  
2. **The Interpreter (Python)**: The actual program that *understands and runs* our Python code. VS Code is the workshop; Python is the engine.  
3. **The Sandbox (Virtual Environment)**: An isolated folder for our project's tools (called libraries or dependencies). This keeps our project clean and prevents conflicts with other Python projects you might build later.

With this model in mind, let's begin.

### **Phase 0: The Pre-Flight Checklist**

Before you download anything, ensure you have the following.

1. **A Personal Computer (Windows or Mac)**: You must have administrator permissions to install software.  
2. **An Email Address**: To sign up for an OpenAI account.  
3. **A Mobile Phone**: Required for account verification with OpenAI.  
4. **A Credit Card**: To put on file with OpenAI. **You will not be charged for this class.** Adding a card is standard practice to activate developer access. OpenAI provides free starting credits that will easily cover our entire project.

### **Phase 1: Install Your Code Editor (Visual Studio Code)**

1. **Download the Installer**:  
   * Go to the official website: [https://code.visualstudio.com/](https://code.visualstudio.com/)  
   * The site will automatically detect your operating system. Click the prominent "Download" button.  
2. **Run the Installer**:  
   * **On Windows**: Open the downloaded .exe file. Accept the license agreement. On the "Select Additional Tasks" screen, make sure **all boxes are checked**, especially **"Add to PATH"**. This is critical. Click through the rest of the installation with the default options.  
   * **On Mac**: Open the downloaded .zip file. This will extract the Visual Studio Code.app. Drag this application into your Applications folder.  
3. **Launch VS Code**: Open the application. You should see a welcome screen.  
4. **(Recommended for Mac Users)** **Add the 'code' Command**:  
   * Open VS Code, press Cmd+Shift+P, type Shell Command: Install 'code' command in PATH, and press Enter. This lets you open projects directly from your terminal.

### **Phase 2: Install Python**

Now we'll install the Python interpreter and teach VS Code how to use it.

1. **Install the Python Extension**:  
   * In VS Code's left-hand toolbar, click the Extensions icon (four squares).  
   * In the search bar, type Python and find the one published by **Microsoft**. Click "Install".  
2. **Install the Python Interpreter**: The extension adds Python *awareness* to VS Code, but we still need to install the Python *engine* itself.  
   * In VS Code, open the Command Palette (Ctrl+Shift+P on Windows, Cmd+Shift+P on Mac).  
   * Type Python: Select Interpreter and click the option.  
   * At the top of the list that appears, choose the option to **"Install Python..."**.  
   * Follow the on-screen instructions. *Note: On Windows, this may open the Microsoft Store. If you encounter any issues, a more reliable method is to download the official installer directly from [python.org/downloads](https://python.org/downloads).*  
3. **Verification Step (Critical)**: Let's confirm Python is installed correctly.  
   * Close and reopen VS Code.  
   * Open a new terminal (Terminal \> New Terminal).  
   * Type the following command and press Enter:  
     python \--version

     * *(If you get a "command not found" error, try python3 \--version)*.  
   * You should see a version number like Python 3.x.x. If you see an error, the installation was not successful or "Add to PATH" was not checked.

### **Phase 3: Get Your AI Access Key (OpenAI API)**

This key is the password that allows our code to talk to the AI model.

1. **Sign Up for a Developer Account**:  
   * Go to: [https://platform.openai.com/](https://platform.openai.com/)  
   * Click **"Sign up"** (do not click "Try ChatGPT"). Complete the process.  
2. **Set Up Billing**:  
   * Once logged in, navigate to the "Billing" section and add your payment method to activate your account.  
3. **Create Your Secret API Key**:  
   * Navigate to the "API keys" section.  
   * Click the button **"+ Create new secret key"**. Name it doj-class-project.  
   * A pop-up will show your key (it starts with sk-...). **THIS IS THE ONLY TIME YOU WILL SEE THIS KEY.**  
   * Click the copy icon and **immediately paste it into a temporary, safe place** (like a blank Notepad or TextEdit file).

### **Phase 4: Create and Prepare Your Project Workspace**

1. **Create a Project Folder**:  
   * On your Desktop, create a new folder named doj-scraper. *Note: Folder and file names are often case-sensitive. Use this exact name.*  
2. **Open the Folder and Terminal in VS Code**:  
   * In VS Code, go to File \> Open Folder... and select doj-scraper.  
   * Open a new terminal (Terminal \> New Terminal).  
3. **Verify Your Terminal Path**: Your terminal must be "inside" your project folder.  
   * Type one of the following commands and press Enter:  
     * **On Mac**: pwd  
     * **On Windows**: cd  
   * The output should be a path that **ends with doj-scraper**. If it doesn't, you need to navigate to it before proceeding.  
4. **Create the Sandbox (Virtual Environment)**:  
   * In the terminal, run this command:  
     python \-m venv venv

     * *(Use python3 if that's what you used in the verification step).*  
   * A new folder named venv will appear in your project.  
5. **Activate the Sandbox**:  
   * **On Windows**:  
     .\\venv\\Scripts\\activate

   * **On Mac**:  
     source venv/bin/activate

   * **Success\!** You will know it worked because your terminal prompt will now start with (venv).

**Important**: Every time you close and reopen this project in VS Code, you must re-run this activation command in the terminal. If you don't see (venv), your code won't find its tools.

6. **Install the Project's Tools**:  
   * In the active terminal (with (venv) showing), run this command:  
     pip install openai requests beautifulsoup4

7. **Final Confidence Check**: Let's run a quick test to ensure all libraries were installed correctly in our sandbox.  
   * Create a new file in VS Code named test\_install.py.  
   * Paste this one line of code into it:  
     import openai, requests, bs4; print("All libraries loaded successfully\!")

   * Save the file.  
   * In your terminal (with (venv) showing), run the file by typing:  
     python test\_install.py

   * You should see the success message. If you do, you can delete this test file.  
8. **Create Your Main Code File**:  
   * In the VS Code file explorer, create one last file named scraper.py.  
   * The file will open, blank and ready for our class.

### **Final Sanity Checklist**

You are 100% ready to begin coding. Use this table to verify your setup is perfect.

| Step | Command to Run (in VS Code Terminal) | Expected Output |
| :---- | :---- | :---- |
| **Verify Python** | python \--version | A version number, e.g., Python 3.11.5 |
| **Activate Environment** | source venv/bin/activate (Mac/Linux) or .\\venv\\Scripts\\activate (Win) | Terminal prompt now starts with (venv) |
| **Check Installed Tools** | pip list | A list that includes openai, requests, and beautifulsoup4 |
| **Ready for Coding** | (Visual Check) | scraper.py file is open and blank |

### **Appendix: Common Troubleshooting**

* **Error: "command not found: python" or "'python' is not recognized..."**  
  * **Fix**: Try using python3 instead of python in all commands. If that also fails, you missed checking "Add to PATH" during installation. Re-install Python and ensure that box is checked.  
* **Error: "Cannot activate venv" or "permission denied" on Mac/Linux**  
  * **Fix**: Make sure your command starts with source. It is source venv/bin/activate, not just venv/bin/activate.  
* **Problem: My code can't import openai. It says "ModuleNotFoundError".**  
  * **Fix**: You forgot to activate your virtual environment. Your terminal prompt must start with (venv). Close the terminal, open a new one, and run the activation command from Step 4.5.  
* **If all else fails (The Escape Hatch)**: If you get completely stuck with the local setup, don't worry. You can still participate using a cloud environment like [Google Colab](https://colab.research.google.com/). You will only need to run \!pip install openai requests beautifulsoup4 in a cell at the top of your notebook.