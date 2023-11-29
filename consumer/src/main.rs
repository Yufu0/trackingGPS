use std::time::SystemTime;
use tokio_postgres::{NoTls, Error};

#[derive(Debug)]
struct Coordonnees {
    id: i32,
    longitude: f64,
    latitude: f64,
    date: SystemTime,
}


#[tokio::main]
async fn main() -> Result<(), Error> {

    let db_url = "postgresql://postgres:postgres@localhost/tracker";

    let (client, connection) = tokio_postgres::connect(db_url, NoTls).await?;
    println!("a");
    // Spawn a task to handle the connection
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("connection error: {}", e);
        }
    });
    println!("a");


    let co = Coordonnees {
        id: 1,
        longitude: -63572375290155.0,
        latitude: 106744840359415.0,
        date: SystemTime::now(),
    };
    println!("a");

    put_item(&client, &co).await?;
    println!("a");

    Ok(())
}



async fn put_item(client: &tokio_postgres::Client, co: &Coordonnees) -> Result<(), Error> {
    client
        .execute(
            "INSERT INTO item_tracker (id, longitude, latitude, datetime) VALUES ($1, $2, $3, $4)",
            &[&co.id, &co.longitude, &co.latitude, &co.date],
        )
        .await?;

    Ok(())
}