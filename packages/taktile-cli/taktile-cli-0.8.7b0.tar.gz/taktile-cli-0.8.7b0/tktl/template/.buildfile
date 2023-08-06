FROM taktile/taktile-runtime:__version__ AS build_step

ENV APPDIR /app

WORKDIR $APPDIR

# Install requirements
COPY ./requirements.txt ${APPDIR}/user_requirements.txt
RUN pip install -r ${APPDIR}/user_requirements.txt

# Copy code and assets for running the application
COPY ./src ${APPDIR}/src
COPY ./assets ${APPDIR}/assets
RUN mkdir -p ${APPDIR}/user_tests
COPY ./requirements.txt tests/* ${APPDIR}/user_tests/
RUN rm ${APPDIR}/user_tests/requirements.txt

#
# DO NOT EDIT ANYTHING BELOW THIS COMMENT
#
FROM build_step

ARG RESOURCE_NAME
ARG DEPLOYMENT_API_URL
ARG TAKTILE_GIT_REF
ARG COMMIT_HASH
ARG TAKTILE_GIT_SHA
ARG LOCAL_CLUSTER
ARG TAKTILE_UPDATE_KEY
ARG REMOTE_ARG=unset


WORKDIR /kaniko/buildcontext/

RUN git lfs install
RUN git config remote.origin.url $REMOTE_ARG
RUN git lfs pull origin
COPY ./assets ${APPDIR}/assets

WORKDIR $APPDIR

# Run tests conditionally
RUN bash /app/scripts/run-tests-and-export.sh $COMMIT_HASH $TAKTILE_UPDATE_KEY $DEPLOYMENT_API_URL $LOCAL_CLUSTER $RESOURCE_NAME
