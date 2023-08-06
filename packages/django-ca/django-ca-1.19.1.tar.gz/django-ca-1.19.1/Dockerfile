# syntax = docker/dockerfile:experimental
ARG IMAGE=python:3.10-alpine3.14

FROM $IMAGE as base
WORKDIR /usr/src/django-ca

RUN --mount=type=cache,target=/etc/apk/cache apk upgrade
RUN --mount=type=cache,target=/etc/apk/cache apk add --update \
        pcre openssl binutils busybox libpq postgresql-client mariadb-connector-c mariadb-client

# Add user (some tests check if it's impossible to write a file)
RUN addgroup -g 9000 -S django-ca && \
    adduser -S -u 9000 -G django-ca django-ca

FROM base as build
RUN --mount=type=cache,target=/etc/apk/cache apk add \
        build-base linux-headers libffi libffi-dev openssl-dev \
        pcre-dev mailcap mariadb-connector-c-dev postgresql-dev cargo
RUN --mount=type=cache,target=/root/.cache/pip/http pip install -U setuptools pip wheel

COPY ca/django_ca/__init__.py ca/django_ca/
COPY requirements.txt setup.cfg setup.py ./
COPY requirements/ requirements/
COPY --chown=django-ca:django-ca docs/source/intro.rst docs/source/intro.rst
RUN --mount=type=cache,target=/root/.cache/pip/http pip install --no-warn-script-location --prefix=/install \
    -r requirements.txt \
    -r requirements/requirements-docker.txt \
    -e .[redis,mysql,postgres]

# Finally, copy sources
COPY ca/ ca/

###############################
# Build sdist and wheel #
###############################
# Build artifacts are tested individually in later stages
FROM build as dist-base
COPY setup.py setup.cfg MANIFEST.in ./
RUN python setup.py sdist bdist_wheel
RUN rm -rf ca/ setup.py setup.cfg MANIFEST.in
COPY devscripts/test-imports.py ./

##############
# Test sdist #
##############
FROM dist-base as sdist-test
RUN --mount=type=cache,target=/root/.cache/pip/http pip install dist/django-ca*.tar.gz
ADD setup.cfg ./
RUN ./test-imports.py

############################
# Test wheels (and extras) #
############################
FROM dist-base as wheel-test
RUN --mount=type=cache,target=/root/.cache/pip/http pip install dist/django_ca*.whl
ADD setup.cfg ./
RUN ./test-imports.py

FROM dist-base as wheel-test-acme
RUN --mount=type=cache,target=/root/.cache/pip/http pip install $(ls dist/django_ca*.whl)[acme]
ADD setup.cfg ./
RUN ./test-imports.py --extra=acme

FROM dist-base as wheel-test-redis
RUN --mount=type=cache,target=/root/.cache/pip/http pip install $(ls dist/django_ca*.whl)[redis]
ADD setup.cfg ./
RUN ./test-imports.py --extra=redis

FROM dist-base as wheel-test-celery
RUN --mount=type=cache,target=/root/.cache/pip/http pip install $(ls dist/django_ca*.whl)[celery]
ADD setup.cfg ./
RUN ./test-imports.py --extra=celery

FROM dist-base as wheel-test-mysql
RUN --mount=type=cache,target=/root/.cache/pip/http pip install $(ls dist/django_ca*.whl)[mysql]
ADD setup.cfg ./
RUN ./test-imports.py --extra=mysql

FROM dist-base as wheel-test-postgres
RUN --mount=type=cache,target=/root/.cache/pip/http pip install $(ls dist/django_ca*.whl)[postgres]
ADD setup.cfg ./
RUN ./test-imports.py --extra=postgres

##############
# Test stage #
##############
FROM build as test
COPY --from=build /install /usr/local
ENV SKIP_SELENIUM_TESTS=y
ENV SQLITE_NAME=:memory:

