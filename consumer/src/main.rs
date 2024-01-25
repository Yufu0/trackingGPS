use std::env;
use dotenv::dotenv;
use serde::Deserialize;
use tokio_postgres::{NoTls, Error, Client, Connection, Socket};
use kafka::consumer::{Consumer, FetchOffset, GroupOffsetStorage};
use tokio_postgres::tls::NoTlsStream;
use uuid::Uuid;
use chrono::{NaiveDateTime, TimeZone, Utc};
use std::{thread, time};

#[derive(Deserialize,Debug)]
struct Coordonnees {
    id: String,
    longitude: f64,
    latitude: f64,
    date: i64,
}


#[tokio::main]
async fn main() {

    dotenv().ok();
    
    let user = env::var("DB_USER").expect("DB_USER not set");
    let password = env::var("DB_PASSWORD").expect("DB_PASSWORD not set");
    let dbname = env::var("DB_NAME").expect("DB_NAME not set");
    let dbhost = env::var("DB_HOST").expect("DB_HOST not set");
    let kafkahost = env::var("KAFKA_HOST").expect("KAFKA_HOST not set");
    let connection_string = format!(
        "user={} password={} dbname={} host={}",
        user, password, dbname, kafkahost
    );
    println!("{}",connection_string);
    let db_url = format!("postgresql://{}:{}@{}/{}", user,password,dbhost,dbname);

    let mut client:Client;
    let mut connection:Connection<Socket,NoTlsStream>;

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
    thread::sleep(five_seconds);

    let mut consumer =
        Consumer::from_hosts(vec!(kafkahost.to_owned()))
            .with_topic("coordinates".to_owned())
            .with_fallback_offset(FetchOffset::Earliest)
            .with_group("2".to_owned())
            .with_offset_storage(Some(GroupOffsetStorage::Kafka)).create().unwrap();



     loop {
         for ms in consumer.poll().unwrap().iter() {

             for m in ms.messages() {
                 let lm = match std::str::from_utf8(m.value) {
                     Ok(mess) => mess,
                     Err(e) => {
                         eprintln!("Erreur lors de la lecture du message : {}", e);
                         // Autres actions en cas d'erreur, par exemple retourner ou quitter
                         continue;
                     }
                 };
                let res : Coordonnees = match serde_json::from_str(lm) {
                     Ok(coo) => coo,
                     Err(e) => {
                         eprintln!("Erreur lors de la transformation JSON -> Coordonnées : {}", e);
                         // Autres actions en cas d'erreur, par exemple retourner ou quitter
                         continue;
                     }
                 };
                 put_item(&client, res).await.expect("Error inserting into PostgreSQL");

             }
             consumer.consume_messageset(ms).expect("TODO: panic message");
         }
         match consumer.commit_consumed(){
             Ok(_)=> {},
             Err(e) => {
                 eprintln!("Erreur est surevenu a la consommation : {}", e);
                 // Autres actions en cas d'erreur, par exemple retourner ou quitter
                 continue;
             }
         };
     } 

 }



async fn put_item(client: &Client, co: Coordonnees) -> Result<(), Error> {
     let id: Uuid = Uuid::new_v5(&Uuid::NAMESPACE_DNS, format!("{}{}", co.id, co.date).as_ref());
     println!("{}",id);
     match client
         .execute(
             "INSERT INTO item_tracker (id,name, longitude, latitude, datetime) VALUES ($5,$1, $2, $3, $4)",
             &[&co.id, &co.longitude, &co.latitude, &co.date,&id.to_string()],
         ).await
         {
         Ok(_)=> {},
         Err(e) => {
             eprintln!("Erreur est surevenu a la consommation : {}", e);
         }
     };
     notify_postgres(&client, id).await;
     Ok(())
 }

async fn notify_postgres(client: &Client, id: Uuid) {
    let notify_query = format!("NOTIFY tracker_channel, '{}'", id);
    client.execute(&notify_query, &[]).await.expect("Failed to notify PostgreSQL");
}



