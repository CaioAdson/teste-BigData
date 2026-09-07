FROM eclipse-temurin:11-jre
ARG FLUME_VERSION=1.11.0
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -fsSL "https://archive.apache.org/dist/flume/${FLUME_VERSION}/apache-flume-${FLUME_VERSION}-bin.tar.gz" | tar -xz -C /opt \
    && mv "/opt/apache-flume-${FLUME_VERSION}-bin" /opt/flume \
    && apt-get purge -y curl && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="/opt/flume/bin:${PATH}"