# Install additional requirements for testing:
RUN --mount=type=cache,target=/root/.cache/pip/http pip install \
    -r requirements/requirements-docs.txt \
    -r requirements/requirements-dist.txt \
    -r requirements/requirements-test.txt \
    -r requirements/requirements-mypy.txt \
    -r requirements/requirements-lint.txt

# copy this late so that changes do not trigger a cache miss during build
COPY tox.ini pyproject.toml ./
COPY setup.py dev.py common.py recreate-fixtures.py ./
COPY --chown=django-ca:django-ca docs/ docs/
COPY --chown=django-ca:django-ca ca/ ca/

# Create some files/directories that we need later on
RUN touch .coverage
RUN mkdir -p /var/lib/django-ca/
RUN chown django-ca:django-ca .coverage /var/lib/django-ca/ /usr/src/django-ca/ca

# From here on, we run as normal user
USER django-ca:django-ca

# Run linters and unit tests
COPY devscripts/ devscripts/
RUN python dev.py code-quality
ARG FAIL_UNDER=100
RUN python dev.py coverage --format=text --fail-under=$FAIL_UNDER

# Run mypy (not yet - we need cryptography 3.5 for that)
#COPY .mypy.ini ./
#COPY stubs/ stubs/
#RUN mypy ca/django_ca/

# Use twine to check source distribution and wheel
COPY --from=dist-base /usr/src/django-ca/dist/ dist/
RUN twine check --strict dist/*

# Generate documentation
ADD docker-compose.yml ./
RUN make -C docs html

# create demo
RUN python dev.py init-demo

###############
# Build stage #
###############
FROM build as prepare
COPY --from=build /install /install

COPY ca/ ca/
COPY scripts/* ca/
COPY conf/ ca/conf/
COPY uwsgi/ uwsgi/
COPY nginx/ nginx/
RUN rm -rf requirements/ ca/django_ca/tests ca/ca/test_settings.py ca/ca/localsettings.py.example ca/.coverage

# Test that imports are working
COPY dev.py common.py ./
RUN cp -a /install/* /usr/local/
ENV DJANGO_CA_SECRET_KEY=dummy
COPY devscripts/test-imports.py ./
RUN ./test-imports.py

# Remove files from working directory
RUN rm dev.py

# Seems like with BuildKit, the test stage is never executed unless we somehow depend on it
COPY --from=test /usr/src/django-ca/.coverage /tmp
COPY --from=sdist-test /usr/src/django-ca/test-imports.py /tmp
COPY --from=wheel-test /usr/src/django-ca/test-imports.py /tmp
COPY --from=wheel-test-acme /usr/src/django-ca/test-imports.py /tmp
COPY --from=wheel-test-redis /usr/src/django-ca/test-imports.py /tmp
COPY --from=wheel-test-celery /usr/src/django-ca/test-imports.py /tmp
COPY --from=wheel-test-mysql /usr/src/django-ca/test-imports.py /tmp
COPY --from=wheel-test-postgres /usr/src/django-ca/test-imports.py /tmp

###############
# final stage #
###############
FROM base
COPY --from=prepare /install /usr/local

RUN mkdir -p /usr/share/django-ca/static /usr/share/django-ca/media /var/lib/django-ca/ \
             /var/lib/django-ca/certs/ca/shared /var/lib/django-ca/certs/ocsp \
             /var/lib/django-ca/shared && \
    chown -R django-ca:django-ca /usr/share/django-ca/ /var/lib/django-ca/

COPY --from=prepare /usr/src/django-ca/ ./
RUN ln -s /usr/src/django-ca/ca/manage.py /usr/local/bin/manage

USER django-ca:django-ca
EXPOSE 8000
VOLUME ["/var/lib/django-ca/", "/usr/share/django-ca/media/"]
WORKDIR /usr/src/django-ca/ca/
ENV DJANGO_CA_SETTINGS=conf/
CMD ./uwsgi.sh
