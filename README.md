# ChatProgram
A chat program using Python, PyQt5 and socket programming.

## Required Libraries
- OpenSSL (used for SSL)
- SSL (should be included when installing Python 3.8)
- PyQt5


## Instructions For Install And Run
1. Use a device with Windows operating system. The GUI is based on the Windows operating systems and have been using the Windows operating system to program this.
2. Download and install miniconda from https://docs.conda.io/en/latest/miniconda.html and select the Python 3.8 Windows version.
3. Open up the Anaconda prompt and copy this command `conda create –n py38 python=3.8` and paste it in the prompt. Press and enter y when prompted.
4. Once environment has been created write this command `conda activate py38` on the prompt to activate the py38 environment. Your environment will change from (base) to (py38)
5. Install OpenSSL library by going on to this website https://slproweb.com/products/Win32OpenSSL.html and install Win64 OpenSSL v3.0.5 .exe file. Follow the steps in this tutorial: https://tecadmin.net/install-openssl-on-windows/
6. Install PyQt5 library by writing `pip install PyQt5` on command line. Press and enter y if prompted to.
7. Download and install Visual Studio Code from https://code.visualstudio.com/download and open Visual Studio Code when finished downloading.
8. On Visual Studio Code, install the Python package in the extension market place (the last button on the left-most vertical side bar)
9. Download or clone this project from Github
10. Open the folder `ChatProgram` on Visual Studio Code
11. On Visual Studio Code, do `Ctrl+Shift+P` and set Python Interpreter on Visual Studio Code to Python 3.8.13 ('py38')
12. Go to `ChatProgram/backEnd/server.py` to run the code for the server. Type `python chat_main.py` in a new terminal on Visual Studio Code to run the GUI. If you want multiple client GUIs, open new terminals on Visual Studio Code and type `python chat_main.py` for every number of clients you want to be in the server. The maximum number of clients is 5.

## How To Use
### Joining The Chat Server As A Client (Connect To Chat Window)
- To connect to the chat rooms, type `localhost` in the IP address field, `9988` in the Port number field and a nickname that you want to use. Press the `Connect` button once you have done that. This will take you to the `Chat Connected` window and create a client socket.
- To exit the application press the 'Exit'.
- When any new clients join the server, their nickname will be shown in the `Connect Clients` large (uneditable) textbox in the `Chat Connected` window

 ### Chat Connected Window
 - To exit, press the `Exit` button. This will close the client socket.
 -  To chat one on one with another client, click on their name and then press the `1:1 Chat` button  in the `Chat Connected` window. This will take you to the `One To One Chat` window with the client you selected.
 - To create a group chat, press the `Create Group` button in the `Chat Connected` window. This will show up in the `Group Chats` large (uneditable) textbox which can be seen by all clients connected to the server. You can create multiple group chats and all clients can join the group chat (if they choose to, see next bullet point)
- To join a group chat, click on the group name and press the `Join Group` button in the `Chat Connected` window. This will take you to the `Group Chat` window with the group you selected.
  -  If you are new to the group, there may be a small delay when loading the `Group Chat` window. This is to ensure the server knows you are a new member to the group chat.

### One To One Chat Window
- To send a message, type in the small text box next to the `Send` button. Once you have written your message, press the `Send` button to send the message.
- To send an image, press the `Send Image` button. This will open up a file selector dialog which will allow you to select and upload image file to send to the chat from any of your folders. Pressing the `Open` button on this dialog will send the image to the chat.  The image will be viewed as a 200x200 pixel thumbnail image in the chat. Pressing `Cancel` will cancel this process and no image will be sent. You can choose images that have the format `JPEG (*.jpg, *jpeg)` or `PNG (*.png)`.
  - **Note: image files will be downloaded in the `/ChatProgram/` directory when its being sent to the chat.**
  - **Currently there are no options to view the image in it's original resolution or to download the image to another folder.**
- To exit the one on one chat, press the `Exit` button.

### Group Chat Window
- Members of the group chat will be shown in the `Members` large (uneditable) textbox
- To send a message, type in the small text box next to the `Send` button. Once you have written your message, press the `Send` button to send the message.
- To send an image, press the `Send Image` button. This will open up a file selector dialog which will allow you to select and upload image file to send to the chat from any of your folders. Pressing the `Open` button on this dialog will send the image to the chat.  The image will be viewed as a 200x200 pixel thumbnail image in the chat. Pressing `Cancel` will cancel this process and no image will be sent. You can choose images that have the format `JPEG (*.jpg, *jpeg)` or `PNG (*.png)`.
  - **Note: image files will be downloaded in the `/ChatProgram/` directory when its being sent to the chat.**
  - **Currently there are no options to view the image in it's original resolution or to download the image to another folder.**
- To invite a client who is not a member of the group chat, press the `Invite` button. This will take you to the `Invite To Group Chat` window which will show you the list of clients that are in the server but not a member of the group chat.

#### Invite To Group Chat Window
-  To invite a client, click on their name and press the `Invite` button. You can only select one client at a time. the `Invite To Group Chat` window will not close until `Cancel` is pressed. 
    - The recipient will get a pop-up dialog asking if they want to join the group chat. If they press the `Yes` button, they will join the group chat and the `Members` list will update. If they press the `No` button, they will not be join the group chat. 
-  To exit the `Invite To Group Chat` window, press the `Cancel` button.
  

## User Interface Snippets
<img src="https://user-images.githubusercontent.com/79692362/195971490-b1d7e43e-133f-4e47-b866-0f126d228e29.png"  width="350" height="300"><img src="https://user-images.githubusercontent.com/79692362/195971498-19bbfdc7-51b0-4c77-a5a7-22ce0a64d471.png"  width="300" height="400">
<img src="https://user-images.githubusercontent.com/79692362/195971549-d04f5597-d919-4f46-8db8-0c158dde98de.png"  width="300" height="300"><img src="https://user-images.githubusercontent.com/79692362/195971660-160df49c-9454-485c-8617-b66f6495aa9b.png"  width="450" height="400">





