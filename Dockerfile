# 1. start from a machine that has Python 3.11
FROM python:3.11-slim

# 2. make and go into /app
WORKDIR /app

# 3. copy the pacakge list in
COPY requirements.txt .                                         

# 4. install packages
RUN pip install -r requirements.txt                                  

# 5. copy the rest of the code
COPY . .                                                            

# 6. start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]