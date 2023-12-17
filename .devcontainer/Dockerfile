FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Install Parsons certs
RUN cd /usr/local/share/ca-certificates/ && \
    mkdir parsons; cd parsons && \
    curl http://pki.parsons.com/pki/TXDAL11ECA01.Parsons.com_Parsons%20Corporate%20Enterprise%20Issuing%20CA.crt > Parsons_Corp_CA.crt && \
    curl http://pki.parsons.com/Parsons%20Corporate%20Global%20Root%20CA.crt > Parsons_Global_CA.crt && \
    curl http://repository.parsons.com/certs/cert_Parsons_Forward_Trust.crt > Parsons_Forward_CA.crt && \
    curl http://repository.parsons.com/certs/cert_lab_decrypt_forward_trust.crt > Parsons_Lab_Forward_CA.crt && \
    chmod 755 ../parsons && \
    chmod 644 Parsons* && \
    update-ca-certificates
