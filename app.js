const express = require("express");
const mysql = require("mysql2/promise");

const app = express();
const PORT = 3000;

app.set("view engine", "ejs");
app.use(express.static("public"));

const dbConfig = {
  host: "localhost",
  port: 3306,
  user: "user_mydb",
  password: "rootPASSWORD",
  database: "my_db",
};

app.get("/", async (req, res) => {
  const connection = await mysql.createConnection(dbConfig);

  const [properties] = await connection.execute(
    "SELECT * FROM properties LIMIT 50"
  );

  await connection.end();

  res.render("index", { properties });
});

app.get("/property/:id", async (req, res) => {
  const connection = await mysql.createConnection(dbConfig);

  const [rows] = await connection.execute(
    "SELECT * FROM properties WHERE id = ?",
    [req.params.id]
  );

  await connection.end();

  res.render("detail", { property: rows[0] });
});

app.listen(PORT, () => {
  console.log(`App running at http://localhost:${PORT}`);
});