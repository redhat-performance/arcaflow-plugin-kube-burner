# build poetry
FROM quay.io/centos/centos:stream8 as poetry

RUN dnf -y module install python39 && dnf -y install python39 python39-pip git

WORKDIR /app

COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN python3.9 -m pip install poetry \
 && python3.9 -m poetry config virtualenvs.create false \
 && python3.9 -m poetry install --without dev \
 && python3.9 -m poetry export -f requirements.txt --output requirements.txt --without-hashes

ENV package arcaflow_plugin_kubeburner
# run tests
COPY ${package}/ /app/${package}
COPY test_kubeburner_plugin.py /app/

ENV PYTHONPATH /app/${package}
RUN mkdir /htmlcov
RUN pip3 install coverage
RUN python3 -m coverage run test_kubeburner_plugin.py
RUN python3 -m coverage html -d /htmlcov --omit=/usr/local/*


# final image
FROM quay.io/centos/centos:stream8
ENV package arcaflow_plugin_kubeburner
RUN dnf -y module install python39 && dnf -y install python39 python39-pip
WORKDIR /app

COPY --from=poetry /app/requirements.txt /app/
COPY --from=poetry /htmlcov /htmlcov/
COPY LICENSE /app/
COPY README.md /app/
COPY ${package}/ /app/${package}
RUN curl -L https://github.com/cloud-bulldozer/kube-burner/releases/download/v1.3/kube-burner-1.3-Linux-x86_64.tar.gz | tar xz -C /app/ kube-burner
RUN git clone https://github.com/redhat-performance/web-burner.git /app/
RUN cp -r /app/web-burner/workload /app/web-burner/objectTemplates /app/
RUN python3.9 -m pip install -r requirements.txt
WORKDIR /app
ENTRYPOINT ["python3", "arcaflow_plugin_kubeburner/kubeburner_plugin.py"]
CMD []

LABEL org.opencontainers.image.source="https://github.com/redhat-performance/arcaflow-plugin-kube-burner"
LABEL org.opencontainers.image.licenses="Apache-2.0+GPL-2.0-only"
LABEL org.opencontainers.image.vendor="Arcalot project"
LABEL org.opencontainers.image.authors="Arcalot contributors"
LABEL org.opencontainers.image.title="Kube-burner Arcalot Plugin"
LABEL io.github.arcalot.arcaflow.plugin.version="1"
