# Resume Contact Information parser

Extracts contact information from one or more uploaded resume with support for multiple file format. The server works on a database which allows us to query the application for later use.


## Installation
Make sure you have installed libreoffice-7.1 before proceeding further, and that it is in path

Then

```bash
git clone https://github.com/dgargdipin/resume_parser
cd resume_parser
python3 -m venv env
pip install -r requirments.txt
```

​                                                         

Upon installation server can be run by 

`python3 app.py`

# Endpoints

**Upload Resume(s)**
----


* **URL**

  /upload/

* **Method:**
  
  `POST` 

*  **URL Params**

   None

   **Data Params**

   The request should the resume files as body attachments with key `files`

* **Success Response:**
  
  Request with success response includes id, mobile numbers and emails in an array in json format.	

  * **Code:** 200 <br />
    **Content:** 
    
    ```json
    [
        {
            "email": [
                "****@gmail.com"
            ],
            "id": "bfba77cc-2a97-4c2b-bf8e-08df5563fbd8",
            "mobile": [
                "**********",
                "**********"
            ]
        },
        {
            "email": [
                "******@gmail.com"
            ],
            "id": "61dd0b67-d3fa-4db0-a688-71c83430ae26",
            "mobile": [
                "*********"
            ]
        }
    ]
    ```
    
    
  
* **Error Response:**

  Wrong input attachment can lead to error responses

  * **Code:** 404<br />
  * If no file attachments

  

* **Sample Call:**

  ```bash
  curl --location --request POST 'http://127.0.0.1:5001/upload/' \
  --form 'files=@"file1.docx"' \
  --form 'files=@"file2.docx"' \
  --form 'files=@"file3.pdf"'
  ```

  

**Get information with a particular id**
----

Returns the contact information of a cv with a particular id

* **URL**

  /getinfo

* **Method:**
  
  `GET` 

*  **URL Params**

   **Required:**

   `id=[string]`

* **Success Response:**

  A successful request should return the contact information of a resume with the requested id, if it exists

  * **Code:** 200 <br />
    **Content:** 
    
    ```json
    {
        "email": [
            "****@gmail.com"
        ],
        "id": "2b49510b-7ca5-400d-9eb7-55c87f916bd9",
        "mobile": [
            "*********"
        ]
    }
    ```
    
    

* **Error Response:**

  * **Code:** 404<br />

* **Sample Call:**

  ```bash
  curl --location --request GET 'http://127.0.0.1:5001/getinfo?id=2b49510b-7ca5-400d-9eb7-55c87f916bd9' \
  --form 'id="7d9bc046-a453-446e-9f8f-88ef9eb91afb"'
  ```

**Get all resume contact information in a csv**
----

Returns all the contact information of uploaded resume in a csv file.

* **URL**

  /getAllExcel

* **Method:**
  
  `GET`

*  **URL Params**

   **Required:**

   None

   **Optional:**

   None

* **Data Params**

  None

  **Success Response:**

  * **Code:** 200 <br />
    **Content:** `allResumes.csv`

* **Error Response:**

  * **Code:** 500 SERVER ERROR<br />

* **Sample Call:**

  ```bash
  curl --location --request GET 'http://127.0.0.1:5001/getAllExcel'
  ```