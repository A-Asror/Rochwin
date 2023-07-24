FROM python:3.10.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apt-get update -y \
    && apt-get install -y libffi-dev gcc python3-dev musl-dev g++ postgresql vim
#    postgresql nano
#    && apk add binutils python-gdal \ zlib-dev py-pip
#    && apk add postgresql-dev
#    && gdal-bin binutils libproj-dev libgdal-dev
#    && libgdal-dev binutils libproj-dev python3-gdal gdal-bin
# musl-dev jpeg-dev apk add libressl-dev perl rust libmagic pango openjpeg-dev


# Upgrade pip
RUN pip install --upgrade pip

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/backend
ENV LOCAL_APP=././././
RUN mkdir $HOME
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/logs
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media

# set work directory
WORKDIR $APP_HOME

# Install dependencies
COPY ./requirements $APP_HOME/requirements
RUN pip install -r requirements/dev.txt

# copy project
COPY $LOCAL_APP $APP_HOME

# run entrypoint.prod.sh
RUN ["chmod", "+x", "/home/app/backend/.docker/dev/backend/entrypoint.sh"]
ENTRYPOINT ["/home/app/backend/.docker/dev/backend/entrypoint.sh"]

# chown all the files to the www-data user
RUN chown -R www-data:www-data $APP_HOME
