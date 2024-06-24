<h1 align="center">
  <br>
  <a href="https://github.com/siddhant385/karavas"><img src="/data/images/logo.png?raw=true" alt="Logo" height="360" width="360"></a>
  <br>
  KARAVAS
  <br>
</h1>

<h4 align="center">An evil RAT (Remote Administration Tool) for Windows Built over Flask.</h4>

<p align="center">
  <a href="https://github.com/siddhant385/karavas/blob/main/LICENSE">
      <img src="https://img.shields.io/badge/license-GPLv3-blue.svg?style=flat-square" alt="License">
  </a>
  <a href="https://github.com/siddhant385/karavas/blob/main/LICENSE">
      <img src="https://img.shields.io/badge/python-3.10,%203.11-blue.svg?style=flat-square" alt="Python">
  </a>
  <a href="https://github.com/siddhant385/karavas/issues">
    <img src="https://img.shields.io/github/issues/siddhant385/karavas.svg?style=flat-square" alt="Issues">
  </a>
  <a href="https://github.com/siddhant385/karavas/blob/main/CONTRIBUTING.md">
      <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat-square" alt="Contributing">
  </a>
</p>
<h4 align="center"><strong>Currently this project is in BETA mode (Heavy development) So mosquitos and bugs are allowed and solutions to eradicate them are also requested</strong></h4>
Karavas is a Remote Administration Tool which is created for a simple yet powerful remote administration.
It was created as a hosting site which can be easily deployed to any python flask hosting service as command and control


## Table of Contents
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#demo)
- [Features](#features)
- [Future](#future)
- [Contributing](#this-is-a-piece-of-shit-contributing)
- [License](#license)
- [Contact](#contact)
- [Credits](#credits)
- [Disclaimer](#disclaimer-)
- [Supporters](#️supporters️)
## Getting Started
There are already many tools on github so Why have I created this one There are following reasons for that

- First I wanted to create this project for learning python and OOPs(Object Oriented Programming)
- I loved the tool EvilOsX and wanted an implementation of it in windows although like mac Windows doesn't come inbuilt with python.
- I liked the concept of **Run Once in client and forget** in EvilOsX, like only you have to run a client and forget about the modules they will load from server and you can update module from server
- Many Great RAT tools doesn't come with **Port Forwarding** we have to either use ngrok or something else to port forward, but if you run this tool from hosting site no porforwarding is needed.
- One more thing This tool only needs a webbrower to run if you host it fromm a hosting site and no space is utilised in your device


### Prerequisites

Ensure you have the following installed on your local machine:
- Python (version 3.7 or higher)

### Installation
- Installation consists of Two Parts First if you want to host to Server(No Port Forwarding Required)
  Below is the implementation:
  1. Clone the repository to any hosting service like [PythonAnywhere](https://www.pythonanywhere.com) or [Vercel](https://vercel.com)

  2. Do the essential steps required to host it to the respective sites as every site has different procedures for hosting

  3. Hurray you're good to go

  4. Note - One click deploy will come soon so Stay Updated or fork this site

- Build Locally in your PC (Port Forwarding Required)

  1. Clone the repository:
    ```sh
    git clone https://github.com/siddhant385/karavas.git
    ```
  2. Navigate to the project directory:
      ```sh
      cd karavas
      ```
      
  3. Install the required Python packages:
      ```sh
      pip install -r requirements.txt
      ```
    

### Usage
- Once the installation is complete, you can run the application with the following command:
    ```sh
    python main.py
    ```
    <br>
    After head to [localhsot:5000](http://localhost:5000)
- The default credentials are 
  <strong>Username:admin</strong>
  <strong>Password:2006</strong>

### Demo

- A demo site is live [Click Me](https://jokesapartismyname.pythonanywhere.com/) to see
- Note builder has been disabled for security and abuse purposes
- It's only a demo so you won't be able to execute commands
- Use the same credentials given above

### Features
- Reverse Shell
- No Port Fowrding Required
- Persistent

### Future
Future of this project depends on you So if You like please star and support me
Although in Future I will enchance this tool with following features and in order:
- Run in windows using exe instead to python to end python dependency in windows (will use pyinstaller)
- Create **different and encrypted payload** for different pc as EvilOsx
- Create **external library independent** modules for windows

### This is a Piece of Shit!!! (Contributing)
Ya I know that this is not complete or it has bugs but it's up to you to download and use it or contribute to it to make it more powerful.
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.
To Contribute follow the below steps
1. Fork the Project
2. Create your Feature Branch ``` git checkout -b feature/AmazingFeature```
3. Commit your Changes ``` git commit -m 'Add some AmazingFeature' ```
4. Push to the Branch ``` git push origin feature/AmazingFeature```
5. Open a Pull Request

### License

Distributed under the GPLv3 License. See LICENSE for more information.

### Contact

Siddhant - ssiddhant385@gmail.com

Project Link: https://github.com/siddhant385/karavas


### Credits and Mentions
- This Tool Uses a Gorgeous API Named [The Null Pointer](https://0x0.st/)
- This Tool also Uses a javascript library [Ansi Up](https://github.com/drudru/ansi_up) for colored terminal in output
- The Special Thanks goes to [Marten4n6](https://github.com/Marten4n6/) for his [EvilOsX](https://github.com/Marten4n6/EvilOSX) This project is a fork of it.


### Disclaimer :
Usage of this tool for attacking targets without prior mutual consent is illegal. It's the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.


### ❤️Supporters❤️
[![Stargazers repo roster for @siddhant385/karavas](https://reporoster.com/stars/siddhant385/karavas)](https://github.com/siddhant385/karavas/stargazers)