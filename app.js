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

function priceToSql(sql, params, field, operator) {
  sql += ` AND CAST(REPLACE(REPLACE(price, '.', ''), ' €', '') AS UNSIGNED) ${operator} ?`;
  params.push(field);
  return sql;
}

function buildSql(filters) {
  let sql = "SELECT * FROM properties WHERE 1=1";
  const params = [];

  if (filters.location) {
    sql += " AND location LIKE ?";
    params.push(`%${filters.location}%`);
  }

  if (filters.type) {
    sql += " AND property_type = ?";
    params.push(filters.type);
  }

  if (filters.rooms) {
    sql += " AND CAST(rooms AS UNSIGNED) = ?";
    params.push(filters.rooms);
  }

  if (filters.bedrooms) {
    sql += " AND CAST(rooms AS UNSIGNED) = ?";
    params.push(filters.bedrooms);
  }

  if (filters.min_bedrooms) {
    sql += " AND CAST(rooms AS UNSIGNED) >= ?";
    params.push(filters.min_bedrooms);
  }

  if (filters.bathrooms) {
    sql += " AND CAST(bathrooms AS UNSIGNED) >= ?";
    params.push(filters.bathrooms);
  }

  if (filters.min_square_meters) {
    sql += " AND CAST(square_meters AS UNSIGNED) >= ?";
    params.push(filters.min_square_meters);
  }

  if (filters.max_square_meters) {
    sql += " AND CAST(square_meters AS UNSIGNED) <= ?";
    params.push(filters.max_square_meters);
  }

  if (filters.min_price) {
    sql = priceToSql(sql, params, filters.min_price, ">=");
  }

  if (filters.max_price) {
    sql = priceToSql(sql, params, filters.max_price, "<=");
  }

  sql += " LIMIT 100";

  return { sql, params };
}

async function getProperties(filters) {
  const { sql, params } = buildSql(filters);

  const connection = await mysql.createConnection(dbConfig);
  const [properties] = await connection.execute(sql, params);
  await connection.end();

  return properties;
}

app.get("/", async (req, res) => {
  const properties = await getProperties(req.query);

  res.render("index", {
    properties,
    filters: req.query,
    aiPrompt: "",
    aiError: "",
  });
});

app.get("/ai-search", async (req, res) => {
  const userPrompt = req.query.prompt || "";

  try {
    const ollamaResponse = await fetch("http://localhost:11434/api/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "llama3",
        stream: false,
        prompt: `
You extract real estate search filters from user text.

Return ONLY valid JSON. No explanation. No markdown.

Return ONLY this JSON structure:
{
  "location": "",
  "type": "",
  "min_price": "",
  "max_price": "",
  "bedrooms": "",
  "min_bedrooms": "",
  "bathrooms": "",
  "min_square_meters": "",
  "max_square_meters": ""
}

Allowed type values:
flat, house, penthouse, studio, ground-floor apartment

Rules:
- Use numbers only for prices, bedrooms, bathrooms and square meters.
- If the user says cheap, use max_price 300000.
- If the user mentions a number of kids, use number of kids plus one as bedrooms.
- If the user mentions pets, use min_square_meters 80.
- If the user says expensive or luxury, use min_price 700000.
- If the user says mid range prices, use min_price 300000 and max_price 700000.
- If the user says not too expensive, it means mid range.
- If the user says not too cheap, it means mid range.
- If the user says "2 bedrooms", use "bedrooms": 2.
- If the user says "at least 2 bedrooms", "2 or more bedrooms", or "minimum 2 bedrooms", use "min_bedrooms": 2.
- If a field is not mentioned, leave it empty.
- Translate Spanish property words:
  piso = flat
  ático = penthouse
  casa/chalet = house
  estudio = studio
  bajo = ground-floor apartment

User query:
"${userPrompt}"
`,
      }),
    });

    const data = await ollamaResponse.json();
    const filters = JSON.parse(data.response);

    console.log("AI filters:", filters);

    const properties = await getProperties(filters);

    res.render("index", {
      properties,
      filters,
      aiPrompt: userPrompt,
      aiError: "",
    });

  } catch (error) {
    console.log("AI error:", error.message);

    const properties = await getProperties({});

    res.render("index", {
      properties,
      filters: {},
      aiPrompt: userPrompt,
      aiError: "AI search is not available. Make sure Ollama is running.",
    });
  }
});

app.get("/property/:id", async (req, res) => {
  const connection = await mysql.createConnection(dbConfig);

  const [rows] = await connection.execute(
    "SELECT * FROM properties WHERE id = ?",
    [req.params.id]
  );

  await connection.end();

  res.render("detail", {
    property: rows[0],
  });
});

app.listen(PORT, () => {
  console.log(`App running at http://localhost:${PORT}`);
});