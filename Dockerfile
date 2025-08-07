# Set up R environment and install emulandice library from locked environment.
FROM rocker/tidyverse:4.1.2

COPY renv.lock renv.lock
RUN R -e "install.packages('renv', version='1.1.5')"
RUN R -e "renv::restore()"

## To create a locked environment.
# RUN R -e "install.packages('renv', version='1.1.5')"
# RUN R -e "renv::init(bare=TRUE)"
# RUN R -e "renv::install('tamsinedwards/emulandice@e3245fa')"
# RUN R -e "renv::snapshot(type='all')"

# Setup environment and install our python app to drive things.
COPY --from=ghcr.io/astral-sh/uv:0.8.5 /uv /uvx /bin/

# Where we're installing this thing.
ARG APP_HOME="/opt/emulandice"

# Use custom user/group so container not run with root permissions.
USER 9876:9876

WORKDIR ${APP_HOME}
COPY . .

# Set HOME so uv installs python here, here it has permissions. Because we're starting from an R base image.
ENV HOME=${APP_HOME}
# Install the application dependencies into a local virtual environment, compiling to bytecode.
RUN uv sync --frozen --no-cache --no-dev --compile-bytecode

# Easily run commands from the environment just created.
ENV PATH="${APP_HOME}/.venv/bin:$PATH"

ENTRYPOINT ["emulandice"]

