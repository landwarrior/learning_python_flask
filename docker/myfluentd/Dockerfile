FROM fluentd:v1.16.2-debian-1.1

RUN rm -f /fluentd/etc/fluent.conf
COPY ./conf/* /fluentd/etc/

EXPOSE 24224
