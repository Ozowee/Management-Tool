# Stock-Management-Tool
A tool created for management products and products stock in your warehouse

# v 0.1 ALPHA :rocket:
- adding products,sizes and stocks to the mongoDB
- bulk adding products from CSV file
- checking stocks and sizes for the desired product ID from mongoDB
- DiscordBot as a commands handler
- clearing records for desired SKU
- removing data from mongoDB
- checking all info from DB
- own collection in DB for each user

# Roadmap
- improve bot handling
- make a website to use the tool
- user login, auth
- bug fixes if happens

# Changelog
- Alpha Version, tests begins
- discord / command handling for every function, including import from csv file
- minor changs on `Add` `Check` `Remove`
- separate collections for each user
- more information about SKU is returned
- adding more ProductInfo to the DB during `add`
- `Remove` command Added
- mirror changes on `add` and `check`
- rewrited code to use MongoDB instead of json file
- `Drop` command Added
- add data from CSV file to the DB
