FROM rust:latest

WORKDIR /usr/src/myapp

COPY ./Cargo.toml ./

COPY ./src ./src

COPY ./.env ./
RUN cargo build
CMD ["cargo", "run"]
