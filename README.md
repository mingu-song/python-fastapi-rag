* 1부 File Upload
  * https://medium.com/thoughts-on-machine-learning/building-a-simple-rag-system-with-fastapi-1-382e15a6ae2a
* 2부 Parser Factory
  * https://medium.com/thoughts-on-machine-learning/building-a-simple-rag-system-with-fastapi-2-18a001df7e65
* 3부 PostgeSQL
  * https://medium.com/thoughts-on-machine-learning/building-a-simple-rag-system-with-fastapi-3-ecb3926f2486
  * ```shell 
    # python version <= 3.9
    pip install sqlalchemy psycopg2 sqlalchemy-utils
    
    # if error on m1 macbook
    pip install sqlalchemy psycopg2-binary sqlalchemy-utils
    
    # and then
    pip install pgvector
    ```
* 4부 Background Embedding
  * https://medium.com/thoughts-on-machine-learning/building-a-simple-rag-system-with-fastapi-4-424a044bf322
  * ```shell 
    # nltk OpenAI
    pip install nltk OpenAI
    ```
* Origin Github
  * https://github.com/fsndzomga/rag-fastapi
* 기타
  * PostgreSQL + Vector
    * ```dockerfile 
      # docker-compose.yml
      version: "3.5"
    
      services:
        postgres-vector:
          container_name: postgres-vector
          image: ankane/pgvector
          ports:
            - 6432:5432
          environment:
            - POSTGRES_USER=root
            - POSTGRES_PASSWORD=root
      ```
  * OPENAI_API_KEY
    * https://platform.openai.com/docs/overview
### 의견
* 심플하게 테스트할 수 있지만 OpenAPI 무료 key의 사용량 제한이 있어 먼갈 해보긴 어렵네 ㅎ
