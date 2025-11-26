FROM fluentd:v1.19.0-debian-1.0

RUN rm -f /fluentd/etc/fluent.conf
COPY ./conf/* /fluentd/etc/

EXPOSE 24224
