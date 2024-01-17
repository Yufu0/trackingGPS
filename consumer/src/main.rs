use std::time::{Duration, SystemTime, UNIX_EPOCH};
use serde::Deserialize;
use tokio_postgres::{NoTls, Error, Client, Connection, Socket};
use kafka::consumer::{Consumer, FetchOffset, GroupOffsetStorage};
use tokio_postgres::tls::NoTlsStream;
use tokio_postgres::types::ToSql;

#[derive(Deserialize,Debug)]
struct Coordonnees {
    id: String,
    longitude: f64,
    latitude: f64,
    date: u64,
}


#[tokio::main]
async fn main() {

    let db_url = "postgresql://postgres:postgres@localhost/tracker";

    let mut client:Client;
    let mut connection:Connection<Socket,NoTlsStream>;

    loop {
        match tokio_postgres::connect(db_url, NoTls).await {
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


    let mut consumer =
        Consumer::from_hosts(vec!("172.17.9.221:29093".to_owned()))
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



 async fn put_item(client: &tokio_postgres::Client, co: Coordonnees) -> Result<(), Error> {
     println!("{:?}", co);
     match client
         .execute(
             "INSERT INTO item_tracker (id, longitude, latitude, datetime) VALUES ($1, $2, $3, $4)",
             &[&co.id, &co.longitude, &co.latitude, &(UNIX_EPOCH + Duration::from_secs(co.date))],
         ).await
         {
         Ok(_)=> println!("Bien"),
         Err(e) => {
             eprintln!("Erreur est surevenu a la consommation : {}", e);
         }
     };
     notify_postgres(&client, co.id).await;
     Ok(())
 }

async fn notify_postgres(client: &tokio_postgres::Client, id: String) {
    let notify_query = format!("NOTIFY your_channel, 'id={}'", id);
    client.execute(&notify_query, &[]).await.expect("Failed to notify PostgreSQL");
}