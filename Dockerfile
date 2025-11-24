FROM python:3.14-trixie

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# add poetry to PATH
ENV PATH="/root/.local/bin:${PATH}"

# define workspace
WORKDIR /app

# copy dependency files
COPY poetry.lock .
COPY pyproject.toml .

# install dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# copy app code
COPY . .

# run the app
CMD ["poetry","run","gunicorn","w", "4", "main:app"]
