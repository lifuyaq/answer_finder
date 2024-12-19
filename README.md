# online_test_helper

online test helper is a simple python app that can help 
you to search the answers in your database(xlsx) by screen shots.

## Installation
```
git clone https://github.com/lifuyaq/online_test_helper.git
```

After install python virtual environment, perform the following command to
install dependency packages:

```
pip install -r requirements.txt
```

## Requirements
You need python 3.11 or higher.  
Excel files should be located in folder ../answers, and the first 
sheet will not be used.In other sheets, the first column should be 
the question and the second columns should be the answers. 


## Problems and solution
For some new python users on mac, please use this code to allow 
easyocr download models.

```
/Applications/Python\ 3.12/Install\ Certificates.command
```


