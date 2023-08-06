FROM continuumio/miniconda3 as build

COPY environment.yml .
RUN conda env create -f environment.yml

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n grimoire -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack


#runtime image
FROM debian:buster AS runtime

COPY --from=build /venv /venv
COPY . /app
WORKDIR /app

CMD  bash -c "source /venv/bin/activate && ./cli.py api serve"
