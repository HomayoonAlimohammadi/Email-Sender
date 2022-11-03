# Send Customizable Emails to your desired recipients!

## How does it work:

### 1. Create mandatory files

- In the project's `root directory` (where the `run_python.sh` exists) create two files <b>`my_data.json`</b> and <b>`professors.xlsx`</b>
  in the <b>`my_data.json`</b>, just like the my_data_fake.json put all your specific data
- <b>`professors.xlsx`</b> should contain all the data of each professor, just like a typical excel file.
- <span style="color:yellow">WARNING</span>: put <b>`app password`</b> of your Gmail in the <b>`password`</b> field in the json file.
- <span style="color:yellow">WARNING</span>: FILL ALL THE FIELDS IN BOTH FILES COMPLETELY OR YOU MIGHT ENCOUNTER SEVERAL ERRORS
- In the `./python` directory (where this `README.md` exists) create a file named <b>`.env`</b> and write down your project's specific configuration
- <span style="color:yellow">WARNING</span>: watch out for typos or mispelling in your path and config, this .env file is very sensetive
- Put your resume with the <span style="color:red">EXACT</span> name of <b>`Resume.pdf`</b> in the root directory (where the `run_python.sh` exists)
- Head to the `python` folder (where this `README.md` exists) and install the dependencies as follows:

```shell
cd python
sudo apt install python3-pip python3-venv
$(which python3) pip install -r requirements.txt
source env/bin/activate
```

### 2. Run the Python Version

- In the root of the project, run:

```shell
chmod u+x run_python.sh
./run_python.sh
```

- if <b>`SEND_EMAIL`</b> is set to `1` in the `.env` config file, all the professors mentioned in the `professors.xlsx` file will get your email
- if <b>`EXPORT_CONTENT`</b> is set to `1` in the `.env` config file, all the email contents will be exported in `./python/exported/` directory which . refers to the root of the project

### 3. Enjoy!
