# Email Sender

This project is an easy way in order to simplify the daunting task of sending numerous emails to professors.

- Frustrated of copying and pasting over and over again with the very good chance of making a typo or mispelling a word in your emails?
- Throwing your precious chances away because the name of the professor didn't match the email content?
- Forgot to thoroughly replace information in your email template?
  <br><br>

This project got your back! Just prepare your and professors data, write down your desired template and you can both <b>send email</b> & <b>export email body</b> using this project!
<br><br>

<center><span style="color:cyan">Made with <3 by Homayoon Alimohammadi</span></center>
<br><br><br>

# Tutorial

- <span style="color:yellow">WARNING</span>: All the commands starting with `make` should be executed where the `Makefile` is available
- In order to use the `python version`, you need to install `python >= 3.10`. [Installation instructions](https://www.python.org/downloads/)
- In order to use the `go version`, you need to install `golang >= 1.17`. [Installation instructions](https://go.dev/doc/install)
- In order to use the command `make` for the `Makefile`, you need to have `make` installed:
  - [Windows](https://stackoverflow.com/questions/2532234/how-to-run-a-makefile-in-windows)
  - [Linux](https://linuxhint.com/install-make-ubuntu/)

## Create Mandatory Files:

- In the project's `root directory` (where the `Makefile` exists) create three files <b>`my_data.json`</b>, <b>`professors.xlsx`</b> and <b>`.env`</b>
  in the <b>`my_data.json`</b>, just like the my_data_fake.json put all your specific data
- <b>`professors.xlsx`</b> should contain all the data of each professor, just like a typical excel file.
- <span style="color:yellow">WARNING</span>: put <b>`app password`</b> of your Gmail in the <b>`password`</b> field in the json file.
- <span style="color:yellow">WARNING</span>: FILL ALL THE FIELDS IN BOTH FILES COMPLETELY OR YOU MIGHT ENCOUNTER SEVERAL ERRORS
- In the <b>`.env`</b> file write down your project's specific configuration
- <span style="color:yellow">WARNING</span>: watch out for typos or mispelling in your path and config, this .env file is very sensetive
- Put your resume with the <span style="color:red">EXACT</span> name of <b>`Resume.pdf`</b> in the root directory (where the `Makefile` exists)
- The template for your email body is stored in the <b>`email_content.txt`</b> in the root of the project. If you want a more customized template, feel free to edit this file. Keywords between curly braces (i.e. {}) like `{my_first_name}` are to be replaced with the data you provide.

- <span style="color:yellow">WARNING</span>: Remember to put all of the keywords between the curly braces (i.e. {}) untouched or you might encounter errors while rendering your template.

## Run

### 1. Python Version

- In the root of the project, run:

```shell
make py
```

- if <b>`SEND_EMAIL`</b> is set to `1` in the `.env` config file, all the professors mentioned in the `professors.xlsx` file will get your email
- if <b>`EXPORT_CONTENT`</b> is set to `1` in the `.env` config file, all the email contents will be exported in `./python/exported/` directory which . refers to the root of the project

### 2. Golang version

- In the root of the project, run:

```shell
make go
```

- if <b>`SEND_EMAIL`</b> is set to `1` in the `.env` config file, all the professors mentioned in the `professors.xlsx` file will get your email
- if <b>`EXPORT_CONTENT`</b> is set to `1` in the `.env` config file, all the email contents will be exported in `./go/exported/` directory which . refers to the root of the project

### 3. Build Golang Binary in Linux or macOS

- In order to build golang binary for easy use and transportation, run:

```shell
make gobuild
```

- There will be a <b>`EmailSender`</b> binary file in the `./go/` directory,

### 4. Build Golang Executable in Windows

- In order to build golang executable for easy use and transportation, run:

```shell
make gobuild_win
```

- There will be a <b>`EmailSender.exe`</b> executable file in the `./go/` directory,

## Cleanup

- In case you want to cleanup the `exported/` directory and all of the `binary` and `executable` files, in the root of the project run:

```shell
make clean
```

<br><br>

# Enjoy!
