use std::time::{Duration, UNIX_EPOCH};
use serde::Deserialize;
use tokio_postgres::{NoTls, Error};
use kafka::consumer::{Consumer, FetchOffset, GroupOffsetStorage};

#[derive(Deserialize,Debug)]
struct Coordonnees {
    id: String,
    longitude: f64,
    latitude: f64,
    date: u64,
}


#[tokio::main]
async fn main(){

    let db_url = "postgresql://postgres:postgres@localhost/tracker";

    let (client, connection) = tokio_postgres::connect(db_url, NoTls).await?;

    // Spawn a task to handle the connection
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("connection error: {}", e);
        }
    });

    let mut consumer =
        Consumer::from_hosts(vec!("localhost:9092".to_owned()))
            .with_topic_partitions("coordinates".to_owned(), &[0, 1])
            .with_fallback_offset(FetchOffset::Earliest)
            .with_group("my-group".to_owned())
            .with_offset_storage(Some(GroupOffsetStorage::Kafka))
            .create()
            .unwrap();
    loop {
        for ms in consumer.poll().unwrap().iter() {
            for m in ms.messages() {
                println!("{:?}", m);
                /*
                    let res : Coordonnees = serde_json::from_str(m).unwrap();
                    put_item(&client, res).await.expect("Error inserting into PostgreSQL");
                */
            }
            consumer.consume_messageset(ms).expect("TODO: panic message");
        }
        consumer.commit_consumed().unwrap();
    }
}



async fn put_item(client: &tokio_postgres::Client, co: Coordonnees) -> Result<(), Error> {
    client
        .execute(
            "INSERT INTO item_tracker (id, longitude, latitude, datetime) VALUES ($1, $2, $3, $4)",
            &[&co.id, &co.longitude, &co.latitude, &(UNIX_EPOCH + Duration::from_secs(co.date))],
        )
        .await?;

    Ok(())
}