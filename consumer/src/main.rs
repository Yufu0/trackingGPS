use std::{env, time};

use dotenv::dotenv;
use kafka::consumer::{Consumer, FetchOffset, GroupOffsetStorage};
use serde::Deserialize;
use tokio_postgres::{Client, Connection, Error, NoTls, Socket};
use tokio_postgres::tls::NoTlsStream;
use uuid::Uuid;

#[derive(Deserialize,Debug)]
struct Location {
    id: String,
    longitude: f64,
    latitude: f64,
    date: i64,
}

#[tokio::main]
async fn main() {
    dotenv().ok();
    
    let user: String = env::var("DB_USER").expect("DB_USER not set");
    let password: String = env::var("DB_PASSWORD").expect("DB_PASSWORD not set");
    let db_name: String = env::var("DB_NAME").expect("DB_NAME not set");
    let db_host: String = env::var("DB_HOST").expect("DB_HOST not set");
    let kafka_host: String = env::var("KAFKA_HOST").expect("KAFKA_HOST not set");
    let db_url: String = format!("postgresql://{}:{}@{}/{}", user, password, db_host, db_name);

    let client:Client;
    let connection:Connection<Socket,NoTlsStream>;

    loop {
        match tokio_postgres::connect(&*db_url, NoTls).await {
            Ok(cl) => {
                client=cl.0;
                connection=cl.1;
                break;
            }
            Err(e) => {
                eprintln!("Erreur lors de la connetion a la base de données : {}", e);
            }
        }
    }

    // Spawn a task to handle the connection
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("connection error: {}", e);
        }
    });

    // Wait 5 seconds to be sure that the connection is established
    let five_seconds = time::Duration::from_secs(5);
    tokio::time::sleep(five_seconds).await;

    let mut consumer =
        Consumer::from_hosts(vec!(kafka_host.to_owned()))
            .with_topic("coordinates".to_owned())
            .with_fallback_offset(FetchOffset::Earliest)
            .with_group("2".to_owned())
            .with_offset_storage(Some(GroupOffsetStorage::Kafka)).create().unwrap();

    loop {
         for ms in consumer.poll().unwrap().iter() {
             for m in ms.messages() {
                 let lm: &str = match std::str::from_utf8(m.value) {
                     Ok(mess) => mess,
                     Err(e) => {
                         eprintln!("Erreur lors de la lecture du message : {}", e);
                         // In case of other errors (return or break)
                         continue;
                     }
                 };
                 let location: Location = match serde_json::from_str(lm) {
                     Ok(coo) => coo,
                     Err(e) => {
                         eprintln!("Erreur lors de la transformation JSON -> Coordonnées : {}", e);
                         // In case of other errors (return or break)
                         continue;
                     }
                 };
                 put_item(&client, location).await.expect("Error inserting into PostgreSQL");

             }
             consumer.consume_messageset(ms).expect("TODO: panic message");
         }

         match consumer.commit_consumed(){
             Ok(_)=> {},
             Err(e) => {
                eprintln!("Erreur est surevenu a la consommation : {}", e);
                // In case of other errors (return or break)
                continue;
             }
         };
    }
}

async fn put_item(client: &Client, co: Location) -> Result<(), Error> {
     let id: Uuid = Uuid::new_v5(&Uuid::NAMESPACE_DNS, format!("{}{}", co.id, co.date).as_ref());
     match client
         .execute(
             "INSERT INTO item_tracker (id,name, longitude, latitude, datetime) VALUES ($5,$1, $2, $3, $4)",
             &[&co.id, &co.longitude, &co.latitude, &co.date,&id.to_string()],
         ).await {
             Ok(_)=> {},
             Err(e) => {
                 eprintln!("An error occurred when inserting into PostgreSQL: {}", e);
             }
         };

    notify_postgres(&client, id).await;
     Ok(())
 }

async fn notify_postgres(client: &Client, id: Uuid) {
    let notify_query: String = format!("NOTIFY tracker_channel, '{}'", id);
    client.execute(&notify_query, &[]).await.expect("Failed to notify PostgreSQL");
}



