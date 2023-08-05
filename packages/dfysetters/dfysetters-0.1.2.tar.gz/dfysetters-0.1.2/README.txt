<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

We are sending 1000's of messages weekly and it is crucial that we pull certain data from this so that we can iterate and improve. We will also be using this data for ML based projects once I can figure out how to do this in a way that benefits the company. If we can analyse our messages and improve our process from the insights gathered, it will allow us to work towards removing setters altogether

Here's why:
* Within the next decade, machines are going to replace customer service chat reps almost certainly, we need to be ahead of that trend
* Machines are far more reliable than humans and at scale, we do not have to hire 100s of people to send messages
* We can collect far more data using software than we could with manual tracking

This is a start, and we will add new functionality as we start

### Built With

* [python](https://www.python.org)
* [pandas](https://pandas.pydata.org)
* [vscode](https://code.visualstudio.com)


<!-- GETTING STARTED -->
## Getting Started

We need to make sure we have python and virtualenv installed so that we can download the packages. Follow the below packages then move to installation

1. ```brew install python3 ```

2. ```brew install virtualenv ```

### Prerequisites

You will need the following accounts setup
1. settersandspecialists.com gmail account
2. Downloaded FB Messages file from drive
2. python, pandas (Follow the Getting Started Steps)

### Installation

See below for the steps to follow to set the code up on your computer

1. ```gh repo clone louisrae/team_scripts```
2. ```cd team_scripts/dfysetters```
3. ```virtualenv venv```
4. ```. venv/bin/activate```
5. ```pip3 install -r requirements.txt```
6. ```cd team_scripts/dfysetters```
7. ```python3 messaging_data.py```


<!-- USAGE EXAMPLES -->
## Usage

This is a fairly simple script to run. It takes in 1 main parameter, then iterates over it, requiring new parameters every time. Firstly you need to provide a URL to the sheet you want to analyse. This will need to be in the standard dfysetters format. Then you will need to enter the name of the specialist on the sheet. The terminal will give you the name of the sheet, and make sure you type the name exactly e.g Morgan Abendroth-Daysh with capitals and hyphens including.

The end result is 2 csv files named account_data and message_tracking with the appropriate data inside.

<!-- ROADMAP -->
## Roadmap

- [] Append to sheets automatically
- [] Pull specialist name automatically 
- [] Allow team to use it, not just me


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- CONTACT -->
## Contact

Your Name - [Louis-Rae](louisrae@settersandspecialists.com)


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Will do this more in future
