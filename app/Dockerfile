FROM python:3.7

COPY . /app

ARG USER_ID
ARG GROUP_ID
ARG username

RUN groupadd -g ${GROUP_ID} ${username} && \
    useradd -l -u ${USER_ID} -g ${username} ${username} && \
    install -d -m 0755 -o ${username} -g ${username} /home/${username} && \
    chown -R ${USER_ID}:${GROUP_ID} /usr/local 
    
RUN chown -R ${username} /app

WORKDIR /app

RUN pip install pipenv 

USER ${username} 

RUN pipenv install 

CMD [ "pipenv", "run", "flask", "run", "--host=0.0.0.0" ]
