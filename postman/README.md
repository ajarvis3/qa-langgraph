Postman collection for qa-langgraph

Files:
- qa-langgraph-postman-collection.json  - Postman collection (v2.1)
- qa-langgraph-postman-environment.json - Postman environment with {{base_url}}

How to use:
1. Start the Flask app (defaults to http://localhost:5000):

```cmd
python app.py
```

2. Import the collection into Postman: File -> Import -> Choose File -> select `postman/qa-langgraph-postman-collection.json`.

3. (Optional) Import the environment: Environments -> Import -> select `postman/qa-langgraph-postman-environment.json`.

4. Select the `qa-langgraph-local` environment (if imported) and open the "Run Agent" request.

5. In the Body -> form-data set `query` (text) and choose a local file for `file` (type: file). Click Send.

Curl example:

```cmd
curl -X POST "http://localhost:5000/run" -F "query=How do I reverse a list in Python?" -F "file=@agent_definition.txt"
```

Notes:
- The collection includes a second request demonstrating a missing file error (expected HTTP 400).
- Adjust `{{base_url}}` in the environment if your Flask app runs on a different host or port.

