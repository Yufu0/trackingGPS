FROM maven:3.9.6-ibm-semeru-17-focal

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN mvn clean install

CMD ["mvn", "spring-boot:run"]