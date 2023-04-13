# Reto Backend - Fast API
![image](https://user-images.githubusercontent.com/80084307/231678122-809c741c-adeb-4eaa-8872-ebd3e2c1e48e.png)
<br>

# 📦 Installation
* ## Create and activate your venv
    ``` Python
    python -m venv .venv
    ```
    * ### **Windows**
        ``` Python
        .venv/Scripts/activate
        ```
    * ### **Linux**
        ``` Python
        source .venv/bin/activate
        ```

<br>

* ## Install requirements
    ``` Python
    pip install -r requirements.txt
    ```

<br><br>

# 🔧 Configuration
* ## You need to have [🐋Docker](https://www.docker.com/) and run this command
```
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

<br><br>

# ⚡ Run API
``` Python
uvicorn api.main:app --reload
```

<br><br>

# ✔️ Run Tests
``` Python
pytest
```




